# ProgressiveAgentSLM ⟷ Hermes — Comparative Analysis

> **Purpose.** Study the **Hermes Agent** harness (Nous Research, `ai-c4y/temp/hermes-agent`) and
> extract the good features, best practices, and shipped implementations that overlap with our
> **ProgressiveAgentSLM (ProgressiveSML)** design — so we can fold the proven ideas back into
> [planning.md](planning.md) and [design-principle.md](design-principle.md).
>
> _(Filename note: requested as `analysis-againstr-hermes.md`; saved as `analysis-against-hermes.md`
> — obvious typo corrected. Rename if you truly want the original spelling.)_

**Verdict up front.** Hermes independently arrived at ~80% of ProgressiveSML's architecture — tiered
context budget, background metadata/learning agent, progressive-disclosure skills, recursive
subagents, FTS5 session search, model-agnostic ladders, disciplined compaction. That convergence is
strong validation of our design. The _difference_ is that Hermes has **shipped and hardened** these
ideas, and in doing so learned lessons our plan hasn't accounted for yet — chiefly **prompt-cache
discipline**, **enforcement over prompting**, and **separation of iteration budget from model
failover**. Those are the things worth stealing.

---

## 1. What Hermes is (one paragraph)

Hermes is a production personal-AI-agent harness that runs one agent core across a CLI, a
multi-platform messaging gateway, a TUI, and a desktop app. It is model-agnostic (Portal / OpenRouter
/ OpenAI / local), self-improves across sessions (agent-curated memory + autonomously created skills),
delegates to isolated subagents, searches its own history, and runs scheduled jobs. Its two governing
principles — declared in [AGENTS.md](temp/hermes-agent/AGENTS.md) — are **"per-conversation prompt
caching is sacred"** and **"the core is a narrow waist; capability lives at the edges."** Both are
directly relevant to us.

---

## 2. Feature-by-feature: Hermes ⟷ ProgressiveSML

| Hermes feature (file)                                                                                                                                                                     | What it does                                                                                                                                                                                                                                         | ProgressiveSML analog (planning §)               | Take-away for us                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Context breakdown** ([context_breakdown.py](temp/hermes-agent/agent/context_breakdown.py))                                                                                              | Attributes every prompt request into typed tiers (system / tools / rules / skills / mcp / subagents / memory / conversation) with `char/4` token estimates + a live `/context` glyph grid.                                                           | `context_window_breakdown` four-tier budget (§3) | Adopt the **same `char/4` heuristic for measure AND threshold** (resolves Open Q#8). Ship a `/context` observability view. |
| **Context engine ABC** ([context_engine.py](temp/hermes-agent/agent/context_engine.py))                                                                                                   | Pluggable compaction engine with a clean lifecycle (`on_session_start` → `update_from_response` → `should_compress` → `compress`).                                                                                                                   | `Reflector` (§8, Phase 0/1)                      | Make our `Reflector` a **pluggable engine with this exact lifecycle**, not a hardcoded 50% call site.                      |
| **Context compressor** ([context_compressor.py](temp/hermes-agent/agent/context_compressor.py))                                                                                           | Structured summary w/ **Resolved/Pending** tracking, **iterative** summaries (each compaction updates the last), tool-output pre-pruning, token-budget tail protection, "historical/reference-only" headings so summaries don't read as live orders. | 50% progressive reflection (§3, §8)              | Replace "compact to 50%" with **iterative + goal-tracking** summaries; prune stale tool output first; use aux model.       |
| **Trajectory compressor** ([trajectory_compressor.py](temp/hermes-agent/trajectory_compressor.py))                                                                                        | Protect first turns + last N turns, compress **only the middle**, only **as much as needed** to hit target, replace with one summary.                                                                                                                | Compaction (§3 core-loop invariant)              | Compact **adaptively** (only enough to fit), not a fixed 50%; always **protect head + tail**.                              |
| **Prompt caching** ([prompt_caching.py](temp/hermes-agent/agent/prompt_caching.py), [system_prompt.py](temp/hermes-agent/agent/system_prompt.py))                                         | 3-tier system prompt (`stable` / `context` / `volatile`), byte-stable prefix for the whole session, cache breakpoints placed on real carriers.                                                                                                       | Four-tier prompt assembly (§3)                   | **Biggest gap** — see §4.1. Reorder tiers stable→volatile so the cacheable prefix never mutates mid-run.                   |
| **Iteration budget** ([iteration_budget.py](temp/hermes-agent/agent/iteration_budget.py))                                                                                                 | Thread-safe consume/**refund** counter; parent cap 500, subagent cap 50; programmatic (batched) tool turns are refunded.                                                                                                                             | `max_retries_until_switching_models` (§4)        | **Separate** the "how much work" budget from "which model" failover (see §4.3). Add **refund** for batched calls.          |
| **Subagent lifecycle** ([subagent_lifecycle.py](temp/hermes-agent/agent/subagent_lifecycle.py))                                                                                           | Immutable frozen-dataclass contracts (`LaunchRequest`/`Handle`/`Status`/`Result`), explicit state machine, `depth`, `role`, `allowed_toolsets`/`blocked_tools`, input/result byte caps, HMAC-signed handles, terminal retention.                     | `delegates` recursive agents (§7)                | Give delegates a **typed immutable boundary + state machine + restricted toolset + size caps**, not raw agent objects.     |
| **Learning loop** ([background_review.py](temp/hermes-agent/agent/background_review.py), [curator.py](temp/hermes-agent/agent/curator.py))                                                | Post-turn **background fork** decides what memory/skills to persist; a periodic **curator** pins/archives/consolidates skills. Never touches the main prompt cache; **never auto-deletes (archive-only)**.                                           | MetadataAgent → `knowledge_graph.jsonl` (§8.2)   | Our metadata agent should also **curate**: lifecycle states, archive-not-delete, run on aux model off critical path.       |
| **Skills = progressive disclosure** ([SKILL.md](temp/hermes-agent/skills/software-development/systematic-debugging/SKILL.md), [learn_prompt.py](temp/hermes-agent/agent/learn_prompt.py)) | Frontmatter (`name`, **`description` ≤60 chars**, `platforms`, `related_skills`, `tags`) always visible; body loads on demand; standardized section order; **no pagination on instructional content**.                                               | `SkillTool` (§6)                                 | Copy the **frontmatter schema + 60-char index rule + section order**; forbid `offset/limit` on skill/prompt reads.         |
| **Learning graph** ([learning_graph.py](temp/hermes-agent/agent/learning_graph.py))                                                                                                       | Builds a graph from skills (`related_skills`) + memory nodes via lexical overlap; renders "what I've learned."                                                                                                                                       | `knowledge_graph` relationships (§8.2, §8.3)     | Our KG can seed edges from `related_skills` + lexical overlap **before** an LLM pass — cheap first, LLM only if hard.      |
| **Session search (FTS5)** ([hermes_state_search.py](temp/hermes-agent/hermes_state_search.py))                                                                                            | FTS5 + trigram + CJK over the session DB; **incremental bounded merge**, **deferred resumable rebuild w/ progress**, query char caps.                                                                                                                | `LogSearch` FTS5 over worklog (§8, Phase 2)      | Adopt **trigram tokenizer**, **incremental merge** (don't block writes), **query caps**, **resumable rebuild**.            |
| **Mixture of Agents** ([moa_loop.py](temp/hermes-agent/agent/moa_loop.py))                                                                                                                | Gathers parallel reference-model outputs, aggregator combines them; strong **PII/secret redaction at the LLM egress boundary**.                                                                                                                      | `parallel_supprocess` + model ladder (§2, §4)    | Optional MoA mode for hard steps; **always redact secrets/PII before text crosses to another model**.                      |
| **Memory manager** ([memory_manager.py](temp/hermes-agent/agent/memory_manager.py))                                                                                                       | Single integration point; **only ONE external provider** (avoids tool-schema bloat); background prefetch pre-turn / sync post-turn with bounded drain; schema normalization.                                                                         | `VectorMemoryTool` (§6)                          | **Prefetch memory in background pre-turn, sync post-turn**; cap providers to avoid prompt bloat.                           |
| **Tool guardrails** ([tool_guardrails.py](temp/hermes-agent/agent/tool_guardrails.py))                                                                                                    | Classifies tools idempotent vs mutating; **detects per-turn tool-call loops** (same call repeated) → warn / synthetic result / halt.                                                                                                                 | Tool `when` menu-pruning (§6, §7)                | Add **loop detection** — SLMs loop hard on the same tool. This is enforcement our prompt-only design lacks.                |
| **Verification-on-stop** ([verification_stop.py](temp/hermes-agent/agent/verification_stop.py))                                                                                           | If the model tries to finish right after editing code with no fresh test evidence, inject a bounded "verify first" nudge; **skips doc/markdown edits**.                                                                                              | `double_check` cognitive_behavior policy (§5)    | Make `double_check` an **enforced turn-end guard**, not a prompt suggestion SLMs ignore. See §4.2.                         |
| **File safety** ([file_safety.py](temp/hermes-agent/agent/file_safety.py))                                                                                                                | Explicit **deny-list** of sensitive paths/prefixes (`.ssh`, `.env`, `.aws`, `/etc/passwd`, credential stores) on top of traversal checks.                                                                                                            | Traversal/absolute-escape rejection (§6, §10)    | Add a **content-based sensitive-path deny-list** — traversal rejection alone doesn't stop reading `~/.ssh/id_rsa`.         |
| **Bounded reads** ([bounded_response.py](temp/hermes-agent/agent/bounded_response.py))                                                                                                    | Byte cap + hard wall-clock deadline on external reads, worker thread to interrupt stalled sockets.                                                                                                                                                   | Ollama/OpenRouter clients (§4, Phase 4)          | **Bound every external read** (HTTP + tool output) with byte cap + deadline; SLM endpoints stall.                          |
| **Context references** ([context_references.py](temp/hermes-agent/agent/context_references.py))                                                                                           | `@file:` / `@folder:` / `@git:` / `@url:` inline expansion with injected-token accounting + sensitive-ref blocking.                                                                                                                                  | `working_folders` + `ReadFileTool` (§2, §6)      | Add **@-mention expansion** with token accounting so users pull source into `current_working_attention` explicitly.        |
| **Narrow-waist / footprint ladder** ([AGENTS.md](temp/hermes-agent/AGENTS.md))                                                                                                            | Every core tool ships on every API call → keep the core tiny; prefer skill/CLI/plugin over new core tools.                                                                                                                                           | Tool menu-pruning by `when` (§6, §7)             | Validates our pruning; go further — **prefer skills (on-demand) over always-present tools** to keep the prompt lean.       |

---

## 3. What Hermes validates in ProgressiveSML (keep doing)

These ProgressiveSML decisions are independently confirmed by a shipped system — don't second-guess
them:

- **Tiered, proportional context budget** — Hermes categorizes context the same way; our fractional
  tiers are sound.
- **Background metadata/knowledge agent off the critical path** — Hermes's post-turn background review
  is exactly this pattern, and it's their flagship "self-improving" feature.
- **Progressive-disclosure skills** — Hermes ships the identical frontmatter-index-then-load-body model
  and is compatible with the `agentskills.io` standard we should target.
- **Recursive subagents routed by a capability description** — Hermes delegates via `delegate_task`
  with a goal + role, matching our "route by `description`" contract.
- **FTS5 over an append-only history** — Hermes's session DB + FTS5 mirrors our worklog + `LogSearch`.
- **Model-agnostic, local-first with cloud fallback** — Hermes's provider abstraction validates our
  `models` ladder.
- **Embedded/file-based stores** — Hermes keeps SQLite session state local; our `sqlite-vec` decision
  (Open Q#16) is aligned.

---

## 4. The three highest-value lessons (where Hermes knows something we don't)

### 4.1 Prompt caching is sacred — our every-iteration rebuild is the biggest risk

Hermes's #1 architectural rule: **the system-prompt prefix must be byte-stable for the life of a
conversation**, because a long run reuses the cached prefix every turn and any mutation multiplies cost
and latency. They split the system prompt into `stable → context → volatile` precisely so the
cacheable front never changes ([system_prompt.py](temp/hermes-agent/agent/system_prompt.py)), and place
cache breakpoints deliberately ([prompt_caching.py](temp/hermes-agent/agent/prompt_caching.py)).

ProgressiveSML's core loop (§3) does the opposite: **every iteration** it re-retrieves blocks via
`cognitive_index` and **reassembles the whole four-tier prompt**, including the `cognitive_reflection_behavior`
tier that holds `system_prompt` + policies + tool descriptions. That churns the prefix every step.

**Why it matters even for local SLMs:** Ollama/llama.cpp reuse the **KV cache** for a stable prompt
prefix. A prefix that changes every iteration forces a full prompt re-evaluation (prefill) each time —
on a 20B model over a 62k window that is the dominant latency cost. This is a _local_ performance
problem, not just a cloud billing one.

**Recommendation (update §3):**

- Split our prompt into a **stable prefix** (`system_prompt` + `cognitive_behavior` policies + tool
  descriptions + delegate descriptions — these are per-run constants) and a **volatile suffix** (the
  retrieved blocks, `current_working_attention`, the question, the answer).
- Only the volatile suffix changes per iteration. Keep the stable prefix byte-identical until a
  compaction genuinely forces a rebuild.
- Add a note to Open Questions: **compaction is the one sanctioned cache-invalidation event** (Hermes's
  exact carve-out).

### 4.2 Enforcement beats prompting — SLMs ignore `when → then` policies

Our `cognitive_behavior` (§5) is **prompt-only**: rules rendered into the system prompt each iteration.
Hermes learned that small models _do not reliably obey_ prompt-only guidance, so its equivalents are
**enforced in code at turn boundaries**:

- `double_check` → **verification-on-stop** ([verification_stop.py](temp/hermes-agent/agent/verification_stop.py)):
  if the model tries to stop after editing code with no fresh evidence, the loop **injects a bounded
  follow-up turn** — it doesn't merely _ask_ the model to double-check.
- anti-drift → **tool-loop guardrails** ([tool_guardrails.py](temp/hermes-agent/agent/tool_guardrails.py)):
  repeated identical tool calls are detected and warned/halted deterministically.

**Recommendation (update §5, §12 Phase 2):** keep `cognitive_behavior` as the declarative surface, but
back the critical policies with **enforced hooks** in the loop:

- `double_check` → a turn-end guard that blocks "done" until the evidence actually covers the question
  (reuse `AnswerEvaluator`) and injects one more retrieval round if not.
- `say_no` → a grounding check: if retrieval returned nothing above a similarity floor, force the
  honest-refusal branch rather than trusting the SLM to choose it.
- add a **tool-loop guard** (idempotent-vs-mutating classification + repeat detection) so a small model
  can't spin on `SqliteVector` forever.

### 4.3 Separate "how much work" from "which model" — our single budget conflates them

ProgressiveSML folds _quality failures_ and _infra failures_ and _total work_ into one counter,
`max_retries_until_switching_models` (§4, Open Q#3/#4). Hermes keeps two orthogonal mechanisms:

- **IterationBudget** ([iteration_budget.py](temp/hermes-agent/agent/iteration_budget.py)) — a
  thread-safe cap on _total_ iterations (parent 500 / subagent 50), with a **refund** so programmatic /
  batched tool turns don't burn the budget.
- **Model failover** — a separate concern handled by the error classifier / provider ladder.

Conflating them means a run that's making real progress but keeps failing self-eval on the _same_ model
can exhaust the ladder and stop, even though more _iterations_ were warranted (or vice-versa).

**Recommendation (update §4, §2):**

- Keep `max_retries_until_switching_models` strictly as the **model-switch trigger**.
- Add a distinct **`ParallelExecutor`/loop-level `IterationBudget`** (we already list `ParallelExecutor`
  in §11) as the _total-work_ cap, with a **refund** for batched/programmatic tool calls.
- Bound a deep delegate tree by **per-subagent iteration caps** (Hermes's 50-vs-500 split), not only by
  ladder length.

---

## 5. Concrete, lower-effort wins to fold in

| #   | Change                                                                                                                                                                      | Where in planning.md   |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| 1   | Use `char/4` for **both** budget measurement and compaction threshold; ship a `/context` breakdown view.                                                                    | §3, Open Q#8           |
| 2   | Make `Reflector` a **pluggable engine** with `should_compress()/compress()` lifecycle.                                                                                      | §11, Phase 0           |
| 3   | Compaction = **iterative summary** (update, don't replace) with **Resolved/Pending** tracking + tool-output pre-prune + adaptive target.                                    | §3, §8                 |
| 4   | Delegates get **immutable dataclass contracts + state machine + restricted toolset + goal/result byte caps**.                                                               | §7, §11                |
| 5   | Skills adopt Hermes frontmatter (**`description` ≤60 chars index**, `related_skills`, `platforms`, `tags`) + fixed section order; **no pagination** on instructional reads. | §6 `SkillTool`         |
| 6   | Seed `knowledge_graph` edges from `related_skills` + lexical overlap **before** any LLM call (cheap-first).                                                                 | §8.2                   |
| 7   | `LogSearch`: **trigram tokenizer**, **incremental merge**, **query char caps**, **resumable rebuild w/ progress**.                                                          | §8, Phase 2            |
| 8   | Add a **sensitive-path deny-list** (`.ssh`, `.env`, credentials, `/etc/*`) to file tools, beyond traversal checks.                                                          | §6, §10 tool safety    |
| 9   | **Bound every external read** (Ollama/OpenRouter/tool output) with byte cap + wall-clock deadline.                                                                          | §4, Phase 4            |
| 10  | Memory: **background prefetch pre-turn, background sync post-turn**, bounded drain; one writable provider.                                                                  | §6 `VectorMemoryTool`  |
| 11  | **Redact secrets/PII** before any block text crosses to another model (metadata agent, MoA, cloud escalation).                                                              | §8.2, §4               |
| 12  | Optional **@-mention** (`@file:`/`@folder:`) expansion with injected-token accounting.                                                                                      | §2 working_folders, §6 |

---

## 6. Notable Hermes ideas that are out-of-scope for ProgressiveSML (context only)

Not recommendations — just so we know what we're deliberately _not_ copying:

- **Multi-platform gateway** (Telegram/Discord/Slack/…): Hermes is a personal assistant; ProgressiveSML
  is a domain-RAG reasoning engine. Not relevant.
- **Cron scheduler / unattended automations**: interesting but orthogonal to a per-question RAG run.
- **Seven terminal backends (Docker/SSH/Modal/Daytona/…)** and **browser control**: Hermes drives real
  environments; our tools stay sandboxed to `worklog_folder` + read-only `working_folders`.
- **Trajectory generation for training** ([trajectory_compressor.py](temp/hermes-agent/trajectory_compressor.py)):
  relevant only if we pursue the _optional_ distillation phase in [design-principle.md](design-principle.md) §7.

---

## 7. Summary — the design deltas to apply

1. **Protect the prompt-cache prefix** — reorder the four-tier prompt into a stable prefix + volatile
   suffix; only compaction may rebuild the prefix. _(biggest change; §3)_
2. **Enforce the critical policies in code** — `double_check`, `say_no`, and anti-loop become turn-end
   guards, not just prompt text. _(§5)_
3. **Split iteration budget from model failover**, and add a **refund** for batched tool calls. _(§2, §4)_
4. **Harden the boundaries** — typed immutable delegate contracts, sensitive-path deny-lists, bounded
   external reads, egress redaction. _(§6, §7, §10)_
5. **Upgrade compaction** to iterative goal-tracking summaries with head+tail protection and adaptive
   target. _(§3, §8)_
6. **Adopt Hermes's skill + FTS + memory-prefetch mechanics** wholesale — they're mature and match our
   plan almost exactly. _(§6, §8)_

Everything else in ProgressiveSML is confirmed by Hermes's convergent, shipped design and should
proceed as planned.

> **Status (2026-08-07): all six deltas applied** to [planning.md](planning.md) (new revision note +
> edits to §2, §3, §4, §5, §7, §8.2, §10, §11, §12, §16) and [design-principle.md](design-principle.md) §6.

---

## 8. What ProgressiveSML solves that Hermes does _not_

Convergence aside, our design deliberately answers three problems Hermes's architecture leaves on the
table — all rooted in the **different target**: Hermes optimizes a _long-lived personal-assistant
conversation_ on capable (often cloud) models; ProgressiveSML optimizes a _bounded, high-recall
reasoning run over a fixed corpus_ on small local models.

1. **Unbounded, addressable memory vs. a linear conversation Hermes must keep compressing.**
   Hermes's context is one growing message list; when it fills, the compressor **summarizes the middle
   and the detail is gone** ([context_compressor.py](temp/hermes-agent/agent/context_compressor.py),
   [trajectory_compressor.py](temp/hermes-agent/trajectory_compressor.py)) — lossy by construction. Our
   **segmented append-only worklog + `cognitive_index`** ([planning §8](planning.md)) makes compaction
   touch only the _derived_ working view: every original block stays on disk and is one
   `{segment, offset}` seek away. **Compaction is lossy for Hermes; for us it is recoverable.** For a
   corpus assistant that must not "forget" a rule it read 30 iterations ago, this is the bigger win.

2. **A team that loops back over each other's raw work vs. subagents that only return a summary.**
   Hermes subagents are **isolated** and hand back a bounded result string
   ([subagent_lifecycle.py](temp/hermes-agent/agent/subagent_lifecycle.py) `_MAX_RESULT_CHARS`); the
   parent never sees the child's evidence, only its conclusion. Our delegates share **one worklog**, so
   any later agent can retrieve a teammate's _original_ blocks by index — the code delegate's evidence
   and the docs delegate's rules are cross-readable, not just their summaries. That's a strictly richer
   collaboration model for multi-faceted questions ("how does approval work _and_ where is it coded").

3. **A per-agent _proportional_ budget that runs the same config on any model vs. a fixed context knob.**
   Hermes tunes to a model's context length and protects a fixed head (`protect_first_n`). Our
   `context_window_breakdown` is expressed as **fractions of the active model's `max_tokens`**
   ([planning §3](planning.md)), so the _same_ agent spec runs unchanged on a 20B/62k local model or a
   cloud model with 10× the window — every tier scales automatically. This matters precisely because we
   escalate _within one run_ across a heterogeneous ladder; Hermes swaps models between conversations.

Secondary things we specify that Hermes leaves implicit: a **background knowledge-graph** with typed
`relationships` per block (Hermes's `learning_graph` is skill/memory-level, not per-block), optional
**embedded graph/vector mirrors** for cross-run recall, and a **declarative single-object config**
(JSON _or_ Python) that a non-programmer can author — Hermes capability lives in code, plugins, and
`config.yaml` fragments.

## 9. Better overall, or over-engineered?

**Neither strictly — it's a _different, defensible_ point on the design curve, with a real
over-engineering risk in the middle tiers.** Honest read:

- **Where it is genuinely better _for its target_:** the recoverable worklog (§8.1), shared-memory
  delegation (§8.2), and proportional budgeting (§8.3) are not gratuitous — they directly serve
  "high-recall reasoning over a fixed corpus on small models," which is a harder memory problem than
  Hermes's. On that axis ProgressiveSML is the stronger design.
- **Where the over-engineering risk is real:** the **knowledge_graph → optional Kuzu/graph-DB +
  vector-DB mirrors** (§8.3) and the **metadata agent's five distilled fields per block** are a lot of
  moving parts to build and keep correct _before_ we've proven the core loop earns its keep. Hermes's
  lesson — **"the core is a narrow waist; capability lives at the edges"** — is the corrective: these
  should stay **default-off and deferred to Phase 2+**, exactly as planned, and we should resist
  shipping them until the file-only path demonstrably falls short. Two RAG delegates + a recoverable
  worklog is already a useful assistant (design-principle §7 build order agrees).
- **The pragmatic verdict:** build the **thin vertical slice first** (Phase 1: one agent, four-tier
  prompt with the new stable-prefix, SqliteVector tool, segmented worklog, `cognitive_index`), prove it
  on real BVMS questions, and only then turn on the metadata agent, the DB mirrors, and MoA. If we hold
  that discipline, ProgressiveSML is **better-suited, not over-engineered**. If we build the whole §8
  stack up front, it tips into over-engineered. The plan already sequences it correctly — the risk is
  execution discipline, not the design.

One concrete simplification worth adopting from Hermes regardless: **keep the always-present tool/core
surface tiny** and push everything optional into on-demand **skills** (progressive disclosure), so the
stable prefix — and the SLM's attention — stays lean.

---

_Companion to [planning.md](planning.md) and [design-principle.md](design-principle.md). Source studied:
`ai-c4y/temp/hermes-agent` (Nous Research, MIT). Written 2026-08-07._
