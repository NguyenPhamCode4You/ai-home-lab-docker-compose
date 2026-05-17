"""
cia_phase3_enrich.py

Phase 3 — Cross-reference Enrichment

Replaces the '# Impact Scope [PLACEHOLDER]' in every Phase 2 doc with a real
impact analysis and '# Used By' section via CSharpImpactAnalyzer.

Also scores each file for criticality and writes is_critical=True back to
both the manifest and csharp_index.json for files scoring >= 5.

Model selection:
  - combined input <= 6000 chars and not is_critical → local Ollama
  - combined input >  6000 chars or is_critical       → OpenRouter cloud

Idempotent: skips files already at phase="enriched".
"""

import asyncio
import json
import os
from datetime import datetime

from .cia_config import (
    OPENROUTER_SYNTHESIS_MODEL,
    CLOUD_BATCH_DELAY,
    BATCH_SIZE,
    DEFAULT_INDEX_PATH,
    DEFAULT_RAW_DOCS_FOLDER,
    DEFAULT_ENRICHED_FOLDER,
    _load_index,
    _save_index,
)
from .agents.CSharpImpactAnalyzer import CSharpImpactAnalyzer
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_GENERAL_MODEL
from .CSharpManifest import CSharpManifest

# -------------------------------------------------------------------
# Phase-local helpers
# -------------------------------------------------------------------


def _select_impact_model(combined_chars: int, is_critical: bool) -> object:
    """Return model for impact analysis based on input size and criticality."""
    if is_critical or combined_chars > 6000:
        return OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL)
    return Ollama(model=OLLAMA_GENERAL_MODEL)


def _build_caller_context(rel_path: str, index: dict, max_chars: int = 3000) -> str:
    """Build the caller list JSON for impact analysis."""
    files = index.get("files", {})
    entry = files.get(rel_path, {})
    class_name = entry.get("class_name", "")
    used_by = index.get("used_by", {}).get(class_name, [])
    callers = []
    for caller_path in used_by:
        ce = files.get(caller_path, {})
        callers.append({
            "file": caller_path,
            "class_name": ce.get("class_name"),
            "architecture_layer": ce.get("architecture_layer"),
            "file_type": ce.get("file_type"),
        })
    return json.dumps(callers, indent=2)[:max_chars]


def _score_criticality(entry: dict, used_by_count: int, impact_text: str) -> int:
    """Compute a criticality score per the Phase 3 rubric. Score >= 5 → is_critical=True."""
    score = 0
    name_lower = entry.get("class_name", "").lower()
    layer = entry.get("architecture_layer", "")
    verb = entry.get("handler_verb", "")
    file_type = entry.get("file_type", "")

    if used_by_count > 20:
        score += 3
    if layer == "Domain" and any(kw in name_lower for kw in ["voyage", "shipment", "estimate"]):
        score += 3
    if file_type == "Handler" and verb in ["Calculate", "Complete", "Create"]:
        score += 2
    if "Impact Rating:** Critical" in impact_text or "Impact Rating:** High" in impact_text:
        score += 2
    if any(kw in name_lower for kw in ["voyage", "estimate", "profitandloss", "calculate", "finance", "payment"]):
        score += 1
    return score


# -------------------------------------------------------------------
# Phase 3 — enrich_with_cross_references
# -------------------------------------------------------------------


async def enrich_with_cross_references(
    raw_folder: str = DEFAULT_RAW_DOCS_FOLDER,
    enriched_folder: str = DEFAULT_ENRICHED_FOLDER,
    index_path: str = DEFAULT_INDEX_PATH,
    manifest: CSharpManifest = None,
    batch_size: int = BATCH_SIZE,
    force_cloud: bool = False,
    force_local: bool = False,
    concurrency: int = 1,
):
    """
    Phase 3: Replace the '# Impact Scope [PLACEHOLDER]' in every Phase 2 doc
    with a real impact analysis and '# Used By' section.

    Also scores each file for criticality and writes is_critical=True back to
    both the manifest and csharp_index.json for files scoring >= 5.

    Model selection:
      - combined input <= 6000 chars and not is_critical → local Ollama
      - combined input >  6000 chars or is_critical       → OpenRouter cloud
    """
    if manifest is None:
        manifest = CSharpManifest()
    index = _load_index(index_path)
    files_dict = index.get("files", {})

    to_process = manifest.get_all_at_phase("documented")
    total = len(to_process)
    print(f"[Phase 3] {total} files to enrich.")

    critical_count = 0
    manifest_lock = asyncio.Lock()

    effective_batch = max(1, concurrency) if (force_cloud or force_local) else batch_size
    for batch_start in range(0, total, effective_batch):
        batch = to_process[batch_start : batch_start + effective_batch]
        used_cloud_this_batch = False

        async def _enrich_file(rel_path: str, file_idx: int):
            nonlocal used_cloud_this_batch, critical_count

            rel_md = os.path.splitext(rel_path)[0] + ".md"
            raw_doc_path = os.path.join(raw_folder, rel_md)
            if not os.path.exists(raw_doc_path):
                print(f"[Phase 3] SKIP (no raw doc): {rel_path}")
                return

            with open(raw_doc_path, "r", encoding="utf-8") as f:
                doc_content = f.read()

            entry = files_dict.get(rel_path, {})
            is_critical = entry.get("is_critical", False)
            caller_context = _build_caller_context(rel_path, index)
            combined_chars = len(doc_content) + len(caller_context)

            model = OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL) if force_cloud else (Ollama(model=OLLAMA_GENERAL_MODEL) if force_local else _select_impact_model(combined_chars, is_critical))
            ts = datetime.now().strftime("%H:%M:%S")
            if isinstance(model, OpenRouter):
                used_cloud_this_batch = True
                print(f"[Phase 3] {ts} [{file_idx}/{total}] CLOUD — {rel_path} ({combined_chars} chars)")
            else:
                print(f"[Phase 3] {ts} [{file_idx}/{total}] LOCAL — {rel_path} ({combined_chars} chars)")

            analyzer = CSharpImpactAnalyzer(llm_model=model)
            try:
                impact_text = await analyzer.run(context=doc_content, question=caller_context)
            except Exception as exc:
                print(f"[Phase 3] ERROR analyzing {rel_path}: {exc}")
                return

            # Replace placeholder (or append if not found)
            placeholder = "# Impact Scope\n[PLACEHOLDER — will be filled in Phase 3]"
            if placeholder in doc_content:
                enriched_content = doc_content.replace(placeholder, impact_text.strip())
            else:
                enriched_content = doc_content.rstrip() + "\n\n" + impact_text.strip()

            out_path = os.path.join(enriched_folder, rel_md)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as out_file:
                out_file.write(enriched_content)

            # Score and flag criticality
            used_by_count = len(index.get("used_by", {}).get(entry.get("class_name", ""), []))
            score = _score_criticality(entry, used_by_count, impact_text)
            if score >= 5 and not is_critical:
                print(f"[Phase 3] CRITICAL: {rel_path} (score={score})")
                files_dict[rel_path]["is_critical"] = True
                critical_count += 1

            manifest.set_phase(
                rel_path,
                "enriched",
                {
                    "enriched_doc_path": out_path,
                    "is_critical": files_dict.get(rel_path, {}).get("is_critical", False),
                },
            )
            async with manifest_lock:
                manifest.save()
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Phase 3] {ts} [{file_idx}/{total}] DONE: {rel_path}")

        await asyncio.gather(*[_enrich_file(p, batch_start + i + 1) for i, p in enumerate(batch)])
        manifest.save()

        if used_cloud_this_batch and batch_start + effective_batch < total:
            print(f"[Phase 3] Sleeping {CLOUD_BATCH_DELAY}s...")
            await asyncio.sleep(CLOUD_BATCH_DELAY)

    # Persist is_critical flags back into the index
    index["files"] = files_dict
    _save_index(index, index_path)
    manifest.save()
    print(f"[Phase 3] Complete. {critical_count} newly flagged critical files.")
