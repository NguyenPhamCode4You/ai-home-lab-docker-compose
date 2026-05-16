"""
cia_phase1_index.py

Phase 1 — Codebase Indexing

Walks every .cs file in the codebase, extracts structural metadata via
CSharpFileAnalyzer, builds csharp_index.json, and populates the used_by
reverse-lookup map.

Idempotent: files already at phase >= 'indexed' in the manifest are skipped.
Checkpoints after every batch — a crash loses at most one batch of work.
"""

import asyncio
import datetime
import os
import re

from .cia_config import (
    CSHARP_CODEBASE_PATH,
    CSHARP_FOCUS_ONLY_FILES,
    CSHARP_IGNORE_FILES,
    CSHARP_LARGE_FILE_LINE_THRESHOLD,
    OPENROUTER_SYNTHESIS_MODEL,
    CLOUD_BATCH_DELAY,
    DEFAULT_INDEX_PATH,
    _load_index,
    _save_index,
)
from .agents.CSharpFileAnalyzer import CSharpFileAnalyzer, FALLBACK_RESULT
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_CODE_MODEL
from .CSharpManifest import CSharpManifest

# -------------------------------------------------------------------
# Phase-local helpers
# -------------------------------------------------------------------


def _matches_glob(rel_path: str, pattern: str) -> bool:
    """Check if a relative (forward-slash) path matches a glob pattern with ** support."""
    path = rel_path.replace("\\", "/")
    pat = pattern.replace("\\", "/")
    regex = re.escape(pat).replace(r"\*\*", ".*").replace(r"\*", "[^/]*").replace(r"\?", "[^/]")
    return bool(re.search(regex, path))


def _get_folder_priority(rel_path: str) -> int:
    """Return a sort key so Domain files are processed before Business, Infrastructure, etc."""
    p = rel_path.replace("\\", "/").lower()
    if "/domain/" in p or p.startswith("core/domain"):
        return 0
    if "/business/" in p or p.startswith("core/business"):
        return 1
    if "/infrastructure/" in p or p.startswith("core/infrastructure"):
        return 2
    if "/api" in p or "apis/" in p or "/controller" in p:
        return 3
    if "/externalclient" in p:
        return 4
    if "/function" in p or "/cronjob" in p:
        return 5
    return 6


def _select_analyzer_model(lines: int) -> object:
    """Return local Ollama for small files, OpenRouter cloud for large files."""
    if lines > CSHARP_LARGE_FILE_LINE_THRESHOLD:
        return OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL)
    return Ollama(model=OLLAMA_CODE_MODEL)


# -------------------------------------------------------------------
# Phase 1 — build_codebase_index
# -------------------------------------------------------------------


async def build_codebase_index(
    codebase_path: str = None,
    index_path: str = DEFAULT_INDEX_PATH,
    manifest: CSharpManifest = None,
    focus_patterns: list[str] = None,
    ignore_patterns: list[str] = None,
    checkpoint_every: int = 50,
    force_cloud: bool = False,
    force_local: bool = False,
    concurrency: int = 1,
):
    """
    Phase 1: Walk every .cs file in codebase_path, extract structural metadata via
    CSharpFileAnalyzer, build csharp_index.json, and populate the used_by reverse-lookup map.

    Filter precedence:
      - ignore_patterns (always applied, defaults to CSHARP_IGNORE_FILES env var)
      - focus_patterns  (when non-empty, ONLY matching files are processed)

    Processing order: Domain → Business → Infrastructure → API → ExternalClient → Functions.
    Checkpoints every `checkpoint_every` files so a crash loses minimal work.
    Idempotent: files already at phase >= 'indexed' in the manifest are skipped.
    """
    codebase_path = codebase_path or CSHARP_CODEBASE_PATH
    if not codebase_path or not os.path.isdir(codebase_path):
        print(f"[Phase 1] ERROR: codebase_path not found or not set: {codebase_path!r}")
        return

    if manifest is None:
        manifest = CSharpManifest()

    # Resolve filter pattern lists from arguments or env vars
    if focus_patterns is None:
        raw = CSHARP_FOCUS_ONLY_FILES.strip()
        focus_patterns = [p.strip() for p in raw.split(",") if p.strip()] if raw else []
    if ignore_patterns is None:
        raw = CSHARP_IGNORE_FILES.strip()
        ignore_patterns = [p.strip() for p in raw.split(",") if p.strip()]

    # --- Collect and filter .cs files ----------------------------------------
    all_cs_files: list[str] = []
    for root, _dirs, files in os.walk(codebase_path):
        for fname in files:
            if not fname.endswith(".cs"):
                continue
            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, codebase_path).replace("\\", "/")
            if any(_matches_glob(rel_path, p) for p in ignore_patterns):
                continue
            if focus_patterns and not any(_matches_glob(rel_path, p) for p in focus_patterns):
                continue
            all_cs_files.append(rel_path)

    all_cs_files.sort(key=_get_folder_priority)
    print(f"[Phase 1] Found {len(all_cs_files)} .cs files after filtering.")

    # --- Load or create index ------------------------------------------------
    if os.path.exists(index_path):
        index = _load_index(index_path)
    else:
        index = {"files": {}, "used_by": {}, "stats": {}}

    already_indexed = {"indexed", "documented", "enriched", "synthesized", "inserted"}
    to_process = [fp for fp in all_cs_files if manifest.get_phase(fp) not in already_indexed]
    print(f"[Phase 1] {len(to_process)} files need indexing ({len(all_cs_files) - len(to_process)} already indexed).")

    # --- Index each file (batched concurrently) ---------------------------------
    processed_count = 0
    effective_batch = max(1, concurrency)
    total = len(to_process)

    for batch_start in range(0, total, effective_batch):
        batch = to_process[batch_start : batch_start + effective_batch]

        async def _index_file(rel_path: str, slot: int):
            abs_path = os.path.join(codebase_path, rel_path.replace("/", os.sep))
            try:
                with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                    file_content = f.read()
            except Exception as exc:
                print(f"[Phase 1] SKIP (read error): {rel_path} — {exc}")
                return None

            lines = file_content.count("\n") + 1
            model = OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL) if force_cloud else (Ollama(model=OLLAMA_CODE_MODEL) if force_local else _select_analyzer_model(lines))
            model_name = model.model if hasattr(model, "model") else str(model)
            model_tag = "CLOUD" if isinstance(model, OpenRouter) else "LOCAL"
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[Phase 1] {ts} [{batch_start + slot + 1}/{total}] {model_tag} ({model_name}) — {rel_path} ({lines} lines)")

            analyzer = CSharpFileAnalyzer(llm_model=model)
            try:
                entry = await analyzer.analyze(file_content=file_content, rel_path=rel_path)
            except Exception as exc:
                print(f"[Phase 1] ERROR analyzing {rel_path}: {exc}")
                entry = dict(FALLBACK_RESULT)
                entry["class_name"] = re.sub(r"\.cs$", "", rel_path.split("/")[-1])

            file_hash = manifest.compute_hash(abs_path)
            return (rel_path, entry, file_hash, lines)

        results = await asyncio.gather(
            *[_index_file(fp, i) for i, fp in enumerate(batch)],
            return_exceptions=True,
        )

        for result in results:
            if result is None:
                continue
            if isinstance(result, Exception):
                print(f"[Phase 1] BATCH ERROR: {result}")
                continue
            rel_path, entry, file_hash, lines = result
            index["files"][rel_path] = entry
            manifest.set_phase(rel_path, "indexed", {
                "hash": file_hash,
                "lines": lines,
                "file_type": entry.get("file_type", "Other"),
                "architecture_layer": entry.get("architecture_layer", "Other"),
                "is_critical": entry.get("is_critical", False),
            })

        # Checkpoint after every batch — crash loses at most one batch of work.
        _save_index(index, index_path)
        manifest.save()

        processed_count += len(batch)
        if processed_count % checkpoint_every < effective_batch or processed_count >= total:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[Phase 1] {ts} Progress: {processed_count}/{total} files indexed.")

    # --- Build used_by reverse-lookup map (SKIPPED for speed) ----------------
    # NOTE: used_by reverse-scan is disabled. Re-enable if incremental dependent
    #       expansion is needed.
    used_by: dict[str, list[str]] = {}
    index["used_by"] = {}

    # --- Stats ---------------------------------------------------------------
    by_layer: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for entry in files_dict.values():
        by_layer[entry.get("architecture_layer", "Other")] = by_layer.get(entry.get("architecture_layer", "Other"), 0) + 1
        by_type[entry.get("file_type", "Other")] = by_type.get(entry.get("file_type", "Other"), 0) + 1

    index["stats"] = {
        "total_files": len(files_dict),
        "by_layer": by_layer,
        "by_type": by_type,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

    _save_index(index, index_path)
    manifest.save()

    print(f"[Phase 1] Complete. {len(files_dict)} files indexed (used_by scan skipped).")
    manifest.print_summary()
