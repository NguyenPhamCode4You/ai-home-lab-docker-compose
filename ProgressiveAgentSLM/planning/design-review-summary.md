# ProgressiveAgentSLM — Design Review Summary (one page)

> Full analysis: [`review-revise-design.md`](review-revise-design.md). **2026-08-12 — this project now
> lives in `ProgressiveAgentSLM/`; the first implementation pass scaffolded the whole thing.**

## Verdict (one paragraph)

The core thesis — **an expert human thinks in an SLM through discipline and cultivated context, not a
bigger LLM** — is sound and independently validated by Hermes, OpenCode, and Claude, which all converged
on the same powers (tiered context budgets, append-only logs + distilled memory, prompt-cache discipline).
**The first implementation pass fixed the docs↔code gap**: a new `ProgressiveAgentSLM/` folder scaffolds
the §11 layout with the three-window `ContextWindow`, `ModelChain`, the memory subsystem, safety/redact,
guards, delegate contracts, the JSONC config loader, and the recursive agent class. The remaining Phases
0–4 core algorithms are tracked in `wip_checklist.md`.

## What's genuinely good (keep — no churn)

- Three-window **proportional** budget (percentages of the active model's `max_tokens`); same config on any model.
- **Recursive single-class agent** — a team is an agent with `delegates`.
- **Append-only `iteration_logging` + derived `memory_data_stores`** — compaction is **lossless**.
- **Enforced, not just prompted** `behavior_policies` — turn-end guards.
- **Prompt-cache discipline**: byte-stable prefix + volatile suffix.
- **Capability-routed model pool** + **pre-built vs. self-cultivated** stores.

## What the first implementation pass delivered

| Area           | On disk now                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------- |
| Package layout | `ProgressiveAgentSLM/src/framework/**` (§11) + `src/agents/models/`                         |
| Planning home  | `ProgressiveAgentSLM/planning/` — full design + WIP tracker                                 |
| Hermes ports   | `bounded_io`, `CircularRounds`, `tools/safety`, `redact`, `guards/*`, `delegates/contracts` |
| Rebuilt core   | `ContextWindow` (3-window), `ModelChain`, `AgentConfig`, recursive `ProgressiveAgentSLM`    |
| Config         | `config/load.py` (JSONC → tree) + `example-revised.json`                                    |
| Tools          | `ReadFileTool` (safety), `TodoTool`, `SqliteVectorQueryTool`, `JsonlQueryTool` + factory    |
| Memory         | `RawLog`, `MemoryStore(s)`, `Distiller`, `LogSearch`, `RunLogger` (importable)              |
| Tests          | `tests/framework/` (green-from-day-one)                                                     |
| Metadata       | `pyproject.toml`, `requirements.txt`, `README.md`, `.gitignore`                             |

## What's still unbuilt (see `wip_checklist.md`)

- Phase 0: cascade-on-zero, compaction signals, `CognitiveIndex`, single-writer, real reflection, complete tests.
- Phase 1: the full per-step loop (retrieve → assemble → act → flush → self-eval → recurse).
- Phase 2: the remaining tools, enforcement guards, ranking, live budget enforcement, `LogSearch` FTS5.
- Phase 3: JSON schema, `ApiServer`/health, Python-dict parity, authoring README.
- Phase 4: stub-model harness, integration smoke, property/immutability/`bounded_io` tests, CI.

## Bottom line

Keep the philosophy, build out the tracked phases, and treat memory discipline + config-loader +
observability as first-class — then it's a legitimately differentiated, local-first domain-expert harness.
