# ProgressiveAgentSLM — Design Review, Revision & Cross-Harness Comparison

> **Ask.** Review and revise the current design; show what is good, what can be better; compare the
> system vs. existing harnesses (Hermes, OpenCode, Claude); and confirm `planning.md` captures what it
> takes to ship this.
>
> **Date:** 2026-08-12

## 0. The thesis — is the core idea sound?

Yes, and it is the strongest thing about the project. The one-liner **"an expert human thinks in an
SLM through discipline and cultivated context of experience, not a bigger LLM"** is genuinely
defensible: a 20B model at ~62k context is cheap; the expensive part is prompt re-prefill and cloud
fallback. Small local models are not the bottleneck — **unbounded / poorly-scoped context is**. The
design attacks exactly that, and the convergence with Hermes / OpenCode / Claude (tiered context
budgets, append-only logs + distilled memory, prompt-cache discipline) is strong _signal_.

The correct posture everywhere: **the discipline comes from deterministic code (hooks, budgets,
deny-lists, redaction); the trained model only supplies reasoning.**

## 1. What's genuinely good — keep, don't second-guess

| Idea                                                                             | Where   | Why it's good                                                                                   |
| -------------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------- |
| Three-window proportional budget (percentages of active `max_tokens`, sum = 100) | §3      | Same config on a 20B/62k local or a cloud 200k model; enables mid-run escalation.               |
| Recursive single-class agent                                                     | §1, §7  | A "team" is an agent with `delegates`; composition is recursion.                                |
| Append-only `iteration_logging` + derived `memory_data_stores`                   | §8      | Compaction touches only the derived view; nothing is truly lost. Better than Hermes (lossy).    |
| Hook-driven, code-enforced `behavior_policies`                                   | §5      | "Enforced, not just prompted" — the biggest behavioral lesson from Hermes.                      |
| Prompt-cache discipline (stable prefix + volatile suffix)                        | §3, §10 | Re-prefill is the dominant local latency cost; keep the prefix byte-identical until compaction. |
| Capability-routed, per-endpoint model pool                                       | §4      | Reasoning / embedding / distillation / self-eval run on distinct warm endpoints in parallel.    |
| Pre-built vs. self-cultivated stores                                             | §8      | One retrieval surface for extraction-pipeline KBs and runtime learning.                         |
| Agent-grounded `sqlite-vec` embedded stores                                      | §6      | Local `.db` files, copyable, serverless.                                                        |

## 2. Reality check: docs vs. code (the real blocker)

The plan describes a two-store, delegate-based, `sqlite-vec` recursive agent; the code in the previous
home was an earlier flat / four-tier-fractional / Supabase design. **The first implementation pass of
this project fixed the divergence**: the `ProgressiveAgentSLM/` folder now scaffolds the §11 layout
with the three-window `ContextWindow`, `ModelChain`, the memory subsystem, `tools/safety` + `redact`,
guards, delegate contracts, the JSONC config loader, and the recursive agent class. The remaining
Phases 0–4 core algorithms are still unbuilt — see [`wip_checklist.md`](wip_checklist.md).

## 3. Comparison: ours vs. Hermes vs. OpenCode vs. Claude

| Dimension              | ProgressiveAgentSLM (us)                                      | Hermes                                          | OpenCode                                             | Claude                             |
| ---------------------- | ------------------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------- | ---------------------------------- |
| Core abstraction       | Recursive agent class, JSON/Python config                     | Pluggable agent core, config, skills, subagents | CLI agent, LSP tooling, prompts-in-YAML, agent modes | Proprietary frontier closed models |
| Local-first discipline | **Strongest** — capability-routed ladder + warm endpoints     | Model-agnostic; no local-first ladder           | Local providers + LiteLLM                            | Closed models                      |
| Memory model           | **Unbounded, recoverable** append-only log + distilled stores | **Lossy** conversation compression              | Session persistence; weaker self-cultivated memory   | Proprietary long-context           |
| Context budget         | Three proportional windows + stable prefix                    | Typed/tiered breakdown (`char/4`)               | Limited                                              | Vendor-controlled                  |
| Self-improvement       | `research`/`reflection` + quiz > most peers                   | Background learning + curator                   | No autonomous self-eval loop                         | Proprietary                        |
| Delegation             | Recursive; shared tree so delegates cross-read evidence       | Subagents isolated; bounded result strings      | Subagents within CLI context                         | Proprietary multi-agent            |
| Configuration UX       | Declarative self-similar JSON (recursive)                     | YAML + code                                     | YAML + `.opencode`                                   | Not user-authored                  |

Net: **ProgressiveAgentSLM is the strongest on "where your experts live" (unbounded recoverable
memory) and on local-first capability-routed budgeting.** Weaknesses vs. Hermes: shipped/hardened
status and no skill-frontmatter progressive-disclosure. It is closer in spirit to "an SDK for building
a reusable, self-cultivating local domain-expert head."

## 4. Recommended revisions (applied)

1. **Accurate status admission** — the on-disk code in the previous home was the earlier design; the
   plan's `[~]` items read as "exists" but were not shipped. Marked `[]` / `[~]` correctly.
2. **New named owners** — `TokenCounter`, `bounded_io`, `run_clock`, `NoFindingsGuard`, `QuizEngine`
   added to Phase 2; `ApiServer`/health to Phase 3.
3. **Config loader** — `example-revised.json` is JSONC; `load_agent` builds a single self-similar
   JSON → full recursive tree.
4. **§8 risks added** — linked-history risk + always-on-store refresh guard.
5. **§15 case adds** — byte-identical stable-prefix assertion and a `bounded_io`/`run_clock` cost test.

## 5. What could be better (sharpest recs)

1. **Single self-similar JSON → full recursive tree** — the loader does this (Phase 3).
2. **Cost/run guard** — `run_clock` (`max_run_seconds`) + failover on slow forward passes.
3. **Real observability** — `GET /api/v1/health` as a Phase-3 deliverable.
4. **`bounded_io`** as a named helper used by every external read — done (Phase 0 port).
5. **Shared-`.db`/per-table contract** for `memory_data_stores`.
6. **`NoFindingsGuard`** — deterministic re-plan + refusal after consecutive empty retrievals.
7. **A curated "edge-case" store** — dedupe/archive/consolidate.
8. **`QuizEngine`** — a named owner for `self_evaluation_quizz`.

## 6. Design risks & judgment calls

- `known_edge_cases_knowledge` can become an unstructured dump → size/similarity flywheel.
- `design_decisions_knowledge` on every iteration fabricates "decisions" → gate on a sparse hook.
- A 15% `response_window` is tight on 8k models + a diagram → write the diagram to a file & link, or widen.
- Cloud escalation — keep `max_retries_until_switching_models` strictly infra/quality failover and
  prefer **local** general-purpose first in the default ladder.

## 7. Bottom line

- **Do not change the philosophy.** The thesis, the recursive agent, the unbounded recoverable memory,
  and prompt-cache discipline are all validated by Hermes/OpenCode/Claude alike.
- **Fix the gap between docs and code** — the `ProgressiveAgentSLM/` folder now scaffolds that; the
  remaining work is the Phase 0–4 core algorithms in `wip_checklist.md`.
- **The one thing that most improves the design**: the single self-similar JSON → full recursive tree
  (done in the loader), plus cost/observability + curator discipline.

**ProgressiveAgentSLM is, as designed, the right (not over-engineered) point on the curve — provided
the build phases are honored and the memory-discipline mechanics are treated as first-class.**

---

_Companion to [`design-review-summary.md`](design-review-summary.md) (one page) and
[`wip_checklist.md`](wip_checklist.md) (execution tracker)._
