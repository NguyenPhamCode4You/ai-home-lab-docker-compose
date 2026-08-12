# Steal List — What to Port from Hermes into ProgressiveAgentSLM

> **Purpose.** Hermes (Nous Research, MIT) is already pulled into `ai-c4y/temp/hermes-agent`. This is the
> **concrete, file-by-file porting list** — what to steal _immediately_, what to adapt, and what to skip —
> grounded in the actual source, not just the analysis doc.
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

| #   | Hermes file                                         | What to steal                                                                                                                                                                                        | Our target                                                                             | Effort                                                                |
| --- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 1   | `agent/bounded_response.py`                         | **Byte-cap + wall-clock-deadline read** (worker-thread drain so a stalled socket can't hang the run; returns partial bytes on timeout; never raises on the error path)                               | `src/framework/bounded_io.py` — the `bounded_io` helper from the review                | **S** — near drop-in                                                  |
| 2   | `agent/iteration_budget.py`                         | **Thread-safe consume/refund iteration counter** (parent cap 500 / subagent 50; `refund()` for batched/programmatic tool turns)                                                                      | `src/framework/CircularRounds.py` + the `behavior_policies_max_circular_rounds` budget | **S** — near drop-in                                                  |
| 3   | `agent/file_safety.py`                              | **Sensitive-path deny-list** (`build_write_denied_paths` / `build_write_denied_prefixes`: `.ssh`, `.aws`, `.env`, `/etc/*`, credential stores) + `HERMES_WRITE_SAFE_ROOT`-style safe-root resolution | `src/framework/tools/safety.py` — the §10 deny-list                                    | **S** — near drop-in                                                  |
| 4   | `agent/redact.py`                                   | **Regex secret redaction** (API-key prefixes, sensitive query params / body keys, short-token full-mask, long-token head/tail preserve)                                                              | `src/framework/redact.py` — the §8.2 egress redaction                                  | **S** — near drop-in                                                  |
| 5   | `agent/tool_guardrails.py`                          | **Tool-loop guard** (idempotent-vs-mutating classification, `ToolCallSignature` = name + canonical-args hash, warn/block/halt thresholds, per-turn `LoopCapConfig` for web-search/subagent caps)     | `src/framework/guards/tool_loop.py` — the anti-drift guard                             | **M** — pure logic, adapt thresholds to our tools                     |
| 6   | `agent/verification_stop.py`                        | **Verify-on-stop** (turn-end guard: if the model tries to finish after editing code with no fresh evidence, inject a bounded follow-up; skips doc/markdown edits)                                    | `src/framework/guards/verify_on_stop.py` — the `double_checking` guard                 | **M** — adapt to "evidence covers the question" via `AnswerEvaluator` |
| 7   | `agent/context_engine.py`                           | **Pluggable context-engine ABC** (`on_session_start → update_from_response → should_compress → compress → on_session_end`) + `sanitize_memory_context` (redact + head/tail truncate at egress)       | `src/framework/Reflector.py` — the pluggable compaction engine                         | **M** — adapt lifecycle to our windows                                |
| 8   | `agent/context_breakdown.py`                        | **`char/4` token estimate + live `/context` breakdown** (system/tools/rules/skills/mcp/subagents/memory/conversation categories, `_chars_to_tokens`)                                                 | `src/framework/tokens.py` (`TokenCounter`) + the §7b health surface                    | **S** — near drop-in                                                  |
| 9   | `agent/prompt_caching.py`                           | **Cache-marker placement** (stable prefix → volatile suffix; breakpoints on real carriers; skip empty-content messages that waste a breakpoint)                                                      | `src/framework/prompt_assembly.py` — the stable-prefix/volatile-suffix assembly        | **M** — adapt to Ollama/OpenRouter (no Anthropic `cache_control`)     |
| 10  | `agent/subagent_lifecycle.py`                       | **Immutable delegate contracts** (`SubagentLaunchRequest`/`Handle`/`Status`/`Result`, state machine, `depth`, `role`, `allowed_toolsets`/`blocked_tools`, byte caps, HMAC-signed handles)            | `src/framework/delegates/contracts.py` — the §7 typed boundary                         | **M** — trim to our needs                                             |
| 11  | `hermes_state_search.py` + `hermes_state_common.py` | **FTS5 + trigram + CJK search** (incremental bounded merge, query char caps, resumable rebuild)                                                                                                      | `src/framework/memory/LogSearch.py` — the §8 FTS index                                 | **M** — adapt to our `iteration_*.jsonl`                              |
| 12  | `agent/curator.py`                                  | **Background curator** (aux-model, inactivity-triggered, pin/archive/consolidate, **never auto-deletes**, persists state)                                                                            | `src/framework/memory/curator.py` — the curation flywheel                              | **M** — adapt to `memory_data_stores`                                 |

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

```python
# Ported from hermes-agent/agent/bounded_response.py (MIT) — pattern, not verbatim
def read_bounded(response, *, max_bytes=64 * 1024, timeout_s=10.0) -> str:
    chunks: list[bytes] = []
    done = threading.Event()
    def _drain() -> None:
        total = 0
        try:
            for chunk in response.iter_bytes():
                if not chunk: continue
                remaining = max_bytes - total
                if remaining <= 0: break
                chunks.append(chunk[:remaining]); total += min(len(chunk), remaining)
        except Exception: pass
        finally: done.set()
    threading.Thread(target=_drain, daemon=True).start()
    if not done.wait(timeout=timeout_s):
        _safe_close(response)  # unblocks the socket read
    return b"".join(chunks).decode("utf-8", errors="replace")
```

**Adapt:** generalize from "error body" to _any_ external read (Ollama/OpenRouter responses, tool
output). Add a `deadline_hit → one infra failure` hook so the model ladder counts it (§4).

### 1.2 `iteration_budget.py` → `src/framework/CircularRounds.py`

**Why.** Our `behavior_policies_max_circular_rounds` (default 5) is the total-work budget, but the plan
has no counter class. Hermes's `IterationBudget` is a **thread-safe consume/refund counter** — exactly
the `CircularRounds` item in Phase 0.

**The key insight to copy:** `refund()` for **programmatic/batched tool turns** — a tool call that the
loop itself issued (not the model) shouldn't burn the model's iteration budget. This is the Hermes
lesson from §4.3 of the analysis.

```python
class CircularRounds:
    def __init__(self, max_total: int): self.max_total = max_total; self._used = 0; self._lock = threading.Lock()
    def consume(self) -> bool:  # True if allowed
        with self._lock:
            if self._used >= self.max_total: return False
            self._used += 1; return True
    def refund(self) -> None:
        with self._lock:
            if self._used > 0: self._used -= 1
    @property
    def remaining(self) -> int:
        with self._lock: return max(0, self.max_total - self._used)
```

**Adapt:** parent cap from `behavior_policies_max_circular_rounds`; delegate cap = parent's (or a
per-delegate override). Wire `refund()` into the tool-call path.

### 1.3 `file_safety.py` → `src/framework/tools/safety.py`

**Why.** Our §10 says "sensitive-path deny-list" but `ReadFileTool.py` on disk is a bare `open()`.
Hermes's `build_write_denied_paths` / `build_write_denied_prefixes` is the exact list, and it's
**self-contained** (only `os`/`pathlib`).

**The key insight to copy:** two layers — **exact paths** (`.ssh/id_rsa`, `.env`, `.netrc`, `.pgpass`,
`.npmrc`, `.pypirc`, `.git-credentials`, `/etc/sudoers`, `/etc/passwd`, `/etc/shadow`) and **directory
prefixes** (`.ssh/`, `.aws/`, `.gnupg/`, `.kube/`, `.docker/`, `.azure/`, `.config/gh/`,
`.config/gcloud/`, `/etc/sudoers.d/`, `/etc/systemd/`). Plus a **safe-root** allowlist
(`HERMES_WRITE_SAFE_ROOT`-style) so writes are confined to `base_folder_path` + `writable`
`working_directories`.

**Adapt:** our `WriteFileTool`/`ReadFileTool`/`SearchFileTool` resolve under `base_folder_path` +
`working_directories`; the deny-list applies _inside_ those roots too (a `writable` working dir must not
let the agent rewrite `.env`).

---

## 2. Steal now — the "enforcement" trio (the §5 guards)

### 2.1 `tool_guardrails.py` → `src/framework/guards/tool_loop.py`

**Why.** Our §5 anti-drift guard ("idempotent-vs-mutating classification + repeated-call detection") is
exactly Hermes's `ToolCallGuardrailConfig` + `ToolCallSignature`. It's **pure logic** (no agent
dependency) — the controller returns decisions (`allow`/`warn`/`block`/`halt`), and the runtime owns
whether a decision becomes a nudge, a synthetic result, or a halt.

**The key insight to copy:** a **stable, non-reversible signature** for a tool call = `tool_name` +
`sha256(canonical_args)` — so "same tool, same args" is detected deterministically, and the signature's
`to_metadata()` never leaks raw argument values. Plus **per-turn caps** (`LoopCapConfig`: max web
searches / max subagents per turn) — a single turn that spirals into 50 web searches is pathological.

**Adapt:** our tool names (`SqliteVectorQueryTool`, `JsonlQueryTool`, `ReadFileTool`, …); thresholds from
config (`warn_after` / `block_after` / `halt_after`); reset counters at the start of each agent loop.

### 2.2 `verification_stop.py` → `src/framework/guards/verify_on_stop.py`

**Why.** Our `double_checking` policy ("verify the gathered evidence actually answers the question; if
gaps remain, loop another round") is exactly Hermes's verify-on-stop. The Hermes version is **policy-only**
— it never runs checks itself; it turns a passive verification ledger into a bounded follow-up when the
model tries to finish without fresh evidence.

**The key insight to copy:** the **doc/markdown skip** — `_NON_CODE_VERIFY_EXTENSIONS` (`.md`,
`.markdown`, `.mdx`, `.rst`, `.txt`, `.adoc`, `.log`, `.csv`, …) and `_NON_CODE_VERIFY_FILENAMES`
(`license`, `notice`, `changelog`, …). A turn that touches _only_ prose must never demand a verification
round. For us: a turn that only wrote `todo.md` or a Mermaid `.md` must not trigger `double_checking`.

**Adapt:** our "evidence" is retrieval results, not code edits. The guard becomes: if the model tries to
emit a final answer and `AnswerEvaluator` says the evidence doesn't cover the question, inject one more
bounded retrieval round (while `CircularRounds.remaining > 0`).

### 2.3 `context_engine.py` → `src/framework/Reflector.py`

**Why.** Our Phase 0 "Progressive reflection (pluggable engine with `should_compress()`/`compress()`
lifecycle)" is exactly Hermes's `ContextEngine` ABC. The lifecycle is the contract:
`on_session_start → update_from_response → should_compress → compress → on_session_end`.

**The key insight to copy:** the engine is **pluggable** (config-driven `context.engine`, default
`"compressor"`, third-party engines via plugin dir) — so our `Reflector` becomes an interface, not a
hardcoded 50% call site. Also steal `sanitize_memory_context`: **redact + head/tail truncate at the
egress boundary** (4k head + 1.5k tail + truncation marker) — this is the §8.2 egress redaction made
concrete.

**Adapt:** our compaction is _adaptive_ (only enough to fit, protect head + tail, update prior summary)
per §3/§8 — the Hermes lifecycle gives the _when_; our `Reflector` gives the _how_.

---

## 3. Steal now — the "context & memory" trio

### 3.1 `context_breakdown.py` → `src/framework/tokens.py` + health surface

**Why.** Our `TokenCounter` (char/4, one measure for budget AND threshold) is exactly Hermes's
`_chars_to_tokens` = `(len(text) + 3) // 4`. And the `/context` breakdown (system/tools/rules/skills/
mcp/subagents/memory/conversation) is the §7b health surface.

**The key insight to copy:** the breakdown is **computed from the same parts the prompt builder uses**
(`build_system_prompt_parts` → `stable`/`context`/`volatile`), so the numbers _always_ match what's
actually sent — not a separate estimate. And `estimate_messages_tokens_rough` uses the same `char/4`
heuristic, so measure and threshold never disagree.

**Adapt:** our categories are the three windows (cognition/attention/response) + the always-on stores;
the health endpoint reports actual token usage per window.

### 3.2 `prompt_caching.py` → `src/framework/prompt_assembly.py`

**Why.** Our stable-prefix/volatile-suffix assembly (§3) is the same idea as Hermes's cache-marker
placement. The Hermes file is Anthropic-specific (`cache_control` markers), but the _placement logic_ is
portable.

**The key insight to copy:** **breakpoints land on real carriers** — skip empty-content messages
(assistant turns that are pure tool_calls, empty tool messages) because a marker there is ignored and
wastes one of the four breakpoints. For Ollama/llama.cpp the "marker" is just _byte-identical prefix_;
for OpenRouter it's the same. The rule "only compaction may rebuild the prefix" is the sanctioned
cache-invalidation event.

**Adapt:** no `cache_control` for Ollama — the byte-stable prefix _is_ the cache. For OpenRouter, keep
the marker logic if the provider honors it.

### 3.3 `hermes_state_search.py` + `hermes_state_common.py` → `src/framework/memory/LogSearch.py`

**Why.** Our §8 `LogSearch` (FTS5 + trigram + CJK, incremental bounded merge, query char caps, resumable
rebuild) is exactly Hermes's `SessionSearchMixin`. The `hermes_state_common.py` constants
(`FTS_TRIGRAM_SQL`, `MAX_FTS5_QUERY_CHARS`, `_FTS_CJK_TRIGGERS`) are the concrete SQL.

**The key insight to copy:** **incremental bounded merge** (`_try_incremental_merge_fts` runs one bounded
merge pass _without failing the completed write_ — maintenance is best-effort, never blocks writes), and
**query char caps** (`MAX_FTS5_QUERY_CHARS`).

**Adapt:** index `iteration_logging/iteration_*.jsonl` instead of the session DB; keep the trigram
tokenizer for CJK/substring.

---

## 4. Steal now — the "delegation & curation" pair

### 4.1 `subagent_lifecycle.py` → `src/framework/delegates/contracts.py`

**Why.** Our §7 typed immutable delegate boundary is exactly Hermes's `SubagentLaunchRequest` /
`SubagentHandle` / `SubagentStatus` / `SubagentResult` frozen dataclasses + state machine.

**The key insight to copy:** the **byte caps** (`_MAX_GOAL_CHARS = 16_000`, `_MAX_CONTEXT_CHARS = 32_000`,
`_MAX_RESULT_CHARS = 32_000`) and the **state machine** (`PENDING → STARTING → RUNNING → SUCCEEDED |
FAILED | INTERRUPTED | CANCELLED`). The parent never hands a child a live agent object — it hands a
frozen request and receives a frozen result.

**Adapt:** our delegate result is `{ state, summary, ref }` (planning §7) — keep that, add the byte caps
and the state enum. Skip the HMAC-signed handles (we're in-process, not cross-process).

### 4.2 `curator.py` → `src/framework/memory/curator.py`

**Why.** Our §8.2 "curate, never delete" + the review's "memory curation flywheel" is exactly Hermes's
curator: **aux-model, inactivity-triggered, pin/archive/consolidate, never auto-deletes, persists state**.

**The key insight to copy:** the **invariants** — only touches agent-created records, **never auto-deletes
(archive is recoverable)**, pinned records bypass auto-transitions, runs on the **auxiliary client**
(never touches the main session's prompt cache). For us: the curator runs on the `is_memory_distillation`
endpoint, off the critical path, and marks `known_edge_cases_knowledge` / `design_decisions_knowledge`
records `stale`/`archived` instead of deleting.

**Adapt:** our "skills" are `memory_data_stores` records; the curator consolidates duplicates and gates
`design_decisions_knowledge` on a sparse hook.

---

## 5. Steal later / adapt (lower priority, still valuable)

| Hermes file                                       | What                                                                                        | Our target                                       | Effort | When                             |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------ | -------------------------------- |
| `agent/memory_manager.py`                         | Background **prefetch pre-turn / sync post-turn** with bounded drain; one writable provider | `src/framework/memory/MemoryStores.py`           | M      | Phase 2 (after the stores exist) |
| `agent/learning_graph.py`                         | Skill/memory graph via lexical overlap, **cheap-first** (edges before LLM)                  | `src/framework/memory/` (the `distill_from` DAG) | M      | Phase 2                          |
| `agent/moa_loop.py`                               | Mixture-of-Agents for hard steps + **PII redaction at egress**                              | `src/framework/` (optional)                      | M      | Phase 4 (optional)               |
| `agent/context_references.py`                     | `@file:`/`@folder:` inline expansion with token accounting                                  | `src/framework/tools/`                           | M      | Phase 2 (optional)               |
| `agent/error_classifier.py`                       | Classify infra vs. quality failures (drives the ladder)                                     | `src/framework/ModelChain.py`                    | M      | Phase 0/1                        |
| `agent/retry_utils.py`                            | 429/backoff retry                                                                           | `src/framework/ModelChain.py`                    | S      | Phase 4                          |
| `agent/auxiliary_client.py`                       | Aux-model client (for distillation/curator)                                                 | `src/framework/ModelChain.py`                    | M      | Phase 2                          |
| `agent/stream_single_writer.py`                   | Single-writer stream (no interleaving)                                                      | `src/framework/logging/RunLogger.py`             | S      | Phase 1                          |
| `agent/turn_summary.py`                           | Per-turn summary (feeds the raw log)                                                        | `src/framework/memory/RawLog.py`                 | S      | Phase 1                          |
| `agent/context_compressor.py`                     | Iterative summary w/ Resolved/Pending + tool-output pre-prune                               | `src/framework/Reflector.py`                     | M      | Phase 2                          |
| `agent/trajectory_compressor.py`                  | Protect head+tail, compress only middle, adaptive target                                    | `src/framework/Reflector.py`                     | M      | Phase 2                          |
| `agent/verification_evidence.py`                  | Passive verification ledger (feeds verify-on-stop)                                          | `src/framework/guards/`                          | M      | Phase 2                          |
| `agent/skill_utils.py` / `skill_preprocessing.py` | Skill frontmatter + progressive disclosure                                                  | `src/framework/tools/SkillTool.py`               | M      | Phase 2 (optional)               |
| `agent/redact.py` (full)                          | The complete regex set (API keys, query params, body keys)                                  | `src/framework/redact.py`                        | S      | Phase 2                          |

---

## 6. Skip (deliberately out of scope)

| Hermes file                                                                | Why skip                                                                                                    |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `gateway/`, `tui_gateway/`, `web/`, `ui-tui/`, `apps/`                     | Multi-platform gateway / TUI / desktop — we're a domain-RAG reasoning engine, not a personal assistant      |
| `cron/`, `batch_runner.py`, `mini_swe_runner.py`                           | Scheduled jobs / unattended automations — orthogonal to a per-question RAG run                              |
| `agent/browser_*.py`, `agent/terminal_*.py`, `agent/process_*.py`          | Real-environment control — our tools stay sandboxed to `base_folder_path` + read-only `working_directories` |
| `providers/`, `agent/*_adapter.py` (Anthropic/Gemini/Bedrock/Vertex/Codex) | Provider adapters — we use Ollama/OpenRouter only                                                           |
| `agent/credential_*.py`, `agent/secret_*.py`                               | Credential management — out of scope for a home-lab RAG agent                                               |
| `agent/billing_*.py`, `agent/usage_pricing.py`, `agent/credits_tracker.py` | Billing/usage — not relevant locally                                                                        |
| `agent/insights.py`, `agent/reactions.py`, `agent/kanban_stop.py`          | Personal-assistant features — not relevant                                                                  |
| `agent/lsp/`, `agent/verify/`                                              | LSP tooling + verify recipes — we reuse `AnswerEvaluator` instead                                           |

---

## 7. The 30-minute quick win (do this first)

The **bounded I/O trio** (§1.1–1.3) is the fastest, highest-value port: three self-contained modules
(`bounded_io.py`, `CircularRounds.py`, `tools/safety.py`) that map 1:1 to already-planned Phase 0 items,
have zero dependency on the rest of Hermes, and immediately harden the existing `ReadFileTool` +
`ModelRegistry` on disk. Port those three, wire them into the current flat loop, and the repo is already
safer and more disciplined — before any of the bigger Phase 1/2 rework lands.

---

_Companion to [`analysis-against-hermes.md`](analysis-against-hermes.md) (the why) and
[`review-revise-design.md`](review-revise-design.md) (the what's-broken). Source studied:
`ai-c4y/temp/hermes-agent` (Nous Research, MIT). Written 2026-08-12._
