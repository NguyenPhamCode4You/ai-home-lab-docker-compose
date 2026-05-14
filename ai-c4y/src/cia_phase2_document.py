"""
cia_phase2_document.py

Phase 2 — Per-file Documentation

For every .cs file at phase="indexed", generate a structured markdown document
via CSharpDocumentWriter.

Model selection:
  - <= CIA_LARGE_FILE_THRESHOLD lines, not critical, <= 5 injected services → Ollama (fast)
  - Otherwise → OpenRouter cloud

Output: wip/csharp-docs/raw/{relative_cs_path}.md
Idempotent: skips files already at phase="documented".
"""

import asyncio
import json
import os

from .cia_config import (
    CSHARP_LARGE_FILE_LINE_THRESHOLD,
    OPENROUTER_SYNTHESIS_MODEL,
    CLOUD_BATCH_DELAY,
    BATCH_SIZE,
    DEFAULT_INDEX_PATH,
    DEFAULT_RAW_DOCS_FOLDER,
    LAYER_PRIORITY,
    _load_index,
)
from .agents.CSharpDocumentWriter import CSharpDocumentWriter
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_CODE_MODEL
from .CSharpManifest import CSharpManifest

# -------------------------------------------------------------------
# Phase-local helpers
# -------------------------------------------------------------------


def _select_doc_writer_model(lines: int, injected_services_count: int, is_critical: bool) -> object:
    """Return local Ollama or cloud OpenRouter based on file characteristics."""
    if is_critical or lines > CSHARP_LARGE_FILE_LINE_THRESHOLD or injected_services_count > 5:
        return OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL)
    return Ollama(model=OLLAMA_CODE_MODEL)


def _layer_sort_key(entry: dict) -> int:
    return LAYER_PRIORITY.get(entry.get("architecture_layer", "Other"), 7)


def _build_index_context(rel_path: str, index: dict, max_chars: int = 2000) -> str:
    """Build a concise index context string to accompany the file content."""
    files = index.get("files", {})
    entry = files.get(rel_path, {})
    if not entry:
        return ""
    class_name = entry.get("class_name", "")
    used_by = index.get("used_by", {}).get(class_name, [])[:10]
    ctx = {
        "file_type": entry.get("file_type"),
        "architecture_layer": entry.get("architecture_layer"),
        "namespace": entry.get("namespace"),
        "injected_services": entry.get("injected_services", []),
        "entities_referenced": entry.get("entities_referenced", []),
        "external_clients_used": entry.get("external_clients_used", []),
        "known_callers_top10": used_by,
    }
    return json.dumps(ctx, indent=2)[:max_chars]


# -------------------------------------------------------------------
# Phase 2 — write_csharp_documents
# -------------------------------------------------------------------


async def write_csharp_documents(
    codebase_path: str,
    index_path: str = DEFAULT_INDEX_PATH,
    output_folder: str = DEFAULT_RAW_DOCS_FOLDER,
    manifest: CSharpManifest = None,
    batch_size: int = BATCH_SIZE,
    force_cloud: bool = False,
    force_local: bool = False,
    concurrency: int = 1,
):
    """
    Phase 2: For every .cs file at phase="indexed", generate a structured markdown document.

    Model selection:
      - <= CSHARP_LARGE_FILE_LINE_THRESHOLD lines  → local Ollama (fast)
      - >  threshold lines, is_critical, or > 5 injected services → OpenRouter cloud

    Output path: output_folder/{relative_cs_path_without_ext}.md
    Idempotent: skips files already at phase="documented".
    """
    if manifest is None:
        manifest = CSharpManifest()
    index = _load_index(index_path)
    files_dict = index.get("files", {})

    to_process = [p for p in files_dict if manifest.get_phase(p) == "indexed"]
    to_process.sort(key=lambda p: _layer_sort_key(files_dict.get(p, {})))

    total = len(to_process)
    print(f"[Phase 2] {total} files to document.")

    effective_batch = max(1, concurrency) if (force_cloud or force_local) else batch_size
    for batch_start in range(0, total, effective_batch):
        batch = to_process[batch_start : batch_start + effective_batch]
        used_cloud_this_batch = False

        async def _doc_file(rel_path: str):
            nonlocal used_cloud_this_batch

            abs_path = os.path.join(codebase_path, rel_path.replace("/", os.sep))
            if not os.path.exists(abs_path):
                print(f"[Phase 2] SKIP (not found): {rel_path}")
                return

            try:
                with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                    file_content = f.read()
            except Exception as exc:
                print(f"[Phase 2] SKIP (read error): {rel_path} — {exc}")
                return

            lines = file_content.count("\n") + 1
            entry = files_dict.get(rel_path, {})
            injected_count = len(entry.get("injected_services", []))
            is_critical = entry.get("is_critical", False)

            model = OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL) if force_cloud else (Ollama(model=OLLAMA_CODE_MODEL) if force_local else _select_doc_writer_model(lines, injected_count, is_critical))
            if isinstance(model, OpenRouter):
                used_cloud_this_batch = True
                print(f"[Phase 2] CLOUD — {rel_path} ({lines} lines)")
            else:
                print(f"[Phase 2] LOCAL — {rel_path} ({lines} lines)")

            writer = CSharpDocumentWriter(llm_model=model)
            index_context = _build_index_context(rel_path, index)

            rel_md = os.path.splitext(rel_path)[0] + ".md"
            out_path = os.path.join(output_folder, rel_md)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            # Idempotency guard
            if os.path.exists(out_path) and manifest.get_phase(rel_path) == "documented":
                print(f"[Phase 2] SKIP (already documented): {rel_path}")
                return

            try:
                with open(out_path, "w", encoding="utf-8") as out_file:
                    async for chunk in writer.stream(context=file_content, question=index_context):
                        print(chunk, end="", flush=True)
                        out_file.write(chunk)
                        out_file.flush()
                manifest.set_phase(rel_path, "documented", {"doc_path": out_path, "lines": lines})
                print(f"\n[Phase 2] DONE: {rel_path}")
            except Exception as exc:
                print(f"[Phase 2] ERROR: {rel_path} — {exc}")

        await asyncio.gather(*[_doc_file(p) for p in batch])
        manifest.save()

        if used_cloud_this_batch and batch_start + effective_batch < total:
            print(f"[Phase 2] Sleeping {CLOUD_BATCH_DELAY}s (cloud rate-limit guard)...")
            await asyncio.sleep(CLOUD_BATCH_DELAY)

    manifest.save()
    print(f"[Phase 2] Complete. {total} files processed.")
