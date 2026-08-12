# ProgressiveAgentSLM — Planning & Progress Tracker

> **This file is the canonical planning + WIP tracker. It now lives inside the
> `ProgressiveAgentSLM/planning/` folder — the project's new home. The copy at
> `ai-c4y/planning/` is the previous home and is superseded.**
>
> **Scope notice (2026-08-12).** The full §1–§16 content of this plan is maintained in this file
> within the new project. It documents the single recursive `ProgressiveAgentSLM` class, the
> three-window percentage context budget, the capability-routed `models_ladder`, hook-driven
> `behavior_policies`, the append-only `iteration_logging` raw log + `memory_data_stores`, and the
> JSON/Python config loader. See `design-principle.md` for the why and `wip_checklist.md` for the
> how (execution checklist — the tracker).

## 1. Mission (condensed)

A single, **recursive** agent class tuned for **local / small language models (SLMs)**: it reasons
like a senior expert through **disciplined, cultivated context of experience — not a bigger LLM**.

> Theme from [`design-principle.md`](design-principle.md): _"an expert human thinks in an SLM through
> discipline and cultivated context of experience, not an LLM."_

## 2. The design pillars

1. **One recursive class.** A "team" is an agent with `delegates` that are themselves
   `ProgressiveAgentSLM` instances. Composition = recursion.
2. **Three-window percentage context budget** (`cognition_window` / `attention_window` /
   `response_window`, sum = 100) over the active model's `max_tokens` — same config, any model.
3. **Byte-stable prefix + volatile suffix** (prompt-cache discipline) — rebuilt only on a sanctioned
   compaction.
4. **Enforced, not just prompted** `behavior_policies` — guarded turn-end hooks, not prompt text.
5. **Append-only `iteration_logging` raw log (L1)** + a chain of derived `memory_data_stores`
   (L2/L3, sqlite-vec) — compaction is lossless; nothing is truly lost.
6. **Capability-routed `models_ladder`** (role flags, per-endpoint warm models, single failover
   budget) — local-first, cloud optional.
7. **One shared `base_folder_path`** — delegates nest under the parent and loop back over each other's
   work via retrieval tools.
8. **Declarative config** (JSON **or** Python) — a non-programmer authors the agent tree.

## 3. Status & progress

See [`wip_checklist.md`](wip_checklist.md) for the 100-todo, phase-by-phase execution tracker, and
[`planning.md`](planning.md) §12 for the phase breakdown. As of 2026-08-12:

- **Phase 0 — Foundation primitives:** scaffolded (structure + stubs). Core algorithms (three-window
  percentage math, model-chain failover, append-only raw log) still **unbuilt** — see the checklist.
- **Phase 1 — Recursive core agent:** **unbuilt** (the recursive loop, windows, ladder, stores).
- **Phase 2 — Full tools + policies + routing:** **unbuilt**.
- **Phase 3 — Config loader (JSON + Python):** `example-revised.json` present (JSONC); loader **unbuilt**.
- **Phase 4 — Hardening:** **unbuilt**.

## 4. Documents in this folder

| File                         | Purpose                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------ |
| `planning.md`                | The full §1–§16 canonical design doc.                                          |
| `wip_checklist.md`           | **The execution tracker** — 100 todos, phase-by-phase, "read / do / validate". |
| `design-principle.md`        | The _why_ — two knowledge stores + a reasoning layer.                          |
| `example-revised.json`       | The canonical `bvms-assistant` config (JSONC).                                 |
| `analysis-against-hermes.md` | Hermes comparison + folded-in lessons.                                         |
| `steal-list-hermes.md`       | The file-by-file porting map from `temp/hermes-agent`.                         |
| `review-revise-design.md`    | The design review (2026-08-12) — code-vs-doc gap.                              |
| `design-review-summary.md`   | The one-page review summary.                                                   |
| `scratch.md`                 | Orientation scratch notes (Phase 0 items 1–2).                                 |
| `IMPROVEMENTS.md`            | The earlier AI-Orchestra improvement roadmap (historical).                     |

> The full canonical design content is preserved in `planning.md` in this folder; the condensed mission
> above and these documents constitute the project's living home and WIP tracker.

_Companion: [`wip_checklist.md`](wip_checklist.md) (tracker), [`design-principle.md`](design-principle.md)
(the why), [`planning.md`](planning.md) (the full design)._
