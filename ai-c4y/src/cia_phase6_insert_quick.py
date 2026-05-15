"""
cia_phase6_insert_quick.py

Phase 6 (Quick) — RAG Vector Store Insertion WITHOUT LLM calls.

Instead of calling an LLM to generate keywords and summaries, this phase:
  - Uses the section header as the keyword string for embedding.
  - Builds the summary from the csharp-manifest.json entry for that file
    (file_type, architecture_layer, is_critical, folder, section).
    Falls back to truncated section content if no manifest entry is found.
  - Adds folder_path to metadata so queries can filter by module/layer.

This is significantly faster than Phase 6 (full) and suitable when you
want to quickly populate the vector store for initial testing or when
the manifest metadata is already rich enough to power retrieval.

Resume model: identical to cia_phase6_insert.py — per-chunk .done markers.
  {rag_done_folder}/{file_name}_c{chunk_idx}.done
Re-running the command resumes from where it left off with no duplicates.

Concurrency: each worker runs embedding + DB insert in a thread pool
(asyncio.to_thread) so N workers genuinely run in parallel even though
both calls are synchronous.
"""

import asyncio
import json
import os

from tqdm import tqdm

from .cia_config import (
    DEFAULT_RAG_CHUNKS_FOLDER,
    DEFAULT_RAG_DONE_FOLDER,
    DEFAULT_INDEX_PATH,
)
from .FileHanlder import split_markdown_header_and_content, remove_excessive_spacing
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding

CIA_MANIFEST_PATH = os.getenv("CIA_MANIFEST_PATH", "wip/csharp-manifest.json")


def _load_manifest_lookup(manifest_path: str) -> dict:
    """
    Build a {file_stem -> manifest_entry} lookup from csharp-manifest.json.

    Manifest keys are full relative CS paths like:
      Core/Business/VoyageManagement/Voyage/GetVoyageById.cs

    We index by bare filename stem (GetVoyageById) so chunk files can find
    their manifest entry without knowing the full source path.
    If two files share a stem (rare), the last one wins.
    """
    if not os.path.exists(manifest_path):
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    lookup = {}
    for cs_path, entry in raw.items():
        stem = os.path.splitext(os.path.basename(cs_path))[0]
        # Also store the original cs_path and folder inside the entry
        merged = dict(entry)
        merged["_cs_path"] = cs_path
        merged["_cs_folder"] = os.path.dirname(cs_path).replace("\\", "/")
        lookup[stem] = merged
    return lookup


def _build_quick_summary(file_name: str, header: str, folder_path: str, manifest_entry: dict | None, sentence: str) -> str:
    """
    Compose a summary string from manifest metadata (no LLM).
    Falls back to truncated section content when no manifest entry exists.
    """
    if manifest_entry:
        parts = {
            "file": file_name,
            "section": header,
            "file_type": manifest_entry.get("file_type", ""),
            "layer": manifest_entry.get("architecture_layer", ""),
            "is_critical": manifest_entry.get("is_critical", False),
            "folder": manifest_entry.get("_cs_folder") or folder_path,
        }
        # Remove empty values to keep the JSON compact
        parts = {k: v for k, v in parts.items() if v not in ("", None)}
        return json.dumps(parts, ensure_ascii=False)
    # Fallback: first 600 chars of the section content
    return sentence[:600]


async def insert_rag_chunks_quick(
    rag_chunks_folder: str = DEFAULT_RAG_CHUNKS_FOLDER,
    rag_done_folder: str = DEFAULT_RAG_DONE_FOLDER,
    table_name: str = None,
    concurrency: int = 5,
):
    """
    Phase 6 (Quick): insert RAG chunks into Supabase with NO LLM calls.

    Embedding still runs (Ollama nomic-embed-text) — only keyword extraction
    and knowledge compression are skipped.
    """
    if not table_name:
        table_name = os.getenv("CIA_RAG_TABLE_NAME", "n8n_documents_csharp")

    if not os.path.exists(rag_chunks_folder):
        print(f"[Phase 6Q] Chunks folder not found: {rag_chunks_folder}")
        print("[Phase 6Q] Run --phase chunk first to generate RAG chunks.")
        return

    os.makedirs(rag_done_folder, exist_ok=True)

    # ── Load manifest lookup (best-effort) ───────────────────────────────────
    manifest_lookup = _load_manifest_lookup(CIA_MANIFEST_PATH)
    if manifest_lookup:
        print(f"[Phase 6Q] Manifest loaded: {len(manifest_lookup)} file entries available.")
    else:
        print("[Phase 6Q] No manifest found — summaries will fall back to truncated content.")

    # ── Collect all chunk files ───────────────────────────────────────────────
    all_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(rag_chunks_folder)
        for f in sorted(files)
        if f.endswith(".md")
    ]

    # ── Flatten files → (file_name, chunk_idx, header, sentence, done_marker, folder_path) ──
    all_chunks = []
    for file_path in all_files:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        rel_dir = os.path.relpath(os.path.dirname(file_path), rag_chunks_folder).replace("\\", "/")
        folder_path = rel_dir if rel_dir != "." else ""

        # Backward-compat: legacy per-file .done
        if os.path.exists(os.path.join(rag_done_folder, file_name + ".done")):
            continue

        with open(file_path, "r", encoding="utf-8") as fh:
            content = fh.read()

        sections = split_markdown_header_and_content(content)
        for chunk_idx, (header, section_content) in enumerate(sections):
            header = header.strip().replace(":", "")
            sentence = remove_excessive_spacing(section_content)
            if not sentence or len(sentence) < 5:
                continue

            chunk_key = f"{file_name}_c{chunk_idx}"
            done_marker = os.path.join(rag_done_folder, chunk_key + ".done")
            if os.path.exists(done_marker):
                continue

            all_chunks.append((file_name, chunk_idx, header, sentence, done_marker, folder_path))

    total_chunks = len(all_chunks)
    total_files = len(all_files)

    print(f"[Phase 6Q] No-LLM mode, {concurrency} parallel workers, table='{table_name}'")
    print(f"[Phase 6Q] {total_chunks} chunk(s) to insert (across {total_files} file(s)).")

    if total_chunks == 0:
        print("[Phase 6Q] Nothing to do — all chunks already inserted.")
        return

    # ── Shared resources ──────────────────────────────────────────────────────
    vector_store = SupabaseVectorStore(embedding=Embedding())
    results = {"done": 0, "error": 0}

    progress = tqdm(
        total=total_chunks,
        desc="[Phase 6Q] Inserting",
        unit="chunk",
        dynamic_ncols=True,
        bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {bar}",
    )

    # ── Queue + N workers ─────────────────────────────────────────────────────
    queue: asyncio.Queue = asyncio.Queue()
    for chunk_data in all_chunks:
        queue.put_nowait(chunk_data)

    shutdown_event = asyncio.Event()

    async def _worker(_worker_id: int):
        while not shutdown_event.is_set():
            try:
                file_name, chunk_idx, header, sentence, done_marker, folder_path = queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            inserted = False
            try:
                knowledge = f"# {header}: {sentence}"
                manifest_entry = manifest_lookup.get(file_name)
                summarize = _build_quick_summary(file_name, header, folder_path, manifest_entry, sentence)

                metadata = {
                    "file_name": file_name,
                    "section": header,
                    "folder_path": folder_path,
                    "keywords": header,  # section heading is the best no-LLM keyword signal
                }
                if manifest_entry:
                    metadata["file_type"] = manifest_entry.get("file_type", "")
                    metadata["architecture_layer"] = manifest_entry.get("architecture_layer", "")

                # Both embedding.run() and vector_store.insert() are synchronous
                # HTTP calls. Run in a thread so N workers are truly concurrent.
                await asyncio.to_thread(
                    vector_store.insert,
                    table_name=table_name,
                    content=knowledge,
                    metadata=metadata,
                    summarize=summarize,
                )
                inserted = True
                open(done_marker, "w").close()
                results["done"] += 1

            except asyncio.CancelledError:
                # If DB insert completed, save the marker to avoid re-inserting on resume
                if inserted:
                    try:
                        open(done_marker, "w").close()
                        results["done"] += 1
                    except Exception:
                        pass
                raise
            except Exception as e:
                results["error"] += 1
                tqdm.write(f"[Phase 6Q] ERROR in {file_name} / {header}: {e}")
            finally:
                progress.update(1)
                progress.set_postfix(ok=results["done"], err=results["error"], refresh=False)

    n_workers = max(1, concurrency)
    workers = [asyncio.create_task(_worker(i)) for i in range(n_workers)]
    try:
        await asyncio.gather(*workers)
    except (KeyboardInterrupt, asyncio.CancelledError):
        shutdown_event.set()
        tqdm.write("\n[Phase 6Q] Interrupt received — waiting for in-flight chunks to finish...")
        await asyncio.gather(*workers, return_exceptions=True)
        progress.close()
        remaining = queue.qsize()
        print(
            f"[Phase 6Q] Stopped safely. "
            f"{results['done']} inserted, {results['error']} errors, "
            f"{remaining} remaining. Re-run the same command to resume."
        )
        return

    progress.close()
    print(
        f"[Phase 6Q] Complete. "
        f"{results['done']} inserted, "
        f"{results['error']} failed (re-run to retry failed chunks)."
    )
