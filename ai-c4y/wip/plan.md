# Plan: C# Codebase RAG Agent — Deep Technical Knowledge System

_Revised: 2026-05-14 | Progress tracked in `wip/progress/`_

## TL;DR

Extend the existing RAG pipeline (ai-c4y/) to ingest an entire C# codebase (BVMS backend) and produce a specialized "BVMS-Code Technical Assistant" RAG agent. The workflow: configure filters → index .cs file structure → generate per-file markdown docs with adaptive model selection → enrich with cross-reference impact analysis → synthesize critical business workflow docs with Mermaid diagrams → insert into Supabase → expose as third agent in the orchestra. An incremental re-learning mode handles MR-triggered updates efficiently.

## Progress Files

Each phase has a dedicated file in `wip/progress/`:

- [Phase 0](progress/phase-0-infrastructure.md) — Infrastructure Setup (manual)
- [Phase 1](progress/phase-1-indexing.md) — Codebase Indexing
- [Phase 2](progress/phase-2-documentation.md) — Per-File Documentation
- [Phase 3](progress/phase-3-enrichment.md) — Cross-Reference Enrichment
- [Phase 4](progress/phase-4-synthesis.md) — Business Workflow Synthesis
- [Phase 5](progress/phase-5-insertion.md) — Supabase Insertion
- [Phase 6](progress/phase-6-rag-chat.md) — RAG Chat Setup
- [Phase 7](progress/phase-7-incremental.md) — Incremental Re-Learning

---

---

## Phase 0 — Infrastructure Setup

**⚠️ Manual steps only. Do not automate. See [progress/phase-0-infrastructure.md](progress/phase-0-infrastructure.md)**

1. Add env vars to `.env` / `.env.example`: `CSHARP_CODEBASE_PATH`, `BVMS_CODE_TABLE_NAME`, `CSHARP_LARGE_FILE_LINE_THRESHOLD`, `CSHARP_FOCUS_ONLY_FILES`, `CSHARP_IGNORE_FILES`
   - `CSHARP_FOCUS_ONLY_FILES`: comma-separated glob patterns — when set, ONLY matching files are processed (e.g., `**/VoyageManagement/**/*.cs`). Leave empty for full codebase.
   - `CSHARP_IGNORE_FILES`: always-applied exclusions (defaults: `**/Migrations/**,**/*.Designer.cs,**/obj/**,**/bin/**`)
2. Create Supabase table `n8n_documents_bvms_code` + RPC function `match_n8n_documents_bvms_code` using same schema as `n8n_documents_bvms_neo`
3. Create output folders: `csharp-docs/raw/`, `csharp-docs/enriched/`, `csharp-docs/workflows/`, `csharp-docs/done/`
4. Manifest schema: `{ file_path: { hash, processed_at, doc_path, phase, file_type, lines, is_critical } }` — phases: `unprocessed → indexed → documented → enriched → synthesized → inserted`

---

## Phase 1 — Codebase Indexing (Structural Extraction)

**See [progress/phase-1-indexing.md](progress/phase-1-indexing.md)**

**New files:** `src/agents/CSharpFileAnalyzer.py`, `src/CSharpManifest.py`, `src/CSharpCodebaseWorkflow.py` (skeleton + `build_codebase_index`), `code_learn_csharp.py`

5. **`CSharpFileAnalyzer.py`** — `Task` subclass. Extracts JSON from each `.cs` file: `{ class_name, namespace, file_type, architecture_layer, handler_verb, methods, using_imports, injected_services, entities_referenced, external_clients_used }`
   - **Model selection:** file `<= CSHARP_LARGE_FILE_LINE_THRESHOLD` (default 200 lines) → `Ollama(OLLAMA_CODE_MODEL)` (fast, local). File `> threshold` → `OpenRouter` cloud model with large context. On JSON parse failure: retry once with stricter prompt; on second failure log + record `file_type: "Other"` (never block pipeline).
6. **`CSharpManifest.py`** — utility wrapping `csharp-manifest.json`: `load/save`, `get_phase/set_phase`, `get_all_at_phase`, `reset_file`, `get_dependents(file_path, index)`, `compute_hash`, `has_changed`
7. **`build_codebase_index()`** in `CSharpCodebaseWorkflow.py`:
   - Walk all `.cs` files → apply `FOCUS_ONLY` then `IGNORE` filters → run `CSharpFileAnalyzer` in async batches
   - Build `csharp_index.json` + `used_by` reverse-lookup map (regex/string match of class names across all files)
   - Checkpoint every 50 files; process priority: Domain → Business → Infrastructure → API → ExternalClients → Functions
8. **`code_learn_csharp.py`** — entry point: `--phase [index|document|enrich|synthesize|insert|all]`, `--mode [full|incremental]`, `--focus`, `--changed-files`, `--from-stdin`

---

## Phase 2 — Per-File Documentation

**See [progress/phase-2-documentation.md](progress/phase-2-documentation.md)**

**New files:** `src/agents/CSharpDocumentWriter.py`
**Modified:** `src/CSharpCodebaseWorkflow.py` (add `write_csharp_documents`)

9. **`CSharpDocumentWriter.py`** — `Task` subclass extending `CodeDocumentWriter`. C#/CQRS-aware prompt generates per-file docs with sections: `# General Purpose`, `# Architecture Layer`, `# Class: {Name}`, `## N. Method — purpose` + code snippet + `**Explanation**` (preserving the existing `insert_code_documents` split boundary), `# Dependencies`, `# Impact Scope` (placeholder for Phase 3).
   - **Model selection:** `<= 200 lines` → local Ollama. `> 200 lines` → `OpenRouter(qwen/qwen3-32b)`. Handler with > 5 injected services → force cloud. `is_critical=true` → force cloud.
10. **`write_csharp_documents()`** — async batches of 10 (cloud rate limit guard). Passes file content + index context (file entry + top-10 `used_by` entries, capped 2000 chars). Saves `csharp-docs/raw/{relative_path}.md`. Flushes manifest every 10 files. Idempotent (skips existing).

---

## Phase 3 — Cross-Reference Enrichment (Reflection Pass)

**See [progress/phase-3-enrichment.md](progress/phase-3-enrichment.md)**

**New files:** `src/agents/CSharpImpactAnalyzer.py`
**Modified:** `src/CSharpCodebaseWorkflow.py` (add `enrich_with_cross_references`)

11. **`CSharpImpactAnalyzer.py`** — `Task` subclass. Takes Phase 2 doc + caller list from `used_by`. Generates: `# Impact Scope` (impact rating Low/Medium/High/Critical + justification + what breaks + affected business areas + safe-to-modify assessment) and `# Used By` (callers grouped by architecture layer).
    - **Model selection:** combined input `<= 6000 chars` → local Ollama. `> 6000 chars` → `OpenRouter(qwen/qwen3-32b)`. `is_critical=true` → force cloud.
12. **`enrich_with_cross_references()`** — replaces `# Impact Scope` placeholder with generated analysis. Scores criticality after each file (signals: `used_by` count, domain entity type, handler verb, impact rating, file name keywords). Files scoring >= 5 tagged `is_critical=true` in manifest + index. Saves to `csharp-docs/enriched/`.

---

## Phase 4 — Business Workflow Synthesis (Self-Learning / Reflection)

**See [progress/phase-4-synthesis.md](progress/phase-4-synthesis.md)**

**New files:** `src/agents/CSharpWorkflowSynthesizer.py`, `src/agents/CSharpCriticalWorkflowAnalyzer.py`
**Modified:** `src/CSharpCodebaseWorkflow.py` (add `synthesize_workflow_documents`)

**All synthesis tasks use cloud models exclusively** (input is always large multi-doc context).

13. **Pass A — Domain Module Flows** (`CSharpWorkflowSynthesizer.py`, model: `OpenRouter/qwen3-32b`):
    - Groups enriched docs by domain module + verb cluster (Read/Write/Calculate/Transition/Sync)
    - Detects cross-domain flows (e.g., `CreateVoyageFromEstimate` spans Estimate + Voyage)
    - Each cluster produces a workflow doc with: business purpose, step-by-step narrative, **Mermaid sequence diagram**, key business rules, entities involved, external integrations, error conditions, **connection links** (exact file paths for navigation)
14. **Pass B — Critical Business Workflow Deep Dives** (`CSharpCriticalWorkflowAnalyzer.py`, model: `OpenRouter/google/gemini-2.5-pro` or best available):
    - Triggered for any cluster with `is_critical=true` files AND for hard-coded priority flows:
      - Voyage/Estimate P&L Calculation
      - Voyage Lifecycle Transitions (CreateVoyageFromEstimate, CompleteVoyage)
      - Bunker Order & Cost Calculation
      - Commission & Payment Calculation
      - ETS / Emissions Calculation
    - Generates everything from Pass A **plus**: data flow map, **Mermaid state machine diagram** (for lifecycle flows), calculation formula breakdown (for financial flows), validation gate map, concurrency/transaction boundaries, impact-if-changed per method, **new developer onboarding guide** for this flow
15. **Final synthesis** — `BVMS_Architecture_Overview.md` from all workflow doc summaries: system capabilities overview, module interconnections, top-level Mermaid component diagram, list of all critical flows with links

---

## Phase 5 — Supabase Insertion

**See [progress/phase-5-insertion.md](progress/phase-5-insertion.md)**

**Modified:** `src/agents/tools/SupabaseVectorStore.py` (add `delete_by_metadata`), `src/CSharpCodebaseWorkflow.py` (add `insert_csharp_knowledge`)

16. **`delete_by_metadata(table_name, key, value)`** — new method on `SupabaseVectorStore`. Deletes existing rows by metadata field before re-insertion. Required for idempotency and incremental updates.
17. **`insert_csharp_knowledge()`**:
    - Enriched per-file docs → existing `insert_code_documents()` (splits on `**Explanation**`, stores code + explanation separately)
    - Workflow/architecture docs → existing `insert_sentences()` (splits on markdown headers)
    - Metadata includes new `source_type` field (`code_file` vs `workflow_doc`) and `is_critical`
    - Insertion order: Architecture Overview → Critical deep dives → Other workflows → Domain → Business → Infrastructure → API

---

## Phase 6 — RAG Chat Setup

**See [progress/phase-6-rag-chat.md](progress/phase-6-rag-chat.md)**

**New files:** `rag_chat_bvms_code.py`
**Modified:** `rag_orchestra.py`

18. **`rag_chat_bvms_code.py`** — mirrors `rag_chat_bvms.py`. Uses `query_function_name="match_n8n_documents_bvms_code"`, `OpenRouter(qwen3-32b)` as default model, C#/CQRS-focused system prompt emphasising impact analysis and development guidance. Standalone port: `8002`.
19. **`rag_orchestra.py`** — add `"BVMS-Code Technical Assistant"` as third agent with description that routes C# technical questions, impact analysis, and development guidance to it.

---

## Phase 7 — Incremental Re-Learning (MR-Triggered)

**See [progress/phase-7-incremental.md](progress/phase-7-incremental.md)**

**Modified:** `src/CSharpManifest.py`, `code_learn_csharp.py`

20. `--mode=incremental`: detects changed files via `git diff --name-only origin/main HEAD` (or `--changed-files` / `--from-stdin`). Expands set to dependents via `used_by` reverse-lookup. Warns user if expanded set > 50 files.
21. Invalidates and re-runs workflow synthesis for clusters containing changed files.
22. `delete_by_metadata` purges old Supabase rows before re-inserting updated content.
23. Optional future: GitLab CI job triggering incremental mode on MR merge.

---

## Relevant Existing Files (Reuse / Modify)

- `src/CodeDocumentWorkflow.py` — pattern for `write_csharp_documents` and `insert_csharp_knowledge`
- `src/agents/CodeDocumentWriter.py` — base class for `CSharpDocumentWriter`
- `src/RagWorkflow.py` — `insert_sentences` reused for workflow docs
- `src/agents/tools/SupabaseVectorStore.py` — extend with `delete_by_metadata`
- `src/FileHanlder.py` — `for_each_file_in_folder`, extend filter logic for `.cs`
- `rag_chat_bvms.py` — template for `rag_chat_bvms_code.py`
- `rag_orchestra.py` — add third agent

## New Files Summary

| File                                           | Phase |
| ---------------------------------------------- | ----- |
| `src/agents/CSharpFileAnalyzer.py`             | 1     |
| `src/CSharpManifest.py`                        | 1     |
| `src/CSharpCodebaseWorkflow.py`                | 1–5   |
| `code_learn_csharp.py`                         | 1–7   |
| `src/agents/CSharpDocumentWriter.py`           | 2     |
| `src/agents/CSharpImpactAnalyzer.py`           | 3     |
| `src/agents/CSharpWorkflowSynthesizer.py`      | 4     |
| `src/agents/CSharpCriticalWorkflowAnalyzer.py` | 4     |
| `rag_chat_bvms_code.py`                        | 6     |

## Verification Steps

1. Run Phase 1 on a single module (e.g., `Core/Business/VoyageManagement/Voyage/`) — verify `csharp_index.json` has correct class names, methods, and dependencies
2. Run Phase 2 on 5 files — verify generated `.md` docs have all sections (General Purpose, Architecture Layer, methods, Dependencies)
3. Run Phase 3 — verify Impact Scope sections reference the correct callers from the index
4. Run Phase 4 on VoyageManagement — verify a coherent "Create Voyage" workflow doc is generated
5. Run Phase 5 — verify rows appear in Supabase `n8n_documents_bvms_code` table with correct metadata
6. Start `rag_chat_bvms_code.py`, ask "What does CreateVoyageFromEstimate do?" — verify it returns accurate handler-level details
7. Start `rag_orchestra.py`, ask "What is the impact of changing ShipmentEntity.ProfitAndLossItems?" — verify BVMS-Code Technical Assistant responds with cross-reference data
8. Test incremental mode: modify one .cs file, run `--mode=incremental` — verify only that file + its dependents are re-indexed

## Key Decisions

- **Static cross-reference analysis**: Use regex/string matching (looking for class names in file content) rather than Roslyn for simplicity. Accuracy is ~90% which is sufficient for RAG.
- **Parallel processing**: Use `asyncio.gather` in batches of 20 files to speed up Phase 2 (biggest bottleneck).
- **Scale management**: The codebase has ~hundreds of .cs files. Priority processing order: Domain entities first → Business handlers → Infrastructure → APIs → ExternalClients (most impactful knowledge first).
- **Separate Supabase table**: Use `n8n_documents_bvms_code` (not mixed with existing `n8n_documents_bvms_neo`) so the two knowledge bases stay independent and the RAG agents stay focused.
- **Model selection**: Phase 1 (indexing) uses `gemma3:4b` (fast). Phase 2-4 (documentation) uses `qwen2.5-coder:14b` (code-aware). Phase 5 insertion uses `nomic-embed-text` (existing).

## Out of Scope

- Roslyn-based static analysis (too complex to set up, regex is sufficient)
- Frontend (React) codebase analysis (separate effort)
- Unit test generation (separate responsibility)
- Live git webhook integration (manual `--mode=incremental` run is sufficient for now)
