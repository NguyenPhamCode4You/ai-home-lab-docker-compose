# ProgressiveAgentSLM — Design Review Summary (one page)

> Full analysis: [`review-revise-design.md`](review-revise-design.md). Source: `planning.md` +
> `design-principle.md` + `example-revised.json` + `analysis-against-hermes.md` + the actual
> `src/framework/` code on disk. Date: 2026-08-12.

## Verdict (one paragraph)

The core thesis — **an expert human thinks in an SLM through discipline and cultivated context, not a
bigger LLM** — is sound and independently validated by Hermes, OpenCode, and Claude, which all converged
on the same powers (tiered context budgets, append-only logs + distilled memory, prompt-cache discipline).
The design is the right point on the curve **if the memory-discipline and build phases are honored**. The
number one real blocker is that **the code on disk is an earlier, different design than the docs**, so a
lot of what reads in `planning.md` as "exists, needs rework" is actually **unbuilt**.

## What's genuinely good (keep — no churn)

- Three-window **proportional** budget (percentages of the active model's `max_tokens`). Same config runs on a 20B local or a cloud 200k model — enables escalation mid-run.
- **Recursive single-class agent** — a team is just an agent with `delegates`.
- **Append-only `iteration_logging` as the single raw source of truth** + derived `memory_data_stores` — compaction is **lossless** (better than Hermes' lossy compress).
- **Enforced, not just prompted** `behavior_policies` — turn-end guards stop hallucination on small models.
- **Prompt-cache discipline**: byte-stable prefix + volatile suffix, rebuild only on sanctioned compaction.
- **Capability-routed model pool** (`is_*` flags, per-endpoint warm models) + **pre-built vs. self-cultivated** stores.

## Reality check: docs vs. code (the real "make it happen" blocker)

| Plan says (`~`, exists-needs-rework)                        | On disk                                                                        |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `ContextWindow` — 3-window **percentage**                   | 4-tier **fractional** (`conversation…/cognitive…/attention…`) — **stale**      |
| `ModelChain` — ordered ladder + role flags + success-reset  | `ModelRegistry` — role→chain dict (`chat/reflection/reasoning`)                |
| append-only `iteration_*.jsonl`                             | `Worklog.py` — single rewritten `worklog.md` (contradicts §8.1)                |
| `SqliteVectorQueryTool` + sqlite-vec `SqliteVectorStore`    | `tools/*` still wrap **Supabase pgvector**; no local `.db`                     |
| `tools/` = SqliteVectorQueryTool, JsonlQueryTool, TodoTool… | `tools/` = `ReadFileTool` (bare `open()`, no deny-list) + `VectorSearchTool`   |
| `AgentConfig` parses full §2 fields + inheritance           | `AgentConfig` has `goal/knowledge/tools/sub_agents/…` — none of the new fields |
| `config/load.py` + `schema.json` (Phase 3)                  | **does not exist**                                                             |

Also: `example-revised.json` is **JSONC (commented)**, so a stock `json.load` will fail — needs a JSONC
loader; and the demo still wires a **flat** agent, not the recursive `delegates` tree it now configures.

## What could be better (sharpest recs)

1. **Single self-similar JSON → full recursive tree.** Load one config, resolve `[base_folder_path]` per node, build the whole delegate tree from the root — the differentiator vs. OpenCode's hand-wired per-mode YAML.
2. **Cost/run guard** — a `run_clock` (`max_run_seconds`) + failover on slow forward passes, on top of per-model retries.
3. **Real observability** — make the §7b `GET /api/v1/health` (models/ stores/ windows/ delegates) a Phase-3 deliverable, not a doc sketch.
4. **`bounded_io`** (byte cap + deadline) as a named helper used by every external read + `SqliteVectorQueryTool`.
5. **Resolve the shared-`.db`/per-table contract** for `memory_data_stores` (all tables in one file need a shared schema + per-table isolation seam).
6. **`NoFindingsGuard`** — deterministic re-plan + refusal branch after consecutive empty retrievals (the enforcement behind `refusing_to_invent`).
7. **A curated "edge-case" store** — dedupe/archive/consolidate, or it'll grow into an unstructured dump.
8. **`QuizEngine`** — a named owner for `self_evaluation_quizz`, wired to the `is_reflection_and_evaluation` model.

## Risks & judgment calls

- `known_edge_cases_knowledge` can become an unbounded dump → add a size/similarity flywheel.
- `design_decisions_knowledge` on every iteration fabricates "decisions" → gate on a sparse hook (research/reflection) or a `when`.
- A 15% `response_window` is tight on 8k models + a diagram → tune up or write diagram to file & link.
- Cloud escalation — keep `max_retries_until_switching_models` strictly infra/quality failover and prefer **local** general-purpose first in the default ladder (already so in `example-revised.json`; make it a documented invariant).

## What I changed

- **Created** `review-revise-design.md` (full analysis, §0–§9).
- **Created** this summary.
- **Edited `planning.md`**: corrected the Phase 0/1 file descriptions to the on-disk reality; added a
  design-risks/open-loops note to §8; added `TokenCounter`/`bounded_io`/`run_clock`/`NoFindingsGuard`/
  `QuizEngine` owners to Phase 2; marked `example-revised.json` as JSONC + added loader/schema + load-a-recursive-tree step to Phase 3; added stable-prefix byte-identical + cost-bound tests to Phase 4.

**Bottom line:** keep the philosophy, close the docs↔code gap, make memory discipline + config-loader +
observability first-class — then it's a legitimately differentiated, local-first domain-expert harness.
