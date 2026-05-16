"""
cia_phase6_insert_quick.py

Phase 6 (Quick) — RAG Vector Store Insertion WITHOUT LLM calls.

Reads every chunk from the rag-chunks folder and inserts all of them
unconditionally. No resume / .done tracking — just a straight bulk load.
Re-running will re-insert everything (useful for table rebuilds).

Each chunk preserves full context:
  content  = "# {header}: {sentence}"
  metadata = file_name, section, folder_path, file_type, architecture_layer,
             manifest_summary (compact JSON from csharp-manifest.json)
  summarize = real chunk content text → embedding2 is semantically rich

Concurrency: N workers each run embedding + DB insert via asyncio.to_thread
so blocking HTTP calls are genuinely parallel.
"""

import asyncio
import json
import os

from tqdm import tqdm

from .cia_config import DEFAULT_RAG_CHUNKS_FOLDER, DEFAULT_RAG_DONE_QUICK_FOLDER
from .FileHanlder import split_markdown_header_and_content, remove_excessive_spacing
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding

CIA_MANIFEST_PATH = os.getenv("CIA_MANIFEST_PATH", "wip/csharp-manifest.json")


def _load_manifest_lookup(manifest_path: str) -> dict:
    """Build a {file_stem -> manifest_entry} lookup from csharp-manifest.json."""
    if not os.path.exists(manifest_path):
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    lookup = {}
    for cs_path, entry in raw.items():
        stem = os.path.splitext(os.path.basename(cs_path))[0]
        merged = dict(entry)
        merged["_cs_folder"] = os.path.dirname(cs_path).replace("\\", "/")
        lookup[stem] = merged
    return lookup


def _build_quick_summary(file_name: str, header: str, folder_path: str, manifest_entry: dict | None) -> str:
    """Build a compact JSON summary from the manifest entry for the metadata field."""
    if manifest_entry:
        parts = {
            "file": file_name,
            "section": header,
            "file_type": manifest_entry.get("file_type", ""),
            "layer": manifest_entry.get("architecture_layer", ""),
            "is_critical": manifest_entry.get("is_critical", False),
            "folder": manifest_entry.get("_cs_folder") or folder_path,
        }
        parts = {k: v for k, v in parts.items() if v not in ("", None)}
        return json.dumps(parts, ensure_ascii=False)
    return ""


async def insert_rag_chunks_quick(
    rag_chunks_folder: str = DEFAULT_RAG_CHUNKS_FOLDER,
    rag_done_folder: str = DEFAULT_RAG_DONE_QUICK_FOLDER,
    table_name: str = None,
    concurrency: int = 5,
):
    """Phase 6 (Quick): bulk-insert all RAG chunks with NO LLM calls, no skip logic."""
    if not table_name:
        table_name = os.getenv("CIA_RAG_TABLE_NAME", "n8n_documents_csharp")

    if not os.path.exists(rag_chunks_folder):
        print(f"[Phase 6Q] Chunks folder not found: {rag_chunks_folder}")
        print("[Phase 6Q] Run --phase chunk first to generate RAG chunks.")
        return

    os.makedirs(rag_done_folder, exist_ok=True)

    manifest_lookup = _load_manifest_lookup(CIA_MANIFEST_PATH)
    if manifest_lookup:
        print(f"[Phase 6Q] Manifest loaded: {len(manifest_lookup)} entries.")
    else:
        print("[Phase 6Q] No manifest — summaries will use truncated content.")

    # ── Collect all chunks from every .md file ────────────────────────────────
    all_chunks = []
    for root, _, files in os.walk(rag_chunks_folder):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            file_path = os.path.join(root, f)
            file_name = os.path.splitext(f)[0]
            rel_dir = os.path.relpath(root, rag_chunks_folder).replace("\\", "/")
            folder_path = rel_dir if rel_dir != "." else ""

            with open(file_path, "r", encoding="utf-8") as fh:
                content = fh.read()

            for chunk_idx, (header, section_content) in enumerate(split_markdown_header_and_content(content)):
                header = header.strip().replace(":", "")
                sentence = remove_excessive_spacing(section_content)
                if not sentence or len(sentence) < 5:
                    continue

                done_marker = os.path.join(rag_done_folder, f"{file_name}_c{chunk_idx}.done")
                if os.path.exists(done_marker):
                    continue

                all_chunks.append((file_name, chunk_idx, header, sentence, done_marker, folder_path))

    total = len(all_chunks)
    already_done = sum(
        1 for root, _, files in os.walk(rag_done_folder)
        for f in files if f.endswith(".done")
    )
    print(f"[Phase 6Q] {concurrency} parallel workers | table='{table_name}' | {total} chunks to insert (already done: {already_done})")

    if total == 0:
        print("[Phase 6Q] Nothing to do — all chunks already inserted.")
        return

    # ── Delete old DB rows for every file that has pending chunks ─────────────
    # Ensures re-runs on changed files don't accumulate duplicate records.
    # Track (file_name, folder_path) pairs to avoid deleting rows from a
    # different file that happens to share the same stem name in another folder.
    pending_files = {(c[0], c[5]) for c in all_chunks}  # (file_name, folder_path)
    pending_file_names = {c[0] for c in all_chunks}
    print(f"[Phase 6Q] Deleting old DB rows for {len(pending_files)} file(s) before insert...")
    _cleanup_store = SupabaseVectorStore(embedding=Embedding())
    total_deleted = 0
    for fn, fp in pending_files:
        try:
            n = _cleanup_store.delete_by_file_name(table_name, fn, folder_path=fp)
            total_deleted += n
            # Also wipe any stale .done markers for this file so the worker re-inserts all its chunks
            for root, _, files in os.walk(rag_done_folder):
                for df in files:
                    if df.startswith(f"{fn}_c") and df.endswith(".done"):
                        os.remove(os.path.join(root, df))
        except Exception as exc:
            print(f"[Phase 6Q] WARNING: could not delete rows for '{fp}/{fn}': {exc}")
    print(f"[Phase 6Q] Deleted {total_deleted} old row(s) from '{table_name}'.")

    # Re-collect chunks now that .done markers have been cleared
    all_chunks = []
    for root, _, files in os.walk(rag_chunks_folder):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            file_name = os.path.splitext(f)[0]
            if file_name not in pending_file_names:
                continue  # not a pending file — skip
            file_path = os.path.join(root, f)
            rel_dir = os.path.relpath(root, rag_chunks_folder).replace("\\", "/")
            folder_path = rel_dir if rel_dir != "." else ""
            with open(file_path, "r", encoding="utf-8") as fh:
                content = fh.read()
            for chunk_idx, (header, section_content) in enumerate(split_markdown_header_and_content(content)):
                header = header.strip().replace(":", "")
                sentence = remove_excessive_spacing(section_content)
                if not sentence or len(sentence) < 5:
                    continue
                done_marker = os.path.join(rag_done_folder, f"{file_name}_c{chunk_idx}.done")
                all_chunks.append((file_name, chunk_idx, header, sentence, done_marker, folder_path))
    total = len(all_chunks)
    print(f"[Phase 6Q] {total} chunk(s) will be (re-)inserted.")

    # ── Queue + N workers ─────────────────────────────────────────────────────
    results = {"done": 0, "error": 0}

    queue: asyncio.Queue = asyncio.Queue()
    for chunk in all_chunks:
        queue.put_nowait(chunk)

    progress = tqdm(
        total=total,
        desc="[Phase 6Q] Inserting",
        unit="chunk",
        dynamic_ncols=True,
        bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {bar}",
    )

    # Each worker owns its own SupabaseVectorStore so a connection reset on one
    # worker doesn't affect the others. Retries also get a fresh instance.
    _MAX_RETRIES = 4
    _RETRY_BASE_DELAY = 2.0  # seconds, doubles on each attempt

    async def _worker():
        worker_store = SupabaseVectorStore(embedding=Embedding())
        while True:
            try:
                file_name, chunk_idx, header, sentence, done_marker, folder_path = queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            manifest_entry = manifest_lookup.get(file_name)
            metadata = {
                "file_name": file_name,
                "section": header,
                "folder_path": folder_path,
                "keywords": header,
            }
            if manifest_entry:
                metadata["file_type"] = manifest_entry.get("file_type", "")
                metadata["architecture_layer"] = manifest_entry.get("architecture_layer", "")
            # Always include the manifest summary JSON so every row has structured context for filtering/display
            metadata["summary_json"] = _build_quick_summary(file_name, header, folder_path, manifest_entry)

            # summarize = actual chunk text so embedding2 indexes rich semantic content,
            # not just a compact JSON blob — both embeddings now cover meaningful text
            summarize = sentence

            last_exc = None
            for attempt in range(_MAX_RETRIES):
                try:
                    await asyncio.to_thread(
                        worker_store.insert,
                        table_name=table_name,
                        content=f"# {header}: {sentence}",
                        metadata=metadata,
                        summarize=summarize,
                    )
                    last_exc = None
                    break  # success
                except Exception as e:
                    last_exc = e
                    delay = _RETRY_BASE_DELAY * (2 ** attempt)
                    tqdm.write(f"[Phase 6Q] Retry {attempt + 1}/{_MAX_RETRIES} for {file_name}/{header} in {delay:.0f}s — {e}")
                    await asyncio.sleep(delay)
                    worker_store = SupabaseVectorStore(embedding=Embedding())  # fresh connection

            if last_exc is None:
                open(done_marker, "w").close()
                results["done"] += 1
            else:
                results["error"] += 1
                tqdm.write(f"[Phase 6Q] FAILED {file_name} / {header}: {last_exc}")

            progress.update(1)
            progress.set_postfix(ok=results["done"], err=results["error"], refresh=False)

    workers = [asyncio.create_task(_worker()) for _ in range(max(1, concurrency))]
    await asyncio.gather(*workers)
    progress.close()
    print(f"[Phase 6Q] Done. {results['done']} inserted, {results['error']} failed.")

