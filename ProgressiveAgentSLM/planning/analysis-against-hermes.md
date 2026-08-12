# ProgressiveAgentSLM ⟷ Hermes — Comparative Analysis

> **Purpose.** Study the **Hermes Agent** harness (Nous Research, `ai-c4y/temp/hermes-agent`) and
> extract the good features, best practices, and shipped implementations that overlap with our
> **ProgressiveAgentSLM (ProgressiveSML)** design — so we can fold the proven ideas back into
> [planning.md](planning.md) and [design-principle.md](design-principle.md).

**Verdict up front.** Hermes independently arrived at ~80% of ProgressiveSML's architecture — tiered
context budget, background metadata/learning agent, progressive-disclosure skills, recursive
subagents, FTS5 session search, model-agnostic ladders, disciplined compaction. That convergence is
strong validation of our design. The _difference_ is that Hermes has **shipped and hardened** these
ideas, and in doing so learned lessons our plan hadn't accounted for yet — chiefly **prompt-cache
discipline**, **enforcement over prompting**, and **separation of iteration budget from model
failover**. Those are the things we stole.

## 1. What Hermes is (one paragraph)

Hermes is a production personal-AI-agent harness that runs one agent core across a CLI, a
multi-platform messaging gateway, a TUI, and a desktop app. It is model-agnostic (Portal / OpenRouter
/ OpenAI / local), self-improves across sessions (agent-curated memory + autonomously created skills),
delegates to isolated subagents, searches its own history, and runs scheduled jobs. Its two governing
principles are **"per-conversation prompt caching is sacred"** and **"the core is a narrow waist;
capability lives at the edges."** Both are directly relevant to us.

## 2. Feature-by-feature: Hermes ⟷ ProgressiveSML

| Hermes feature              | What it does                                                                                            | ProgressiveSML analog                       | Take-away for us                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Context breakdown**       | Typed context tiers (system/tools/rules/skills/…) with `char/4` estimates + a live `/context` grid      | `context_window_breakdown_percentages` (§3) | Use **`char/4` for both measure AND threshold**; ship a `/context` view.              |
| **Context engine ABC**      | Pluggable compaction lifecycle (`on_session_start → update_from_response → should_compress → compress`) | `Reflector` (§8)                            | Make `Reflector` a **pluggable engine**, not a hardcoded 50% call site.               |
| **Context compressor**      | Structured summary w/ Resolved/Pending, iterative summaries, tool-output pre-prune, tail protection     | Adaptive compaction (§3, §8)                | Replace "compact to 50%" with **iterative + goal-tracking**; prune stale tool output. |
| **Trajectory compressor**   | Protect first+last turns, compress only the middle, as much as needed                                   | Compaction (§3)                             | Compact **adaptively**, **protect head + tail**.                                      |
| **Prompt caching**          | Byte-stable prefix, cache breakpoints on real carriers                                                  | Stable prefix + volatile suffix (§3)        | **Biggest gap** — reorder tiers stable→volatile.                                      |
| **Iteration budget**        | Thread-safe consume/**refund**; parent 500 / subagent 50                                                | `CircularRounds` (§2, §4)                   | **Separate** "how much work" from "which model"; add **refund**.                      |
| **Subagent lifecycle**      | Immutable frozen contracts + state machine + byte caps                                                  | `delegates/contracts.py` (§7)               | Delegates get a **typed immutable boundary + restricted toolset + size caps**.        |
| **Learning loop / curator** | Background fork + curator pin/archive/consolidate, never deletes                                        | `Distiller` + curator (§8.2)                | Curate: lifecycle states, archive-not-delete, aux model.                              |
| **FTS5 session search**     | FTS5 + trigram + CJK, incremental merge, rebuild w/ progress                                            | `LogSearch` (§8)                            | Adopt **trigram tokenizer, incremental merge, query caps**.                           |
| **MoA + redaction**         | Mixture of Agents + PII redaction at egress                                                             | model ladder + `redact.py` (§8.2)           | **Always redact** before text crosses to another model.                               |
| **Tool guardrails**         | Idempotent-vs-mutating + repeat detection                                                               | `guards/tool_loop.py` (§5)                  | Add **loop detection** — SLMs loop hard on one tool.                                  |
| **Verification-on-stop**    | Turn-end "verify first" nudge; skips doc/markdown edits                                                 | `guards/verify_on_stop.py` (§5)             | Make `double_checking` an **enforced turn-end guard**.                                |
| **File safety**             | Sensitive-path deny-list beyond traversal                                                               | `tools/safety.py` (§10)                     | Add a **deny-list** (`.ssh`, `.env`, `/etc/*`).                                       |
| **Bounded reads**           | Byte cap + deadline on external reads                                                                   | `bounded_io.py` (§4)                        | **Bound every external read** with byte cap + deadline.                               |
| **Skills**                  | Progressive disclosure (frontmatter index → body on demand)                                             | `SkillTool` (§6)                            | **Prefer skills (on-demand) over always-present tools.**                              |

## 3. What Hermes validates in ProgressiveSML (keep doing)

- **Tiered, proportional context budget** — sound.
- **Background metadata/knowledge agent off the critical path** — the flagship self-improving pattern.
- **Recursive subagents routed by a capability description**.
- **FTS5 over an append-only history**.
- **Model-agnostic, local-first with cloud fallback**.
- **Embedded/file-based stores** — SQLite state local; `sqlite-vec` is aligned.

## 4. The three highest-value lessons

### 4.1 Prompt caching is sacred — a stable prefix is the biggest win

Hermes's #1 rule: the system-prompt prefix must be **byte-stable for the life of a conversation**,
because a long run reuses the cached prefix every turn and any mutation multiplies cost + latency.
Our original loop re-retrieved + reassembled the whole prompt each iteration. We now hold the
run-constant tiers byte-identical until a compaction — the single sanctioned cache-invalidation event.

### 4.2 Enforcement beats prompting

Small models ignore `when → then` prompt text. Hermes backs the critical policies with **enforced
turn-end guards**. We ship `double_checking` → verify-on-stop, `refusing_to_invent` → grounding gate,
anti-drift → tool-loop guard — all deterministic, in `guards/`.

### 4.3 Separate "how much work" from "which model"

Our original single budget conflated quality + infra + total work. We now keep two orthogonal budgets:
`max_retries_until_switching_models` (failover only) and a **separate `CircularRounds`** total-work cap
(with a **refund** for batched/tool turns) — Hermes's exact split.

## 5. Summary — the design deltas applied

1. **Protect the prompt-cache prefix** — stable prefix + volatile suffix; only compaction may rebuild. _(§3)_
2. **Enforce the critical policies in code** — turn-end guards, not prompt text. _(§5)_
3. **Split iteration budget from model failover** + add a **refund**. _(§2, §4)_
4. **Harden the boundaries** — typed delegate contracts, deny-lists, bounded reads, egress redaction. _(§6, §7, §10)_
5. **Upgrade compaction** to iterative goal-tracking with head+tail protection and adaptive target. _(§3, §8)_
6. **Adopt Hermes's FTS + memory-prefetch mechanics** wholesale. _(§6, §8)_

## 6. What ProgressiveSML solves that Hermes does _not_

All rooted in the different target (a bounded high-recall reasoning run over a fixed corpus on small
local models vs. a long-lived personal-assistant conversation):

1. **Unbounded, addressable memory** — Hermes's compaction is lossy; ours is recoverable (raw log +
   derived stores).
2. **A team that loops back over each other's raw work** — delegates share one tree vs. Hermes's
   isolated subagents that return a summary.
3. **A per-agent _proportional_ budget** that runs the same config on any model.

## 7. Better overall, or over-engineered?

**Neither strictly — a different, defensible point on the curve, with a real over-engineering risk in
the middle tiers.** The recoverable worklog, shared-memory delegation, and proportional budgeting are
genuinely better _for our target_. The graph-DB/vector mirrors + metadata-agent's five distilled fields
should stay **default-off and deferred to Phase 2+** (Hermes's "narrow waist" lesson). Build the thin
vertical slice first, prove it on real BVMS questions, then turn on the extras.

One simplification to adopt regardless: **keep the always-present tool/core surface tiny** and push
optional capability into on-demand skills.

---

_Companion to [planning.md](planning.md) and [design-principle.md](design-principle.md). Source studied:
`ai-c4y/temp/hermes-agent` (Nous Research, MIT). Written 2026-08-07._
