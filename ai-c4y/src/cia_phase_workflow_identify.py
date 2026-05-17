"""
cia_phase_workflow_identify.py

Workflow Identification Phase — reverse-engineer the indexed codebase to
discover potentially critical/complex business workflows that are NOT already
captured in the hardcoded PRIORITY_CRITICAL_FLOWS config.

Algorithm:
  1. Load csharp_index.json + csharp-manifest.json
  2. Build a condensed per-module metadata view (class name, type, verb, entities,
     criticality flag) — small enough to fit in a single LLM context window
  3. Feed the condensed view + existing known flows (as exclusion list) to
     CSharpWorkflowIdentifier (LLM)
  4. Parse the JSON response; validate each candidate has the required fields
  5. Deduplicate against PRIORITY_CRITICAL_FLOWS by name (case-insensitive)
  6. Merge with any previously discovered flows and write to
     wip/discovered-workflows.json

Output format (same schema as PRIORITY_CRITICAL_FLOWS, plus extra fields):
  [
    {
      "name":            "WorkflowName",
      "module":          "VoyageManagement",
      "required_tokens": ["voyage", "estimate"],
      "any_tokens":      ["create", "convert"],
      "rationale":       "Creates a new voyage from a cost estimate — multi-step.",
      "source":          "discovered",
      "confidence":      0.9
    },
    ...
  ]

The discovered-workflows.json is then read by Phase 4 (synthesize_workflow_documents)
so that every identified flow automatically gets a Pass B deep-dive document on the
next synthesize run.
"""

import json
import os
import re

from .cia_config import (
    DEFAULT_INDEX_PATH,
    DEFAULT_DISCOVERED_WORKFLOWS_PATH,
    PRIORITY_CRITICAL_FLOWS,
    _load_index,
)
from .agents.CSharpWorkflowIdentifier import CSharpWorkflowIdentifier
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_GENERAL_MODEL
from .CSharpManifest import CSharpManifest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS = {"name", "module", "required_tokens", "any_tokens"}


def _build_module_metadata(files_dict: dict, manifest: CSharpManifest) -> dict[str, list[dict]]:
    """
    Condense csharp_index.json into a per-module list of compact file descriptors.

    Each descriptor is small enough that the whole codebase fits in ~4 000 tokens.
    """
    modules: dict[str, list[dict]] = {}
    for rel_path, entry in files_dict.items():
        # Only include files that have been at least indexed
        phase = manifest.get_phase(rel_path)
        if phase not in ("indexed", "documented", "enriched", "synthesized", "inserted"):
            continue

        class_name = entry.get("class_name", "") or os.path.splitext(os.path.basename(rel_path))[0]
        file_type = entry.get("file_type", "Other")
        arch_layer = entry.get("architecture_layer", "Other")
        verb = entry.get("handler_verb", "")
        entities = entry.get("entities_referenced", [])
        is_critical = entry.get("is_critical", False)

        # Module from path heuristic (same logic as phase 4)
        module = _detect_module(rel_path, entry.get("namespace", ""))

        descriptor: dict = {"class": class_name, "type": file_type, "layer": arch_layer}
        if verb:
            descriptor["verb"] = verb
        if is_critical:
            descriptor["critical"] = True
        if entities:
            descriptor["entities"] = entities[:6]  # cap at 6 to stay compact

        modules.setdefault(module, []).append(descriptor)

    return modules


def _detect_module(rel_path: str, namespace: str) -> str:
    """Infer domain module from file path or namespace (mirrors phase 4 logic)."""
    known = [
        "VoyageManagement", "MasterData", "Finance", "BunkerOrder",
        "OrderRequest", "UserManagement", "TaskAlert", "FileStorage", "ExternalClients",
    ]
    search = (rel_path + namespace).replace("\\", "/").lower()
    for mod in known:
        if mod.lower() in search:
            return mod
    return "General"


def _render_metadata_text(modules: dict[str, list[dict]], max_chars: int = 24_000) -> str:
    """
    Render the per-module metadata as a compact readable text block.

    Format per module:
        Module: VoyageManagement  (43 files)
          - CalculateVoyagePnLHandler  [Handler/Business]  verb=Calculate  critical  entities=[VoyagePnL,Voyage]
          - ...
    """
    lines = []
    total = 0
    for module, descriptors in sorted(modules.items()):
        header = f"\nModule: {module}  ({len(descriptors)} files)"
        lines.append(header)
        total += len(header)
        for d in descriptors:
            parts = [f"  - {d['class']}  [{d['type']}/{d['layer']}]"]
            if d.get("verb"):
                parts.append(f"verb={d['verb']}")
            if d.get("critical"):
                parts.append("critical")
            if d.get("entities"):
                parts.append(f"entities=[{','.join(d['entities'])}]")
            line = "  ".join(parts)
            if total + len(line) > max_chars:
                lines.append("  ... (truncated)")
                break
            lines.append(line)
            total += len(line)
    return "\n".join(lines)


def _build_exclusion_text(known_flows: list[dict]) -> str:
    """Format the known PRIORITY_CRITICAL_FLOWS as a simple list for the LLM exclusion list."""
    if not known_flows:
        return "(none)"
    return "\n".join(
        f"  - {f['name']} ({f.get('module', '?')}): "
        f"required={f.get('required_tokens', [])}, any={f.get('any_tokens', [])}"
        for f in known_flows
    )


def _load_existing_discovered(output_path: str) -> list[dict]:
    """Load previously discovered workflows if the file exists."""
    if not os.path.exists(output_path):
        return []
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [d for d in data if isinstance(d, dict)]
    except Exception:
        return []


def _deduplicate(candidates: list[dict], known_names: set[str]) -> list[dict]:
    """Remove candidates whose name (normalised) already exists in the known set."""
    seen: set[str] = set(known_names)
    unique = []
    for c in candidates:
        key = c.get("name", "").lower().replace("_", "").replace("-", "")
        if key and key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def _validate_candidate(c: dict) -> bool:
    """Return True if the candidate has all required fields with sensible types."""
    if not _REQUIRED_FIELDS.issubset(c.keys()):
        return False
    if not isinstance(c["required_tokens"], list) or not isinstance(c["any_tokens"], list):
        return False
    name = c.get("name", "")
    if not name or not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", name):
        return False
    return True


# ---------------------------------------------------------------------------
# Phase entry point
# ---------------------------------------------------------------------------


async def identify_critical_workflows(
    index_path: str = DEFAULT_INDEX_PATH,
    output_path: str = DEFAULT_DISCOVERED_WORKFLOWS_PATH,
    manifest: CSharpManifest = None,
    force_cloud: bool = False,
    force_local: bool = False,
    concurrency: int = 1,
):
    """
    Reverse-engineer the codebase index to discover new critical workflow candidates.

    Writes (or updates) `output_path` (wip/discovered-workflows.json).
    Phase 4 synthesize merges this file with PRIORITY_CRITICAL_FLOWS at runtime.
    """
    if manifest is None:
        manifest = CSharpManifest()

    if not os.path.exists(index_path):
        print(f"[Workflow-Identify] Index not found: {index_path}")
        print("[Workflow-Identify] Run --phase index first.")
        return

    print(f"[Workflow-Identify] Loading index from {index_path}...")
    index = _load_index(index_path)
    files_dict = index.get("files", {})
    print(f"[Workflow-Identify] {len(files_dict)} files in index.")

    # Build condensed metadata
    modules = _build_module_metadata(files_dict, manifest)
    total_eligible = sum(len(v) for v in modules.values())
    print(f"[Workflow-Identify] {total_eligible} indexed files across {len(modules)} module(s): {list(modules.keys())}")

    if total_eligible == 0:
        print("[Workflow-Identify] No indexed files found — run --phase index first.")
        return

    metadata_text = _render_metadata_text(modules)
    print(f"[Workflow-Identify] Condensed metadata: {len(metadata_text)} chars")

    # Build exclusion list from hardcoded + previously discovered
    existing_discovered = _load_existing_discovered(output_path)
    all_known = list(PRIORITY_CRITICAL_FLOWS) + existing_discovered
    exclusion_text = _build_exclusion_text(all_known)
    known_names = {f.get("name", "").lower().replace("_", "").replace("-", "") for f in all_known}

    print(f"[Workflow-Identify] Excluding {len(all_known)} already-known workflow(s).")

    # Choose LLM
    if force_local:
        llm = Ollama(model=OLLAMA_GENERAL_MODEL)
        print("[Workflow-Identify] Using Ollama (local).")
    else:
        from .agents.models.OpenRouter import OpenRouter as _OR
        model_name = os.getenv("CIA_OPENROUTER_CRITICAL_MODEL", "google/gemini-2.5-pro")
        llm = OpenRouter(model=model_name)
        print(f"[Workflow-Identify] Using OpenRouter ({model_name}).")

    identifier = CSharpWorkflowIdentifier(llm_model=llm)

    print("[Workflow-Identify] Calling LLM to identify workflow candidates...")
    raw_response = await identifier.run(
        context=metadata_text,
        question=exclusion_text,
    )

    candidates = identifier.parse_response(raw_response)
    print(f"[Workflow-Identify] LLM returned {len(candidates)} candidate(s).")

    # Validate and filter
    valid = [c for c in candidates if _validate_candidate(c)]
    invalid_count = len(candidates) - len(valid)
    if invalid_count:
        print(f"[Workflow-Identify] Dropped {invalid_count} invalid candidate(s) (bad schema).")

    # Deduplicate against all known flows
    new_candidates = _deduplicate(valid, known_names)
    print(f"[Workflow-Identify] {len(new_candidates)} genuinely new workflow(s) after deduplication.")

    # Annotate with source marker
    for c in new_candidates:
        c.setdefault("source", "discovered")

    # Merge with existing discovered (keep old, append new)
    merged = existing_discovered + new_candidates
    print(f"[Workflow-Identify] Total discovered workflows: {len(merged)} (was {len(existing_discovered)}, added {len(new_candidates)})")

    # Write output
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"[Workflow-Identify] Written to {output_path}")

    # Summary table
    if new_candidates:
        print("\n  New workflows discovered:")
        for c in new_candidates:
            print(f"    [{c.get('module','?')}] {c['name']} — {c.get('rationale', '')}")
    else:
        print("[Workflow-Identify] No new workflows found — index may not have changed since last run.")

    print("\n[Workflow-Identify] Done.")
