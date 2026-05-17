"""
cia_phase4_synthesize.py

Phase 4 — Workflow Synthesis

Two-pass synthesis from enriched per-file docs into high-level workflow documents:

  Pass A — Domain module flow docs (one per module × verb cluster)
  Pass B — Critical workflow deep dives (priority flows + is_critical clusters)
  Final  — BVMS_Architecture_Overview.md from all workflow summaries

Model selection: Ollama if force_local, otherwise OpenRouter (cloud default).
Concurrent batches controlled by the `concurrency` parameter.
"""

import asyncio
import os
import re
from datetime import datetime

from .cia_config import (
    OPENROUTER_SYNTHESIS_MODEL,
    OPENROUTER_CRITICAL_MODEL,
    CLOUD_BATCH_DELAY,
    DEFAULT_INDEX_PATH,
    DEFAULT_ENRICHED_FOLDER,
    DEFAULT_WORKFLOWS_FOLDER,
    VERB_CLUSTERS,
    PRIORITY_CRITICAL_FLOWS,
    _load_index,
    _load_discovered_flows,
)
from .agents.CSharpWorkflowSynthesizer import CSharpWorkflowSynthesizer
from .agents.CSharpCriticalWorkflowAnalyzer import CSharpCriticalWorkflowAnalyzer
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_GENERAL_MODEL
from .CSharpManifest import CSharpManifest

# -------------------------------------------------------------------
# Phase-local helpers
# -------------------------------------------------------------------


def _tokenize_identifier(text: str) -> set[str]:
    """Split a CamelCase class name or file path into a set of lowercase word tokens.

    Examples::
        CreateVoyageFromEstimate  → {create, voyage, from, estimate}
        VoyagePnLCalculator       → {voyage, pn, l, calculator}  (acronyms split per char)
        BBC.VoyageManagement/...  → includes all path segments
    """
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)
    spaced = re.sub(r'([a-z\d])([A-Z])', r'\1 \2', spaced)
    tokens = re.split(r'[^a-zA-Z0-9]+', spaced)
    return {t.lower() for t in tokens if len(t) > 1}


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
      1. Hard-coded priority flows (PRIORITY_CRITICAL_FLOWS) — always included first
      2. Dynamically discovered flows from wip/discovered-workflows.json
         (written by --phase workflow-identify)
      3. Any critical cluster not already covered by a priority flow
    """
    # Merge static config with dynamically discovered flows (deduplicated by name)
    discovered = _load_discovered_flows()
    seen_names_lower = {f["name"].lower() for f in PRIORITY_CRITICAL_FLOWS}
    extra_flows = [d for d in discovered if d.get("name", "").lower() not in seen_names_lower]
    all_flow_defs = list(PRIORITY_CRITICAL_FLOWS) + extra_flows
    if extra_flows:
        print(f"[Phase 4 Pass B] Merging {len(extra_flows)} discovered workflow(s) from wip/discovered-workflows.json")

    targets = []
    seen_flow_names: set[str] = set()

    for flow_def in all_flow_defs:
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
    tmp_path = output_path + ".tmp"
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
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
        with open(tmp_path, "w", encoding="utf-8") as out_file:
            async for chunk in synthesizer.stream(context=summaries_text, question="BVMS System Overview"):
                print(chunk, end="", flush=True)
                out_file.write(chunk)
                out_file.flush()
        os.rename(tmp_path, output_path)
        print(f"\n[Phase 4] DONE: {output_path}")
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        print(f"[Phase 4] ERROR synthesizing architecture overview: {e}")


# -------------------------------------------------------------------
# Phase 4 — synthesize_workflow_documents
# -------------------------------------------------------------------


async def synthesize_workflow_documents(
    enriched_folder: str = DEFAULT_ENRICHED_FOLDER,
    workflows_folder: str = DEFAULT_WORKFLOWS_FOLDER,
    index_path: str = DEFAULT_INDEX_PATH,
    manifest: CSharpManifest = None,
    force_cloud: bool = False,
    force_local: bool = False,
    concurrency: int = 1,
):
    """
    Phase 4: Two-pass workflow synthesis.

    Pass A — Domain module flow docs (one per module × verb cluster)
    Pass B — Critical workflow deep dives (priority flows + is_critical clusters)
    Final  — BVMS_Architecture_Overview.md from all workflow summaries

    Model selection: Ollama if force_local, otherwise OpenRouter (cloud default).
    Concurrent batches controlled by the `concurrency` parameter.
    """
    if manifest is None:
        manifest = CSharpManifest()
    index = _load_index(index_path)
    files_dict = index.get("files", {})
    os.makedirs(workflows_folder, exist_ok=True)

    effective_batch = max(1, concurrency)

    # ----------------------------------------------------------------
    # Build cluster map
    # ----------------------------------------------------------------
    clusters: dict[str, dict[str, list]] = {}
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
    # Pass A — module flow docs (concurrent batches)
    # ----------------------------------------------------------------
    pass_a_tasks = []
    for module, verb_groups in clusters.items():
        module_folder = os.path.join(workflows_folder, module)
        os.makedirs(module_folder, exist_ok=True)
        for verb_cluster, file_paths in verb_groups.items():
            output_path = os.path.join(module_folder, f"{verb_cluster}_workflow.md")
            pass_a_tasks.append((module, verb_cluster, list(file_paths), output_path))

    print(f"[Phase 4 Pass A] Modules: {list(clusters.keys())}, {len(pass_a_tasks)} clusters to synthesize")
    total_a = len(pass_a_tasks)
    workflow_summaries: list[str] = []

    async def _pass_a_item(module_v, verb_cluster_v, file_paths_v, output_path_v, task_idx: int):
        cluster_label = f"{module_v} — {verb_cluster_v}"
        tmp_path = output_path_v + ".tmp"
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists(output_path_v):
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Phase 4 Pass A] {ts} [{task_idx}/{total_a}] SKIP (exists): {output_path_v}")
            with open(output_path_v, "r", encoding="utf-8") as f:
                return f.read()[:500]
        context = _load_enriched_docs_concat(file_paths_v, enriched_folder, max_chars=40000)
        if not context:
            print(f"[Phase 4 Pass A] SKIP (no enriched docs): {cluster_label}")
            return None
        # Workflow synthesis is complex — use the critical model (CIA_OPENROUTER_CRITICAL_MODEL)
        # for richer, more accurate module-level workflow docs.
        # The architecture overview (final step) stays on the cheaper synthesis model.
        llm = Ollama(model=OLLAMA_GENERAL_MODEL) if force_local else OpenRouter(model=OPENROUTER_CRITICAL_MODEL)
        synthesizer = CSharpWorkflowSynthesizer(llm_model=llm)
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[Phase 4 Pass A] {ts} [{task_idx}/{total_a}] Synthesizing: {cluster_label} ({len(file_paths_v)} files)")
        try:
            with open(tmp_path, "w", encoding="utf-8") as out_file:
                async for chunk in synthesizer.stream(context=context, question=cluster_label):
                    if effective_batch == 1:
                        print(chunk, end="", flush=True)
                    out_file.write(chunk)
                    out_file.flush()
            os.rename(tmp_path, output_path_v)
            with open(output_path_v, "r", encoding="utf-8") as f:
                summary = f.read()[:500]
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"\n[Phase 4 Pass A] {ts} [{task_idx}/{total_a}] DONE: {output_path_v}")
            return summary
        except Exception as exc:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print(f"[Phase 4 Pass A] ERROR: {cluster_label}: {exc}")
            return None

    for batch_start in range(0, total_a, effective_batch):
        batch = pass_a_tasks[batch_start : batch_start + effective_batch]
        results = await asyncio.gather(*[_pass_a_item(*t, task_idx=batch_start + i + 1) for i, t in enumerate(batch)])
        workflow_summaries.extend(r for r in results if r)
        if batch_start + effective_batch < total_a:
            print(f"[Phase 4 Pass A] Sleeping {CLOUD_BATCH_DELAY}s (rate-limit guard)...")
            await asyncio.sleep(CLOUD_BATCH_DELAY)

    # ----------------------------------------------------------------
    # Pass B — critical deep dives (concurrent batches)
    # ----------------------------------------------------------------
    pass_b_targets = _collect_pass_b_targets(files_dict, enriched_folder, critical_clusters)
    for target in pass_b_targets:
        module_folder = os.path.join(workflows_folder, target["module"])
        os.makedirs(module_folder, exist_ok=True)
        target["output_path"] = os.path.join(module_folder, f"{target['flow_name']}_CRITICAL_deep_dive.md")

    print(f"[Phase 4 Pass B] {len(pass_b_targets)} critical deep dives...")
    total_b = len(pass_b_targets)

    async def _pass_b_item(target_v, task_idx: int):
        flow_name = target_v["flow_name"]
        file_paths_v = target_v["file_paths"]
        output_path_v = target_v["output_path"]
        tmp_path = output_path_v + ".tmp"
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists(output_path_v):
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Phase 4 Pass B] {ts} [{task_idx}/{total_b}] SKIP (exists): {output_path_v}")
            return
        context = _load_enriched_docs_concat(file_paths_v, enriched_folder, max_chars=60000)
        if not context:
            print(f"[Phase 4 Pass B] SKIP (no enriched docs): {flow_name}")
            return
        llm = Ollama(model=OLLAMA_GENERAL_MODEL) if force_local else OpenRouter(model=OPENROUTER_CRITICAL_MODEL)
        analyzer = CSharpCriticalWorkflowAnalyzer(llm_model=llm)
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[Phase 4 Pass B] {ts} [{task_idx}/{total_b}] Deep diving: {flow_name} ({len(file_paths_v)} files)")
        try:
            with open(tmp_path, "w", encoding="utf-8") as out_file:
                async for chunk in analyzer.stream(context=context, question=flow_name):
                    if effective_batch == 1:
                        print(chunk, end="", flush=True)
                    out_file.write(chunk)
                    out_file.flush()
            os.rename(tmp_path, output_path_v)
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"\n[Phase 4 Pass B] {ts} [{task_idx}/{total_b}] DONE: {output_path_v}")
        except Exception as exc:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print(f"[Phase 4 Pass B] ERROR: {flow_name}: {exc}")

    for batch_start in range(0, total_b, effective_batch):
        batch = pass_b_targets[batch_start : batch_start + effective_batch]
        await asyncio.gather(*[_pass_b_item(t, batch_start + i + 1) for i, t in enumerate(batch)])
        if batch_start + effective_batch < total_b:
            print(f"[Phase 4 Pass B] Sleeping {CLOUD_BATCH_DELAY}s...")
            await asyncio.sleep(CLOUD_BATCH_DELAY)

    # ----------------------------------------------------------------
    # Cross-domain flows (single task, no batching needed)
    # ----------------------------------------------------------------
    cross_domain_paths = _detect_cross_domain_files(files_dict)
    if cross_domain_paths:
        cross_folder = os.path.join(workflows_folder, "CrossDomain")
        os.makedirs(cross_folder, exist_ok=True)
        context = _load_enriched_docs_concat(cross_domain_paths, enriched_folder, max_chars=60000)
        if context:
            output_path = os.path.join(cross_folder, "EstimateToVoyageTransition_CRITICAL_deep_dive.md")
            tmp_path = output_path + ".tmp"
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            if not os.path.exists(output_path):
                llm = Ollama(model=OLLAMA_GENERAL_MODEL) if force_local else OpenRouter(model=OPENROUTER_CRITICAL_MODEL)
                analyzer = CSharpCriticalWorkflowAnalyzer(llm_model=llm)
                print(f"[Phase 4] Synthesizing cross-domain flow ({len(cross_domain_paths)} files)")
                try:
                    with open(tmp_path, "w", encoding="utf-8") as out_file:
                        async for chunk in analyzer.stream(
                            context=context, question="EstimateToVoyageTransition"
                        ):
                            print(chunk, end="", flush=True)
                            out_file.write(chunk)
                            out_file.flush()
                    os.rename(tmp_path, output_path)
                    print(f"\n[Phase 4] DONE: {output_path}")
                except Exception as exc:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                    print(f"[Phase 4] ERROR cross-domain: {exc}")

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
