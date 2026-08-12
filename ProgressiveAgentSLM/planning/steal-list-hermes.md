# Steal List — What to Port from Hermes into ProgressiveAgentSLM

> **Purpose.** Hermes (Nous Research, MIT) is at `ai-c4y/temp/hermes-agent` (in the _previous_ home) —
> and now, per the porting map below, its immediately-usable primitives land in **this** project
> (`ProgressiveAgentSLM/src/framework/`). This is the concrete, file-by-file porting list — what to
> steal _immediately_, what to adapt, and what to skip — grounded in the actual source.
>
> **How to use.** Each row names the Hermes file, the exact primitive to port, the target in our
> `src/framework/`, and the porting effort. "Steal" = copy the pattern/algorithm (MIT license, keep the
> attribution header); "adapt" = rework to our config/loop; "skip" = deliberately out of scope.
>
> **License note.** Hermes is MIT. Porting the _pattern_ is fine; if you copy substantial code, keep the
> original copyright header and add a `# Ported from hermes-agent (MIT)` comment.
>
> **Date:** 2026-08-12 · Companion to [`analysis-against-hermes.md`](analysis-against-hermes.md) and
> [`review-revise-design.md`](review-revise-design.md).

---

## 0. The shortlist — steal these _now_ (highest value / lowest effort)

| #   | Hermes file                                         | What to steal                                                                                                                                                          | Our target                                                                             | Effort                                          |
| --- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------- |
| 1   | `agent/bounded_response.py`                         | **Byte-cap + wall-clock-deadline read** (worker-thread drain so a stalled socket can't hang the run; returns partial bytes on timeout; never raises on the error path) | `src/framework/bounded_io.py` — the `bounded_io` helper from the review                | **S** — near drop-in                            |
| 2   | `agent/iteration_budget.py`                         | **Thread-safe consume/refund iteration counter** (parent cap 500 / subagent 50; `refund()` for batched/programmatic tool turns)                                        | `src/framework/CircularRounds.py` + the `behavior_policies_max_circular_rounds` budget | **S** — near drop-in                            |
| 3   | `agent/file_safety.py`                              | **Sensitive-path deny-list** (`build_write_denied_paths` / `build_write_denied_prefixes`: `.ssh`, `.aws`, `.env`, `/etc/*`, credential stores) + safe-root resolution  | `src/framework/tools/safety.py` — the §10 deny-list                                    | **S** — near drop-in                            |
| 4   | `agent/redact.py`                                   | **Regex secret redaction** (API-key prefixes, sensitive query params / body keys, short-token full-mask, long-token head/tail preserve)                                | `src/framework/redact.py` — the §8.2 egress redaction                                  | **S** — near drop-in                            |
| 5   | `agent/tool_guardrails.py`                          | **Tool-loop guard** (idempotent-vs-mutating classification, `ToolCallSignature` = name + canonical-args hash, warn/block/halt thresholds, per-turn caps)               | `src/framework/guards/tool_loop.py` — the anti-drift guard                             | **M** — pure logic, adapt thresholds            |
| 6   | `agent/verification_stop.py`                        | **Verify-on-stop** (turn-end guard: if the model tries to finish with no fresh evidence, inject a bounded follow-up; skips doc/markdown edits)                         | `src/framework/guards/verify_on_stop.py` — the `double_checking` guard                 | **M** — adapt to "evidence covers the question" |
| 7   | `agent/context_engine.py`                           | **Pluggable context-engine ABC** (`on_session_start → update_from_response → should_compress → compress → on_session_end`) + `sanitize_memory_context`                 | `src/framework/Reflector.py` — the pluggable compaction engine                         | **M**                                           |
| 8   | `agent/context_breakdown.py`                        | **`char/4` token estimate + live `/context` breakdown**                                                                                                                | `src/framework/tokens.py` (`TokenCounter`) + the §7b health surface                    | **S**                                           |
| 9   | `agent/prompt_caching.py`                           | **Cache-marker placement** (stable prefix → volatile suffix; breakpoints on real carriers)                                                                             | `src/framework/prompt_assembly.py` — stable-prefix/volatile-suffix assembly            | **M**                                           |
| 10  | `agent/subagent_lifecycle.py`                       | **Immutable delegate contracts** (request/handle/status/result, state machine, depth, role, allowed/blocked tools, byte caps)                                          | `src/framework/delegates/contracts.py` — the §7 typed boundary                         | **M**                                           |
| 11  | `hermes_state_search.py` + `hermes_state_common.py` | **FTS5 + trigram + CJK search** (incremental bounded merge, query char caps, resumable rebuild)                                                                        | `src/framework/memory/LogSearch.py`                                                    | **M**                                           |
| 12  | `agent/curator.py`                                  | **Background curator** (aux-model, inactivity-triggered, pin/archive/consolidate, never auto-deletes)                                                                  | `src/framework/memory/curator.py` — the curation flywheel                              | **M**                                           |

---

## 1. Steal now — the "bounded I/O" trio (highest value)

### 1.1 `bounded_response.py` → `src/framework/bounded_io.py`

**Why it's the #1 steal.** Our plan (§4, §10) says "every model / tool read is capped by bytes +
wall-clock deadline" but has no implementation. Hermes's `read_streaming_error_body` is the exact
pattern, and it's **self-contained** (only depends on `httpx` + `threading`).

**The key insight to copy:** a wall-clock check _between_ yielded chunks can't interrupt a socket read
that stalls mid-chunk (control never returns to Python until httpx's own 30s+ timeout). So the read runs
on a **daemon worker thread** and the caller waits with a hard deadline; on timeout, close the response
(which unblocks the read) and return partial bytes. **Never raises on the error path.**

### 1.2 `iteration_budget.py` → `src/framework/CircularRounds.py`

**Why.** Our `behavior_policies_max_circular_rounds` (default 5) is the total-work budget, but the plan
has no counter class. Hermes's `IterationBudget` is a **thread-safe consume/refund counter** — exactly
the `CircularRounds` item in Phase 0.

**The key insight to copy:** `refund()` for **programmatic/batched tool turns** — a tool call that the
loop itself issued (not the model) shouldn't burn the model's iteration budget.

### 1.3 `file_safety.py` → `src/framework/tools/safety.py`

**Why.** Our §10 says "sensitive-path deny-list" but `ReadFileTool.py` on disk is a bare `open()`.
Hermes's `build_write_denied_paths` / `build_write_denied_prefixes` is the exact list, and it's
**self-contained** (only `os`/`pathlib`).

**The key insight to copy:** two layers — **exact paths** (`.ssh/id_rsa`, `.env`, `.netrc`, `.pgpass`,
`.npmrc`, `.pypirc`, `.git-credentials`, `/etc/sudoers`, `/etc/passwd`, `/etc/shadow`) and **directory
prefixes** (`.ssh/`, `.aws/`, `.gnupg/`, `.kube/`, `.docker/`, `.azure/`, `.config/gh/`,
`.config/gcloud/`, `/etc/sudoers.d/`, `/etc/systemd/`). Plus a **safe-root** allowlist
(`HERMES_WRITE_SAFE_ROOT`-style).

---

## 2. Steal now — the "enforcement" trio (the §5 guards)

### 2.1 `tool_guardrails.py` → `src/framework/guards/tool_loop.py`

**The key insight to copy:** a **stable, non-reversible signature** for a tool call = `tool_name` +
`sha256(canonical_args)` — so "same tool, same args" is detected deterministically, and the signature's
`to_metadata()` never leaks raw argument values. Plus **per-turn caps** (`LoopCapConfig`: max web
searches / max subagents per turn).

### 2.2 `verification_stop.py` → `src/framework/guards/verify_on_stop.py`

**The key insight to copy:** the **doc/markdown skip** — `_NON_CODE_VERIFY_EXTENSIONS` (`.md`,
`.markdown`, `.mdx`, `.rst`, `.txt`, `.adoc`, `.log`, `.csv`, …). A turn that touches _only_ prose must
never demand a verification round. For us: a turn that only wrote `todo.md` or a Mermaid `.md` must not
trigger `double_checking`.

### 2.3 `context_engine.py` → `src/framework/Reflector.py`

**The key insight to copy:** the engine is **pluggable** (config-driven `context.engine`, default
`"compressor"`) — so our `Reflector` becomes an interface, not a hardcoded 50% call site. Also steal
`sanitize_memory_context`: **redact + head/tail truncate at the egress boundary**.

---

## 3. Steal now — the "context & memory" trio

### 3.1 `context_breakdown.py` → `src/framework/tokens.py` + health surface

**The key insight to copy:** the breakdown is **computed from the same parts the prompt builder uses**
(`build_system_prompt_parts` → `stable`/`context`/`volatile`), so the numbers _always_ match what's
actually sent — not a separate estimate. `_chars_to_tokens` = `(len(text) + 3) // 4`.

### 3.2 `prompt_caching.py` → `src/framework/prompt_assembly.py`

**The key insight to copy:** **breakpoints land on real carriers** — skip empty-content messages
(assistant turns that are pure tool_calls, empty tool messages) because a marker there is ignored and
wastes one of the four breakpoints. For Ollama/llama.cpp the "marker" is just _byte-identical prefix_.

### 3.3 `hermes_state_search.py` + `hermes_state_common.py` → `src/framework/memory/LogSearch.py`

**The key insight to copy:** **incremental bounded merge** (`_try_incremental_merge_fts` runs one bounded
merge pass _without failing the completed write_ — maintenance is best-effort, never blocks writes), and
**query char caps** (`MAX_FTS5_QUERY_CHARS`).

---

## 4. Steal now — the "delegation & curation" pair

### 4.1 `subagent_lifecycle.py` → `src/framework/delegates/contracts.py`

**The key insight to copy:** the **byte caps** (`_MAX_GOAL_CHARS = 16_000`, `_MAX_CONTEXT_CHARS = 32_000`,
`_MAX_RESULT_CHARS = 32_000`) and the **state machine** (`PENDING → STARTING → RUNNING → SUCCEEDED |
FAILED | INTERRUPTED | CANCELLED`). The parent never hands a child a live agent object.

### 4.2 `curator.py` → `src/framework/memory/curator.py`

**The key insight to copy:** the **invariants** — only touches agent-created records, **never auto-deletes
(archive is recoverable)**, pinned records bypass auto-transitions, runs on the **auxiliary client**.
For us: the `is_memory_distillation` endpoint, off the critical path.

---

## 5. Steal later / adapt (lower priority, still valuable)

| Hermes file                                       | What                                                                 | Our target                                       | When      |
| ------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------ | --------- |
| `agent/memory_manager.py`                         | Background prefetch pre-turn / sync post-turn; one writable provider | `src/framework/memory/MemoryStores.py`           | Phase 2   |
| `agent/learning_graph.py`                         | Skill/memory graph via lexical overlap, cheap-first                  | `src/framework/memory/` (the `distill_from` DAG) | Phase 2   |
| `agent/moa_loop.py`                               | MoA for hard steps + PII redaction at egress                         | `src/framework/` (optional)                      | Phase 4   |
| `agent/context_references.py`                     | `@file:`/`@folder:` expansion with token accounting                  | `src/framework/tools/`                           | Phase 2   |
| `agent/error_classifier.py`                       | Classify infra vs. quality failures (drives the ladder)              | `src/framework/ModelChain.py`                    | Phase 0/1 |
| `agent/retry_utils.py`                            | 429/backoff retry                                                    | `src/framework/ModelChain.py`                    | Phase 4   |
| `agent/auxiliary_client.py`                       | Aux-model client (for distillation/curator)                          | `src/framework/ModelChain.py`                    | Phase 2   |
| `agent/stream_single_writer.py`                   | Single-writer stream (no interleaving)                               | `src/framework/logging/RunLogger.py`             | Phase 1   |
| `agent/turn_summary.py`                           | Per-turn summary (feeds the raw log)                                 | `src/framework/memory/RawLog.py`                 | Phase 1   |
| `agent/context_compressor.py`                     | Iterative summary w/ Resolved/Pending + tool-output pre-prune        | `src/framework/Reflector.py`                     | Phase 2   |
| `agent/trajectory_compressor.py`                  | Protect head+tail, compress only middle, adaptive target             | `src/framework/Reflector.py`                     | Phase 2   |
| `agent/verification_evidence.py`                  | Passive verification ledger (feeds verify-on-stop)                   | `src/framework/guards/`                          | Phase 2   |
| `agent/skill_utils.py` / `skill_preprocessing.py` | Skill frontmatter + progressive disclosure                           | `src/framework/tools/SkillTool.py`               | Phase 2   |
| `agent/redact.py` (full)                          | The complete regex set (API keys, query params, body keys)           | `src/framework/redact.py`                        | Phase 2   |

---

## 6. Skip (deliberately out of scope)

| Hermes file                                                                | Why skip                                                                     |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `gateway/`, `tui_gateway/`, `web/`, `ui-tui/`, `apps/`                     | Multi-platform gateway / TUI / desktop — we're a domain-RAG reasoning engine |
| `cron/`, `batch_runner.py`, `mini_swe_runner.py`                           | Scheduled jobs / unattended automations — orthogonal                         |
| `agent/browser_*.py`, `agent/terminal_*.py`, `agent/process_*.py`          | Real-environment control — our tools stay sandboxed                          |
| `providers/`, `agent/*_adapter.py`                                         | Provider adapters — we use Ollama/OpenRouter only                            |
| `agent/credential_*.py`, `agent/secret_*.py`                               | Credential management — out of scope                                         |
| `agent/billing_*.py`, `agent/usage_pricing.py`, `agent/credits_tracker.py` | Billing/usage — not relevant locally                                         |
| `agent/insights.py`, `agent/reactions.py`, `agent/kanban_stop.py`          | Personal-assistant features                                                  |
| `agent/lsp/`, `agent/verify/`                                              | LSP tooling + verify recipes — we reuse `AnswerEvaluator`                    |

---

## 7. The 30-minute quick win (do this first)

The **bounded I/O trio** (§1.1–1.3) is the fastest, highest-value port: three self-contained modules
(`bounded_io.py`, `CircularRounds.py`, `tools/safety.py`) that map 1:1 to already-planned Phase 0 items,
have zero dependency on the rest of Hermes, and immediately harden the current `ReadFileTool` +
`ModelRegistry` on disk. Port those three, wire them into the current flat loop, and the repo is already
safer and more disciplined — before any of the bigger Phase 1/2 rework lands.

---

_Companion to [`analysis-against-hermes.md`](analysis-against-hermes.md) (the why) and
[`review-revise-design.md`](review-revise-design.md) (the what's-broken). Source studied:
`ai-c4y/temp/hermes-agent` (Nous Research, MIT). Written 2026-08-12._
