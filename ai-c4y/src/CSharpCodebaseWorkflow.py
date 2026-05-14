"""
CSharpCodebaseWorkflow.py

Master workflow module for the BVMS C# codebase RAG pipeline.
Each method corresponds to one pipeline phase.

Phase 1 — build_codebase_index()          → walks .cs files, extracts metadata, builds index
Phase 2 — write_csharp_documents()        → generates per-file markdown docs
Phase 3 — enrich_with_cross_references()  → adds Impact Scope + Used By sections
Phase 4 — synthesize_workflow_documents() → produces workflow + critical deep-dive docs
"""

import asyncio
import datetime
import json
import os
import re

from dotenv import load_dotenv

from .agents.CSharpFileAnalyzer import CSharpFileAnalyzer, FALLBACK_RESULT
from .agents.CSharpDocumentWriter import CSharpDocumentWriter
from .agents.CSharpImpactAnalyzer import CSharpImpactAnalyzer
from .agents.CSharpWorkflowSynthesizer import CSharpWorkflowSynthesizer
from .agents.CSharpCriticalWorkflowAnalyzer import CSharpCriticalWorkflowAnalyzer
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_CODE_MODEL, OLLAMA_GENERAL_MODEL
from .CSharpManifest import CSharpManifest

load_dotenv()

# -------------------------------------------------------------------
# Configuration from env
# -------------------------------------------------------------------

CSHARP_CODEBASE_PATH            = os.getenv("CODE_IMPACT_ANALYZER_CODEBASE_PATH", "")
CSHARP_FOCUS_ONLY_FILES         = os.getenv("CODE_IMPACT_ANALYZER_FOCUS_ONLY_FILES", "")
CSHARP_IGNORE_FILES             = os.getenv(
    "CODE_IMPACT_ANALYZER_IGNORE_FILES",
    "**/Migrations/**,**/*.Designer.cs,**/obj/**,**/bin/**",
)
CSHARP_LARGE_FILE_LINE_THRESHOLD = int(os.getenv("CODE_IMPACT_ANALYZER_LARGE_FILE_THRESHOLD", 200))
OPENROUTER_SYNTHESIS_MODEL = os.getenv("CODE_IMPACT_ANALYZER_SYNTHESIS_MODEL", "qwen/qwen3-32b")
OPENROUTER_CRITICAL_MODEL = os.getenv("CODE_IMPACT_ANALYZER_CRITICAL_MODEL", "google/gemini-2.5-pro")
CLOUD_BATCH_DELAY = float(os.getenv("CODE_IMPACT_ANALYZER_CLOUD_BATCH_DELAY", "2.0"))
BATCH_SIZE = int(os.getenv("CODE_IMPACT_ANALYZER_BATCH_SIZE", "10"))

# Output folder defaults — all scoped under wip/ for easy management
DEFAULT_INDEX_PATH       = os.getenv("CODE_IMPACT_ANALYZER_INDEX_PATH",            "wip/csharp-index.json")
DEFAULT_RAW_DOCS_FOLDER  = os.getenv("CODE_IMPACT_ANALYZER_RAW_DOCS_FOLDER",       "wip/csharp-docs/raw")
DEFAULT_ENRICHED_FOLDER  = os.getenv("CODE_IMPACT_ANALYZER_ENRICHED_DOCS_FOLDER",  "wip/csharp-docs/enriched")
DEFAULT_WORKFLOWS_FOLDER = os.getenv("CODE_IMPACT_ANALYZER_WORKFLOWS_FOLDER",      "wip/csharp-docs/workflows")

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

# Architecture layers ordered by processing priority (Domain first)
LAYER_PRIORITY = {
    "Domain": 0,
    "Business": 1,
    "Infrastructure": 2,
    "API": 3,
    "ExternalClient": 4,
    "Functions": 5,
    "CronJobs": 6,
    "Other": 7,
}

# Handler verb → verb-cluster mapping for workflow grouping
VERB_CLUSTERS = {
    "ReadFlows": ["get", "search", "find", "list", "query", "fetch", "load"],
    "WriteFlows": ["create", "update", "delete", "add", "remove", "set", "save"],
    "CalculationFlows": ["calculate", "compute", "estimate", "evaluate", "recalculate"],
    "TransitionFlows": ["complete", "approve", "cancel", "send", "submit", "confirm", "close", "reopen"],
    "SyncFlows": ["sync", "import", "export", "migrate", "refresh", "transfer"],
}

# Priority critical flows for Phase 4 Pass B — always deep-dived regardless of scoring.
#
# Matching uses token-set logic on the CamelCase-tokenized class name + file path:
#   required_tokens  — ALL must be present (narrows scope)
#   any_tokens       — AT LEAST ONE must be present (identifies the flow)
# This is resilient to naming variations like:
#   CalculateVoyagePnLCommandHandler / VoyagePnLCalculator / GetVoyageProfitQuery
PRIORITY_CRITICAL_FLOWS = [
    {
        "name": "CalculateVoyagePnL",
        "module": "VoyageManagement",
        "required_tokens": ["calculate"],
        "any_tokens": ["pnl", "profit", "voyage", "estimate"],
    },
    {
        "name": "CreateVoyageFromEstimate",
        "module": "VoyageManagement",
        "required_tokens": ["voyage", "estimate"],
        "any_tokens": ["create", "from", "transition", "convert"],
    },
    {
        "name": "VoyageLifecycle",
        "module": "VoyageManagement",
        "required_tokens": ["voyage"],
        "any_tokens": ["complete", "cancel", "close", "lifecycle", "finalize", "reopen"],
    },
    {
        "name": "BunkerCostCalculation",
        "module": "BunkerOrder",
        "required_tokens": ["bunker"],
        "any_tokens": ["cost", "calculate", "order", "price", "qty", "quantity"],
    },
    {
        "name": "CommissionPayment",
        "module": "Finance",
        "required_tokens": [],
        "any_tokens": ["commission", "payment", "invoice", "settlement", "receivable", "payable"],
    },
    {
        "name": "ETSEmissions",
        "module": "Finance",
        "required_tokens": [],
        "any_tokens": ["ets", "emission", "carbon", "ghg", "greenhouse", "eu"],
    },
]

# -------------------------------------------------------------------
# Internal helpers
# -------------------------------------------------------------------


def _tokenize_identifier(text: str) -> set[str]:
    """Split a CamelCase class name or file path into a set of lowercase word tokens.

    Examples::
        CreateVoyageFromEstimate  → {create, voyage, from, estimate}
        VoyagePnLCalculator       → {voyage, pn, l, calculator}  (acronyms split per char)
        BBC.VoyageManagement/...  → includes all path segments
    """
    # Split CamelCase: ABCDef → ABC Def, camelCase → camel Case
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)
    spaced = re.sub(r'([a-z\d])([A-Z])', r'\1 \2', spaced)
    tokens = re.split(r'[^a-zA-Z0-9]+', spaced)
    return {t.lower() for t in tokens if len(t) > 1}


def _load_index(index_path: str) -> dict:
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_index(index: dict, index_path: str):
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def _select_doc_writer_model(lines: int, injected_services_count: int, is_critical: bool) -> object:
    """Return local Ollama or cloud OpenRouter based on file characteristics."""
    if is_critical or lines > CSHARP_LARGE_FILE_LINE_THRESHOLD or injected_services_count > 5:
        return OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL)
    return Ollama(model=OLLAMA_CODE_MODEL)


def _select_impact_model(combined_chars: int, is_critical: bool) -> object:
    """Return model for impact analysis based on input size and criticality."""
    if is_critical or combined_chars > 6000:
        return OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL)
    return Ollama(model=OLLAMA_GENERAL_MODEL)


def _layer_sort_key(entry: dict) -> int:
    return LAYER_PRIORITY.get(entry.get("architecture_layer", "Other"), 7)


def _detect_module(rel_path: str, namespace: str) -> str:
    """Infer domain module from file path or namespace."""
    modules = [
        "VoyageManagement", "MasterData", "Finance", "BunkerOrder",
        "OrderRequest", "UserManagement", "TaskAlert", "FileStorage", "ExternalClients",
    ]
    search = (rel_path + namespace).replace("\\", "/").lower()
    for mod in modules:
        if mod.lower() in search:
            return mod
    return "General"


def _detect_verb_cluster(class_name: str, handler_verb: str) -> str:
    """Map a class name / handler verb to the appropriate verb cluster."""
    name = (class_name + handler_verb).lower()
    for cluster, verbs in VERB_CLUSTERS.items():
        for verb in verbs:
            if name.startswith(verb) or verb in name:
                return cluster
    return "WriteFlows"


def _build_index_context(rel_path: str, index: dict, max_chars: int = 2000) -> str:
    """Build a concise index context string to accompany the file content in Phase 2."""
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


def _build_caller_context(rel_path: str, index: dict, max_chars: int = 3000) -> str:
    """Build the caller list JSON for Phase 3 impact analysis."""
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


def _load_enriched_docs_concat(file_paths: list, enriched_folder: str, max_chars: int) -> str:
    """Concatenate enriched markdown docs for a cluster, respecting the char cap."""
    parts = []
    total = 0
    for rel_path in file_paths:
        rel_md = os.path.splitext(rel_path)[0] + ".md"
        doc_path = os.path.join(enriched_folder, rel_md)
        if not os.path.exists(doc_path):
            continue
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        header = f"\n\n---\n## File: {rel_path}\n\n"
        chunk = header + content
        if total + len(chunk) > max_chars:
            remaining = max_chars - total
            if remaining > 500:
                parts.append(chunk[:remaining])
            break
        parts.append(chunk)
        total += len(chunk)
    return "".join(parts)


def _detect_cross_domain_files(files_dict: dict) -> list[str]:
    """
    Heuristic: files that reference entity classes from two or more domain modules
    are considered cross-domain and get their own synthesis cluster.
    """
    module_keywords = ["voyage", "estimate", "bunker", "finance", "masterdata", "orderrequest"]
    cross_domain = []
    for rel_path, entry in files_dict.items():
        name_lower = entry.get("class_name", "").lower()
        refs_lower = " ".join(entry.get("entities_referenced", [])).lower()
        hits = sum(1 for kw in module_keywords if kw in refs_lower)
        if hits >= 2 or "fromestimate" in name_lower or "fromvoyage" in name_lower:
            cross_domain.append(rel_path)
    return cross_domain


def _collect_pass_b_targets(
    files_dict: dict,
    enriched_folder: str,
    critical_clusters: dict,
) -> list[dict]:
    """
    Build the list of Pass B deep-dive targets:
      1. Hard-coded priority flows (always included)
      2. Any critical cluster not already covered by a priority flow
    """
    targets = []
    seen_flow_names: set[str] = set()

    # Hard-coded priority flows first
    for flow_def in PRIORITY_CRITICAL_FLOWS:
        flow_name = flow_def["name"]
        module = flow_def["module"]
        required = flow_def.get("required_tokens", [])
        any_of = flow_def.get("any_tokens", [])

        matching_paths = []
        for rel_path, entry in files_dict.items():
            tokens = _tokenize_identifier(entry.get("class_name", "") + " " + rel_path)
            required_match = all(t in tokens for t in required)
            any_match = (not any_of) or any(t in tokens for t in any_of)
            if required_match and any_match:
                rel_md = os.path.splitext(rel_path)[0] + ".md"
                if os.path.exists(os.path.join(enriched_folder, rel_md)):
                    matching_paths.append(rel_path)

        if matching_paths:
            targets.append({"flow_name": flow_name, "module": module, "file_paths": matching_paths})
            seen_flow_names.add(flow_name)

    # Additional critical clusters
    for cluster_key, file_paths in critical_clusters.items():
        module, verb_cluster = cluster_key.split("|", 1)
        flow_name = f"{module}_{verb_cluster}"
        if flow_name not in seen_flow_names:
            targets.append({"flow_name": flow_name, "module": module, "file_paths": file_paths})

    return targets


async def _synthesize_architecture_overview(
    workflows_folder: str,
    workflow_summaries: list[str],
):
    """Final Phase 4 synthesis: produce BVMS_Architecture_Overview.md."""
    output_path = os.path.join(workflows_folder, "BVMS_Architecture_Overview.md")
    if os.path.exists(output_path):
        print("[Phase 4] SKIP (exists): BVMS_Architecture_Overview.md")
        return

    summaries_text = "\n\n---\n".join(workflow_summaries[:40])

    overview_template = """
You are a principal .NET architect summarizing the entire BVMS (BBC Voyager Management System) codebase.
Below are condensed summaries of all identified business workflow documents in the system.

{context}

Generate a high-level architecture overview document with EXACTLY these sections:

---

# BVMS System Architecture Overview

## System Purpose
What is BVMS? What shipping/voyage management business domain does it serve?
2–3 sentences.

## Business Capabilities
Numbered list of every major capability the system provides (at least one per discovered module).

## Module Overview
For each module listed below, write one paragraph on its purpose and key operations:
- VoyageManagement
- Finance
- BunkerOrder
- MasterData
- OrderRequest
- UserManagement
- ExternalClients

## Module Interconnections
How do the modules interact with each other? Which modules depend on others?

```mermaid
graph TD
    VoyageManagement --> Finance
    VoyageManagement --> BunkerOrder
    VoyageManagement --> MasterData
    ...
```

(Complete the diagram based on what you found in the workflow summaries.)

## Critical Business Flows

| Flow | Module | Complexity | Deep-Dive Doc |
|---|---|---|---|
| CreateVoyageFromEstimate | VoyageManagement | High | VoyageManagement/CreateVoyageFromEstimate_CRITICAL_deep_dive.md |
| CalculateVoyagePnL | VoyageManagement | Critical | VoyageManagement/CalculateVoyagePnL_CRITICAL_deep_dive.md |
| ... | ... | ... | ... |

(Fill in the table based on all deep-dive docs that were generated.)

## Development Guidelines Summary
5 key architectural conventions a new developer must know before contributing to BVMS:
1. ...
2. ...
3. ...
4. ...
5. ...
    """

    synthesizer = CSharpWorkflowSynthesizer(
        llm_model=OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL),
        instruction_template=overview_template,
    )
    print("[Phase 4] Synthesizing BVMS_Architecture_Overview.md...")
    try:
        with open(output_path, "w", encoding="utf-8") as out_file:
            async for chunk in synthesizer.stream(context=summaries_text, question="BVMS System Overview"):
                print(chunk, end="", flush=True)
                out_file.write(chunk)
                out_file.flush()
        print(f"\n[Phase 4] DONE: {output_path}")
    except Exception as e:
        print(f"[Phase 4] ERROR synthesizing architecture overview: {e}")


# -------------------------------------------------------------------
# Phase 1 — Codebase indexing
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


async def build_codebase_index(
    codebase_path: str = None,
    index_path: str = DEFAULT_INDEX_PATH,
    manifest: CSharpManifest = None,
    focus_patterns: list[str] = None,
    ignore_patterns: list[str] = None,
    checkpoint_every: int = 50,
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

    # --- Index each file ------------------------------------------------------
    processed_count = 0
    for rel_path in to_process:
        abs_path = os.path.join(codebase_path, rel_path.replace("/", os.sep))
        try:
            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                file_content = f.read()
        except Exception as exc:
            print(f"[Phase 1] SKIP (read error): {rel_path} — {exc}")
            continue

        lines = file_content.count("\n") + 1
        model = _select_analyzer_model(lines)
        model_tag = "CLOUD" if isinstance(model, OpenRouter) else "LOCAL"
        print(f"[Phase 1] {model_tag} — {rel_path} ({lines} lines)")

        analyzer = CSharpFileAnalyzer(llm_model=model)
        try:
            entry = await analyzer.analyze(file_content=file_content, rel_path=rel_path)
        except Exception as exc:
            print(f"[Phase 1] ERROR analyzing {rel_path}: {exc}")
            entry = dict(FALLBACK_RESULT)
            entry["class_name"] = re.sub(r"\.cs$", "", rel_path.split("/")[-1])

        file_hash = manifest.compute_hash(abs_path)
        index["files"][rel_path] = entry
        manifest.set_phase(rel_path, "indexed", {
            "hash": file_hash,
            "lines": lines,
            "file_type": entry.get("file_type", "Other"),
            "architecture_layer": entry.get("architecture_layer", "Other"),
            "is_critical": entry.get("is_critical", False),
        })

        processed_count += 1
        if processed_count % checkpoint_every == 0:
            print(f"[Phase 1] Checkpoint: {processed_count}/{len(to_process)} files indexed...")
            _save_index(index, index_path)
            manifest.save()

    # --- Build used_by reverse-lookup map ------------------------------------
    print("[Phase 1] Building used_by reverse-lookup map...")
    used_by: dict[str, list[str]] = {}
    files_dict = index["files"]

    class_names = {
        entry.get("class_name"): rel_path
        for rel_path, entry in files_dict.items()
        if entry.get("class_name")
    }

    for scan_path in all_cs_files:
        abs_scan = os.path.join(codebase_path, scan_path.replace("/", os.sep))
        try:
            with open(abs_scan, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue
        for class_name, source_path in class_names.items():
            if source_path == scan_path:
                continue
            if re.search(rf"\b{re.escape(class_name)}\b", content):
                bucket = used_by.setdefault(class_name, [])
                if scan_path not in bucket:
                    bucket.append(scan_path)

    index["used_by"] = used_by

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

    total_used_by = sum(len(v) for v in used_by.values())
    print(f"[Phase 1] Complete. {len(files_dict)} files indexed, {total_used_by} used_by relationships found.")
    manifest.print_summary()


# -------------------------------------------------------------------
# Phase 2 — Per-file documentation
# -------------------------------------------------------------------


async def write_csharp_documents(
    codebase_path: str,
    index_path: str = DEFAULT_INDEX_PATH,
    output_folder: str = DEFAULT_RAW_DOCS_FOLDER,
    manifest: CSharpManifest = None,
    batch_size: int = BATCH_SIZE,
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

    for batch_start in range(0, total, batch_size):
        batch = to_process[batch_start : batch_start + batch_size]
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

            model = _select_doc_writer_model(lines, injected_count, is_critical)
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

        if used_cloud_this_batch and batch_start + batch_size < total:
            print(f"[Phase 2] Sleeping {CLOUD_BATCH_DELAY}s (cloud rate-limit guard)...")
            await asyncio.sleep(CLOUD_BATCH_DELAY)

    manifest.save()
    print(f"[Phase 2] Complete. {total} files processed.")


# -------------------------------------------------------------------
# Phase 3 — Cross-reference enrichment
# -------------------------------------------------------------------


async def enrich_with_cross_references(
    raw_folder: str = DEFAULT_RAW_DOCS_FOLDER,
    enriched_folder: str = DEFAULT_ENRICHED_FOLDER,
    index_path: str = DEFAULT_INDEX_PATH,
    manifest: CSharpManifest = None,
    batch_size: int = BATCH_SIZE,
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

    for batch_start in range(0, total, batch_size):
        batch = to_process[batch_start : batch_start + batch_size]
        used_cloud_this_batch = False

        async def _enrich_file(rel_path: str):
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

            model = _select_impact_model(combined_chars, is_critical)
            if isinstance(model, OpenRouter):
                used_cloud_this_batch = True
                print(f"[Phase 3] CLOUD — {rel_path} ({combined_chars} chars)")
            else:
                print(f"[Phase 3] LOCAL — {rel_path} ({combined_chars} chars)")

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
            print(f"[Phase 3] DONE: {rel_path}")

        await asyncio.gather(*[_enrich_file(p) for p in batch])
        manifest.save()

        if used_cloud_this_batch and batch_start + batch_size < total:
            print(f"[Phase 3] Sleeping {CLOUD_BATCH_DELAY}s...")
            await asyncio.sleep(CLOUD_BATCH_DELAY)

    # Persist is_critical flags back into the index
    index["files"] = files_dict
    _save_index(index, index_path)
    manifest.save()
    print(f"[Phase 3] Complete. {critical_count} newly flagged critical files.")


# -------------------------------------------------------------------
# Phase 4 — Workflow synthesis
# -------------------------------------------------------------------


async def synthesize_workflow_documents(
    enriched_folder: str = DEFAULT_ENRICHED_FOLDER,
    workflows_folder: str = DEFAULT_WORKFLOWS_FOLDER,
    index_path: str = DEFAULT_INDEX_PATH,
    manifest: CSharpManifest = None,
):
    """
    Phase 4: Two-pass workflow synthesis.

    Pass A — Domain module flow docs (one per module × verb cluster)
    Pass B — Critical workflow deep dives (priority flows + is_critical clusters)
    Final  — BVMS_Architecture_Overview.md from all workflow summaries

    All synthesis uses cloud models exclusively.
    """
    if manifest is None:
        manifest = CSharpManifest()
    index = _load_index(index_path)
    files_dict = index.get("files", {})
    os.makedirs(workflows_folder, exist_ok=True)

    # ----------------------------------------------------------------
    # Build cluster map
    # ----------------------------------------------------------------
    # clusters[module][verb_cluster] = [rel_paths]
    clusters: dict[str, dict[str, list]] = {}
    # critical_clusters["module|verb_cluster"] = [rel_paths with is_critical=True]
    critical_clusters: dict[str, list] = {}

    for rel_path, entry in files_dict.items():
        phase = manifest.get_phase(rel_path)
        if phase not in ("enriched", "synthesized", "inserted"):
            continue
        module = _detect_module(rel_path, entry.get("namespace", ""))
        verb_cluster = _detect_verb_cluster(
            entry.get("class_name", ""), entry.get("handler_verb", "")
        )
        clusters.setdefault(module, {}).setdefault(verb_cluster, []).append(rel_path)

        if entry.get("is_critical", False):
            key = f"{module}|{verb_cluster}"
            critical_clusters.setdefault(key, []).append(rel_path)

    # ----------------------------------------------------------------
    # Pass A — module flow docs
    # ----------------------------------------------------------------
    print(f"[Phase 4 Pass A] Modules: {list(clusters.keys())}")
    workflow_summaries: list[str] = []

    for module, verb_groups in clusters.items():
        module_folder = os.path.join(workflows_folder, module)
        os.makedirs(module_folder, exist_ok=True)

        for verb_cluster, file_paths in verb_groups.items():
            cluster_label = f"{module} — {verb_cluster}"
            output_path = os.path.join(module_folder, f"{verb_cluster}_workflow.md")

            if os.path.exists(output_path):
                print(f"[Phase 4 Pass A] SKIP (exists): {output_path}")
                with open(output_path, "r", encoding="utf-8") as f:
                    workflow_summaries.append(f.read()[:500])
                continue

            context = _load_enriched_docs_concat(file_paths, enriched_folder, max_chars=40000)
            if not context:
                print(f"[Phase 4 Pass A] SKIP (no enriched docs): {cluster_label}")
                continue

            synthesizer = CSharpWorkflowSynthesizer(
                llm_model=OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL)
            )
            print(f"[Phase 4 Pass A] Synthesizing: {cluster_label} ({len(file_paths)} files)")
            try:
                with open(output_path, "w", encoding="utf-8") as out_file:
                    async for chunk in synthesizer.stream(context=context, question=cluster_label):
                        print(chunk, end="", flush=True)
                        out_file.write(chunk)
                        out_file.flush()
                with open(output_path, "r", encoding="utf-8") as f:
                    workflow_summaries.append(f.read()[:500])
                print(f"\n[Phase 4 Pass A] DONE: {output_path}")
            except Exception as exc:
                print(f"[Phase 4 Pass A] ERROR: {cluster_label}: {exc}")

            await asyncio.sleep(CLOUD_BATCH_DELAY)

    # ----------------------------------------------------------------
    # Pass B — critical deep dives
    # ----------------------------------------------------------------
    print("[Phase 4 Pass B] Starting critical deep dives...")
    pass_b_targets = _collect_pass_b_targets(files_dict, enriched_folder, critical_clusters)

    for target in pass_b_targets:
        flow_name = target["flow_name"]
        module = target["module"]
        file_paths = target["file_paths"]

        module_folder = os.path.join(workflows_folder, module)
        os.makedirs(module_folder, exist_ok=True)
        output_path = os.path.join(module_folder, f"{flow_name}_CRITICAL_deep_dive.md")

        if os.path.exists(output_path):
            print(f"[Phase 4 Pass B] SKIP (exists): {output_path}")
            continue

        context = _load_enriched_docs_concat(file_paths, enriched_folder, max_chars=60000)
        if not context:
            print(f"[Phase 4 Pass B] SKIP (no enriched docs): {flow_name}")
            continue

        analyzer = CSharpCriticalWorkflowAnalyzer(
            llm_model=OpenRouter(model=OPENROUTER_CRITICAL_MODEL)
        )
        print(f"[Phase 4 Pass B] Deep diving: {flow_name} ({len(file_paths)} files)")
        try:
            with open(output_path, "w", encoding="utf-8") as out_file:
                async for chunk in analyzer.stream(context=context, question=flow_name):
                    print(chunk, end="", flush=True)
                    out_file.write(chunk)
                    out_file.flush()
            print(f"\n[Phase 4 Pass B] DONE: {output_path}")
        except Exception as exc:
            print(f"[Phase 4 Pass B] ERROR: {flow_name}: {exc}")

        await asyncio.sleep(CLOUD_BATCH_DELAY)

    # ----------------------------------------------------------------
    # Cross-domain flows
    # ----------------------------------------------------------------
    cross_domain_paths = _detect_cross_domain_files(files_dict)
    if cross_domain_paths:
        cross_folder = os.path.join(workflows_folder, "CrossDomain")
        os.makedirs(cross_folder, exist_ok=True)
        context = _load_enriched_docs_concat(cross_domain_paths, enriched_folder, max_chars=60000)
        if context:
            output_path = os.path.join(cross_folder, "EstimateToVoyageTransition_CRITICAL_deep_dive.md")
            if not os.path.exists(output_path):
                analyzer = CSharpCriticalWorkflowAnalyzer(
                    llm_model=OpenRouter(model=OPENROUTER_CRITICAL_MODEL)
                )
                print(f"[Phase 4] Synthesizing cross-domain flow ({len(cross_domain_paths)} files)")
                try:
                    with open(output_path, "w", encoding="utf-8") as out_file:
                        async for chunk in analyzer.stream(
                            context=context, question="EstimateToVoyageTransition"
                        ):
                            print(chunk, end="", flush=True)
                            out_file.write(chunk)
                            out_file.flush()
                    print(f"\n[Phase 4] DONE: {output_path}")
                except Exception as exc:
                    print(f"[Phase 4] ERROR cross-domain: {exc}")
                await asyncio.sleep(CLOUD_BATCH_DELAY)

    # ----------------------------------------------------------------
    # Final synthesis: BVMS_Architecture_Overview.md
    # ----------------------------------------------------------------
    await _synthesize_architecture_overview(workflows_folder, workflow_summaries)

    # Update manifest phase for all processed files
    for rel_path in list(files_dict.keys()):
        if manifest.get_phase(rel_path) == "enriched":
            manifest.set_phase(rel_path, "synthesized")
    manifest.save()
    print("[Phase 4] Complete.")
