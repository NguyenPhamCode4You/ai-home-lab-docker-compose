"""
cia_phase6_insert_quick.py

Phase 6 (Quick) — RAG Vector Store Insertion WITHOUT LLM calls.

Reads every chunk from the rag-chunks folder and inserts all of them
unconditionally. No resume / .done tracking — just a straight bulk load.
Re-running will re-insert everything (useful for table rebuilds).

Each chunk preserves full context:
  content  = "# {header}: {sentence}"
  metadata = file_name, section, folder_path, file_type, architecture_layer
  summarize = compact JSON from csharp-manifest.json, or first 600 chars of content

Concurrency: N workers each run embedding + DB insert via asyncio.to_thread
so blocking HTTP calls are genuinely parallel.
"""

import asyncio
import json
import os

from tqdm import tqdm

from .cia_config import DEFAULT_RAG_CHUNKS_FOLDER
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


def _build_quick_summary(file_name: str, header: str, folder_path: str, manifest_entry: dict | None, sentence: str) -> str:
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
    return sentence[:600]


async def insert_rag_chunks_quick(
    rag_chunks_folder: str = DEFAULT_RAG_CHUNKS_FOLDER,
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

            for header, section_content in split_markdown_header_and_content(content):
                header = header.strip().replace(":", "")
                sentence = remove_excessive_spacing(section_content)
                if not sentence or len(sentence) < 5:
                    continue
                all_chunks.append((file_name, header, sentence, folder_path))

    total = len(all_chunks)
    print(f"[Phase 6Q] {concurrency} parallel workers | table='{table_name}' | {total} chunks to insert")

    if total == 0:
        print("[Phase 6Q] No chunks found.")
        return

    # ── Queue + N workers ─────────────────────────────────────────────────────
    vector_store = SupabaseVectorStore(embedding=Embedding())
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

    async def _worker():
        while True:
            try:
                file_name, header, sentence, folder_path = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            try:
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

                await asyncio.to_thread(
                    vector_store.insert,
                    table_name=table_name,
                    content=f"# {header}: {sentence}",
                    metadata=metadata,
                    summarize=_build_quick_summary(file_name, header, folder_path, manifest_entry, sentence),
                )
                results["done"] += 1
            except Exception as e:
                results["error"] += 1
                tqdm.write(f"[Phase 6Q] ERROR {file_name} / {header}: {e}")
            finally:
                progress.update(1)
                progress.set_postfix(ok=results["done"], err=results["error"], refresh=False)

    workers = [asyncio.create_task(_worker()) for _ in range(max(1, concurrency))]
    await asyncio.gather(*workers)
    progress.close()
    print(f"[Phase 6Q] Done. {results['done']} inserted, {results['error']} failed.")

