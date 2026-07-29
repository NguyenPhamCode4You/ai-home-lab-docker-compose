# ProgressiveAgentSLM — Planning & Progress Tracker

> **ProgressiveAgentSLM** is a single, **recursive** agent class optimized for **local / small
> language models (SLMs)**. One instance owns an identity, a `system_prompt`, a four-tier
> **context-window budget** (`context_window_breakdown`, expressed as **fractions** of the active
> model's context), a **ladder** of **models** (local→cloud, with one per-model retry budget),
> a set of **cognitive_behavior** policies (`when → then`), a set of **tools** (Supabase vector
> search, todo, write-file, search-file, vector-memory, skills), and a set of **delegates** — which
> are themselves `ProgressiveAgentSLM` instances. The agent _progressively_ builds a lightweight
> **cognitive index** over an **append-only worklog** (its single source of truth), retrieving only
> the blocks it needs back into a bounded working window — so quality comes from disciplined memory
> handling, not a bigger model. Every agent and delegate reads and writes the same worklog in the
> run's **worklog_folder**, so teammates can loop back over each other's work.
>
> Any model slot can be escalated, plug-and-play, to a more capable **cloud** model (OpenRouter). The
> class reuses existing primitives (`Task`, model clients, `SupabaseVectorStore`, `DocumentRanking`,
> `PythonCodeExecute`, `KnowledgeCompression`, `IterationSummarizer`, `AnswerEvaluator`,
> `FinalThoughtSummarizer`) and drops into `create_chat_backend` unchanged.

**Status legend:** ⬜ Not started · 🟡 In progress · ✅ Done · ⛔ Blocked

---

## 1. Vision & Design Philosophy

- **One recursive class.** Everything is a `ProgressiveAgentSLM`. A "team" is simply an agent whose `delegates` are other agents — composition _is_ recursion; there is no separate orchestrator type. Each agent carries its own `agent_id` + `description`, and the `description` alone is the signal a parent reads to decide when to hand it a sub-question.
- **Progressive cognition by indexing, not stuffing.** Each iteration the model's context is partitioned into four proportional tiers (§3) — fractions of whatever model is active. Instead of accumulating everything in the prompt, the agent appends its work to an **append-only `raw_worklog.log`** and builds a **`cognitive_index`** — a compact map of ~10–20-token pointers into that log. To think, it looks up the index and pulls only the relevant blocks back into a bounded working set (`context_window.log`). On small models, quality comes from disciplined memory handling — not a bigger model.
- **Local & SLM-first, cloud optional.** `models` is a priority **ladder** (highest → lowest). Local Ollama models do the frequent work; a cloud model (OpenRouter) sits lower as an automatic fallback, or is promoted to the top for hard steps. Each model gets one bounded retry budget — `max_retries_untill_switching_models` — that counts **both** quality (self-eval) **and** infra (timeout/HTTP) failures before the agent **switches to the next model** on the ladder (§4).
- **Behavior by policy, not by code.** `cognitive_behavior` is a list of `when → then` rules rendered into the system prompt every iteration — it both steers how a small model thinks (deep-think, double-check, visualize, say-no) and acts as the run's **todo checklist**. Policies are declarative only (no per-policy models); a non-programmer shapes behavior without touching Python.
- **One append-only worklog, shared by the whole team.** Every agent and delegate writes finished blocks into the same `raw_worklog.log` (the single source of truth) through one serialized writer, and indexes them in `cognitive_index`. Delegates deliver their final answer to the parent when done, but their work stays in the shared log so any later agent can **loop back** over it via the index.
- **Route by description, guide tools by `when`.** A parent routes a sub-question to a delegate purely by reading each delegate's `description` — no separate gate to maintain. Tools still carry a `when` guidance string that is injected next to the tool so a small model calls it at the right moment (and to prune the tool menu, §7).
- **Reuse, don't rebuild.** Async streaming generators that `yield` chunks, DI via constructor kwargs, `Task`-subclass agents, prompt-based JSON with robust regex fallbacks, JSON-file config/state. New code lives under `src/framework/`; existing files are touched minimally.

---

## 2. The `ProgressiveAgentSLM` Object

A single class configured by one object (JSON or Python). Every field has a sensible default; only `agent_id`, `description`, and — on the root agent — at least one `model` are required.

| Field                                 | Type        | Meaning                                                                                                                                                                                                                                |
| ------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`                            | str         | Stable identifier. Used by a parent to address this agent (`delegate:<agent_id>`) and as its section in the shared worklog.                                                                                                            |
| `description`                         | str         | One-line capability summary. The **sole** signal a parent reads to decide whether to delegate here — no separate gate.                                                                                                                 |
| `system_prompt`                       | str \| null | The agent's base persona / instructions, rendered at the top of the `cognitive_reflection_behavior` tier (§3). Optional; when omitted a default is built from `description` + `cognitive_behavior`. Per-agent (not inherited).         |
| `worklog_folder`                      | str         | Directory for the run's four-file worklog subsystem (§8). Delegates share the parent's `worklog_folder` (one shared log per run).                                                                                                      |
| `context_window_breakdown`            | object      | The four-tier budget expressed as **fractions** of the active model's `max_tokens` (§3) — the heart of the design. Actual token counts are inferred per model.                                                                         |
| `max_retries_untill_switching_models` | int         | Single per-model retry budget covering **both** quality (self-eval) **and** infra (timeout / HTTP) failures. Default **5**. When a model exhausts it, **switch to the next model** on the ladder; ladder exhaustion ends the run (§4). |
| `models`                              | list        | Priority **ladder** (§4), highest first. Each model gets its own `max_retries_untill_switching_models`; a successful iteration resets the ladder to the top model.                                                                     |
| `cognitive_behavior`                  | list        | `when → then` behavioral policies (§5) rendered into the system prompt each iteration; also the run's todo checklist. Declarative only — no per-policy models.                                                                         |
| `tools`                               | list        | Capabilities the agent may call, each with a `when` guidance string (§6): Supabase, todo, write-file, search-file, vector-memory, skills, …                                                                                            |
| `delegates`                           | list        | Nested `ProgressiveAgentSLM` configs (§7). The parent routes sub-questions to them by reading each one's `agent_id` / `description`.                                                                                                   |

> **Inheritance:** a delegate that omits `models` or `max_retries_untill_switching_models` **inherits the parent's**. It also shares the parent's `worklog_folder` (hence the shared `raw_worklog.log` + `cognitive_index`), while keeping its **own** `context_window.log` + `response_window.log`. `context_window_breakdown`, `system_prompt`, `cognitive_behavior`, and `tools` are per-agent (not inherited), so each delegate is independently budgeted and specialized.

---

## 3. `context_window_breakdown` — the four-tier proportional budget

The budget is expressed as **fractions of the active model's `max_tokens`**, not absolute token counts — so the same config runs unchanged on models with different context sizes, and each tier's real allowance is inferred at runtime as `fraction × max_tokens`. Only **three** tiers are declared; the **remainder is reserved for the answer**. Instead of stuffing accumulated history into the prompt, the agent keeps the full record in an append-only `raw_worklog.log` and a `cognitive_index` map over it; the tiers below bound what actually enters the prompt each step.

| Tier                             | Default | Holds                                                                                                                                                                                                                             | Budget / compaction rule                                                                                                                                      |
| -------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_history_awareness` | 0.025   | A brief summary of the last few turns — just enough to stay coherent without repeating everything (the full history lives in the worklog).                                                                                        | Set **0** for a stateless / one-shot agent; the freed budget is **donated to the next tier** so the agent "thinks harder".                                    |
| `cognitive_reflection_behavior`  | 0.325   | The cognition workspace: `system_prompt` + `cognitive_behavior` policies, tool descriptions + usage instructions, delegate descriptions, and the internal reasoning/reflection trace used to pick the next step or switch models. | Hosts the `cognitive_index` retrieval + reflection; when it and `current_working_attention` exceed budget, a progressive reflection compacts both to **50%**. |
| `current_working_attention`      | 0.525   | The working set for this run: the current user question plus everything retrieved from tools, delegates, and the past worklog (blocks pulled from `raw_worklog` via the index).                                                   | Compacted to **50%** when over budget (stale blocks dropped — still recoverable from `raw_worklog`).                                                          |
| _(remainder ≈ 0.125)_            | —       | The answer the agent is emitting this iteration (backed by `response_window.log`, §8).                                                                                                                                            | Hard output cap = `max_tokens − Σ(declared tiers)`. Flushed to `raw_worklog` + indexed, then **cleared** for the next iteration.                              |
| _(unbounded)_                    | —       | `raw_worklog.log` — every finished block from every agent/delegate, the **single source of truth**.                                                                                                                               | **Append-only, never rewritten.** No budget; this is what makes the 50% compactions above safe (nothing is truly lost).                                       |

> The three declared fractions default to **0.025 / 0.325 / 0.525 = 0.875**, leaving **≈ 0.125** for answering. They must sum to **< 1**; the loader rejects a breakdown that leaves no room for the answer (§12 Phase 3). For `gpt-oss:20b` (`max_tokens: 62000`) they resolve to ≈ **1,550 / 20,150 / 32,550** tokens, with **≈ 7,750** left for the answer; swap in a bigger-context model and every tier scales up automatically.

**Prompt assembly per step:**

```
[ cognitive_reflection_behavior:  system_prompt + cognitive_behavior(when→then, todo)
                                 + tool/delegate descriptions + reasoning/reflection trace   ≤ f_cog  × max_tokens ]
[ conversation_history_awareness:  brief rolling summary of recent turns                     ≤ f_conv × max_tokens ]
[ current_working_attention:       question + retrieved blocks (via cognitive_index) + tools ≤ f_work × max_tokens ]
→ answer:                          the response for this iteration                           ≤ (1 − Σf) × max_tokens
```

**Core loop invariant — index & retrieve, then compact:**

```
per block b produced (delegate answer / tool result / iteration answer):
    raw_worklog.append(b)                      # append-only source of truth
    cognitive_index.append(pointer(b))         # {block_id, agent, iter, raw_lines, summary≈10-20 tok, keywords}

per iteration:
    working ← retrieve(cognitive_index, question)          # pull only relevant blocks from raw_worklog
    if size(working) + size(cognitive_reflection) > budget:
        reflect_and_compact(target = 0.5 * current_size)   # merge pointers / drop stale blocks (recoverable)
    response_window ← respond(prompt)                       # ≤ (1 − Σf) × max_tokens
    flush(response_window → raw_worklog + cognitive_index); clear(response_window)
```

Every tier is a slice of the **selected** model's `max_tokens`, so the assembled request can **never** exceed that model's context — no separate size-inference step is needed (§4). Because `raw_worklog` is immutable, `cognitive_index` is a pure **index** (not a compressed blob), and compaction only ever touches the derived views, the agent can shrink its working memory aggressively and still recover any detail by following a pointer back into the raw log.

---

## 4. Models — per-agent priority ladder

`models` is an ordered list, highest priority first. Each entry:

| Key          | Required | Meaning                                                                                                                                                                      |
| ------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `platform`   | yes      | `ollama` (local) or `open_router` (cloud). Maps to the existing `Ollama` / `OpenRouter` clients.                                                                             |
| `name`       | yes      | Model name on that platform.                                                                                                                                                 |
| `url`        | no       | Platform endpoint (e.g. `http://localhost:11434` for Ollama, `https://openrouter.ai/api/v1` for OpenRouter). Defaults to the platform's env default.                         |
| `max_tokens` | no       | Context ceiling. A number sets it; `"auto"` (or omitted) uses the platform's advertised context. Every `context_window_breakdown` fraction is taken against this value (§3). |

**Selection & the ladder.** Walk the list top-down; the active model is the first **reachable** one. Because the budget is proportional to whatever model is chosen (§3), any model fits — there is no minimum-size gate. The list is a **ladder** with **one** per-model budget:

- **Retry budget — `max_retries_untill_switching_models` (default 5).** A single counter per model covering **both** failure kinds: a "not good enough" verdict from the per-iteration quick self-evaluation (a _quality_ failure) **and** a timeout / HTTP / unreachable error (an _infra_ failure). When the current model's counter reaches the budget, the agent **switches to the next model** on the ladder and resets the counter to 0.
- **Success resets the ladder.** When a model handles an iteration successfully, the ladder pointer resets to the **top** model for the next iteration (the cheapest capable model is always tried first).
- **Stopping.** The run stops when the ladder is **exhausted** — the last model uses up its `max_retries_untill_switching_models`. There is no separate global iteration cap; the ladder length × the per-model budget bounds the total work.

This is the per-agent generalization of a role-based registry — local-first with cloud as an automatic backstop, or cloud promoted by putting it first.

```json
"models": [
  { "platform": "ollama",      "name": "gpt-oss:20b",                 "url": "http://localhost:11434",       "max_tokens": 62000 },
  { "platform": "open_router", "name": "anthropic/claude-3.5-sonnet", "url": "https://openrouter.ai/api/v1", "max_tokens": "auto" }
]
```

---

## 5. `cognitive_behavior` — `when → then` behavioral policies

`cognitive_behavior` is a list of rules that shape the agent's behavior. Each rule renders into the system prompt **every iteration** as "**When** _condition_, **then** _action_." This serves two jobs at once: it steers how a small model thinks, and it acts as the run's **todo checklist** the model re-reads each pass to stay on task. The rendered rules live in the `cognitive_reflection_behavior` tier (§3). Policies are **declarative only** — they carry no per-policy `models`; model choice is governed globally by the ladder (§4), so authoring stays simple and one policy can't fragment the model routing.

| Key    | Meaning                                                                                        |
| ------ | ---------------------------------------------------------------------------------------------- |
| `id`   | Short label for the policy (e.g. `deep_think`, `double_check`, `visualize_diagram`, `say_no`). |
| `when` | The condition / trigger, in plain language.                                                    |
| `then` | The action the agent should take when the condition holds.                                     |

Recommended baseline policies: **deep_think** (decompose complex questions before answering), **double_check** (verify gathered evidence actually answers the question; re-iterate if gaps remain), **visualize_diagram** (emit a diagram when structure/relationships matter), **say_no** (answer honestly when the KB has no answer rather than hallucinate).

---

## 6. Tools — capabilities with `when` guidance

Each tool entry tells the agent **what** the tool is and **when** to use it. The `when` string is injected next to the tool in the prompt so a small model calls it at the right moment.

**Supabase (primary tool).** Vector search over a pgvector RPC — the most useful capability for these RAG agents.

| Key             | Meaning                                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| `type`          | `Supabase`.                                                                                                |
| `function_name` | The pgvector RPC to call (e.g. `match_n8n_documents_bvms_neo`).                                            |
| `ranking`       | If `true`, re-rank retrieved chunks with parallel `DocumentRanking` (reuse `RagAssistant.stream` batches). |
| `when`          | Guidance: when this knowledge source is the right one to query.                                            |

All other tools follow the same `{ type, when, … }` shape, and each `when` is used both to guide the model and to **prune the menu** (§7): only tools whose `when` matches the current step are shown. The Supabase wrapper is built on the now-async `SupabaseVectorStore.async_query`.

**Standard tool catalog** (industry-conventional shapes, reusing existing primitives):

| Tool                  | Shape (beyond `type` + `when`)                  | Behavior                                                                                                                                                                                                                                                                                                              |
| --------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Supabase`            | `function_name`, `ranking`                      | **Primary.** pgvector RPC via `SupabaseVectorStore.async_query`; optional parallel `DocumentRanking`. Read-only domain knowledge base.                                                                                                                                                                                |
| `ReadFileTool`        | —                                               | Read a file's contents. Paths resolve against the run's `worklog_folder`; `..` / absolute escapes rejected (OWASP A01/A03).                                                                                                                                                                                           |
| `SearchFileTool`      | `glob?`                                         | Locate files by name/glob or find where a term/symbol appears (ripgrep-style); returns path + line + snippet. Read-only, traversal-safe.                                                                                                                                                                              |
| `WriteFileTool`       | `require_approval?`                             | Persist an artifact (notes, generated code, a report). Path traversal / absolute escapes rejected (OWASP A01/A03). `require_approval: true` gates the write; default **false** → runs without prompting (home-lab). Reuses `FileHanlder`.                                                                             |
| `TodoTool`            | —                                               | Maintains the run's checklist (`todo.md` in the `worklog_folder`). The model **rewrites the whole list** (`[{id, content, status: pending\|in_progress\|completed}]`); the loop re-injects it each iteration (anti-drift).                                                                                            |
| `VectorMemoryTool`    | `function_name` (recall), `write_function_name` | The agent's **own, cross-run, writable** long-term memory (distinct from the read-only KB). `recall(query, k)` + `remember(text, tags?)`, backed by a Supabase memory table reusing `Embedding`. Naturally embeds `cognitive_index` summaries for semantic recall.                                                    |
| `SkillTool`           | `skills_dir`                                    | On-demand **procedure packs** (progressive disclosure): each skill file has `{ id, description, when }` frontmatter + a body of steps. Only id/description/when are always visible; the body loads when its `when` matches. **Trusted-local files only** (loading external skill text is a prompt-injection surface). |
| `GenerateDiagramTool` | —                                               | Emits Mermaid for the `visualize_diagram` policy.                                                                                                                                                                                                                                                                     |
| `RunPythonTool`       | `require_approval?`                             | Wraps `PythonCodeExecute`; `require_approval: true` gates execution; default **false** → runs without prompting. ⚠️ Autonomous execution — revisit before any non-local use.                                                                                                                                          |

---

## 7. Delegates — recursive composition

`delegates` is a list of **nested `ProgressiveAgentSLM` configs**. There is no separate "sub-agent" type — a delegate is a full agent with its own `system_prompt`, `context_window_breakdown`, `tools`, and optional `cognitive_behavior` / `models` / `delegates`. The parent:

1. **Routes by description.** For a sub-question the small model picks a delegate by reading each one's `description` — via the proven `_parse_agent_routing` JSON pattern, generalized to `delegate:<agent_id>`. Delegates are **not** gated by a separate `when`; a clear `description` is the whole contract (tools are still menu-pruned by their own `when`, §6). Fewer moving parts → more reliable SLM routing.
2. **Hands the sub-question down.** The delegate runs its **own** full progressive loop with its own `context_window.log` + `response_window.log`, but writes finished blocks into the **shared** `raw_worklog.log` + `cognitive_index` (one per run) under its own `agent_id`.
3. **Delivers when done.** Unlike the parent's live stream, a delegate returns only its **final** answer to the parent; the parent folds that block into its own working set (by index lookup) and continues. Because the delegate's full work remains in the shared log, any **later** agent or delegate can loop back over it via the index.

Depth is bounded by each model's `max_retries_untill_switching_models` at every level plus an overall recursion cap. Two RAG-backed delegates (`bvms-general-knowledge`, `bvms-code-knowledge`), each owning a Supabase function, is the canonical example (§13).

---

## 8. The Worklog — the four-file `worklog_folder` memory subsystem

The worklog is a **four-file subsystem** living in the run's `worklog_folder` (`<worklog_folder>/<run_id>/`, from the `worklog_folder` config field). It replaces the old `runs/` artifacts. `raw_worklog.log` + `cognitive_index` are **shared** by the whole team (single source of truth); `context_window.log` + `response_window.log` are **per-agent**. The tiers in §3 are the _prompt-side_ budget; these files are the _on-disk_ storage that budget draws from.

| File                    | Scope     | Written by                        | Role                                                                                                                                                                                                 |
| ----------------------- | --------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `raw_worklog.log`       | shared    | one **serialized writer** per run | **Append-only, never rewritten.** Every finished block (any model, main or delegate) is patched in as a delimited block with a stable line range. The single source of truth everyone loops back to. |
| `cognitive_index.jsonl` | shared    | the same writer                   | One **pointer record per block**: a ~10–20-token summary + the `raw_worklog` line range. The searchable **map** used to pull only relevant blocks back into a working window.                        |
| `context_window.log`    | per-agent | the owning agent                  | The agent's current working set, streamed to as it works; compacted to 50% when it exceeds the `current_working_attention` budget.                                                                   |
| `response_window.log`   | per-agent | the owning agent                  | The agent's **latest** answer only; flushed to `raw_worklog` + `cognitive_index`, then **cleared** each iteration.                                                                                   |

**A "block"** is one unit of finished work — a delegate's answer, a tool result, or an iteration's answer. Blocks are **flushed at completion** (not token-by-token): the writer buffers the output, then appends the whole block so line ranges stay intact and parallel delegates never interleave.

**The write path, per block:**

1. The agent streams into its own `context_window.log` / `response_window.log` while working.
2. On block completion, it enqueues the block to the run's **single writer**, which:
   a. appends the block to `raw_worklog.log` and records its `[start_line, end_line]`;
   b. appends one record to `cognitive_index.jsonl` (a cheap ~10–20-token summary via `KeywordExtractor` / `SimpleEntityExtractor`, an LLM summary only when needed).
3. `response_window.log` is cleared for the next iteration.

**The read path (index-and-retrieve).** To assemble its next prompt an agent does **not** replay the whole log; it queries `cognitive_index` (by keyword, and later by `VectorMemoryTool` embeddings), takes the matching line ranges, and pulls **only those blocks** from `raw_worklog` into `context_window.log`. This is RAG over the team's own worklog — the core trick that keeps SLM prompts small.

**Progressive reflection (compaction).** When `context_window.log` **+** `cognitive_index` exceed their budgets (`current_working_attention`, `cognitive_reflection_behavior`), a reflection compacts **both to 50% of current size**: index pointers are merged into coarser line ranges, and stale context blocks are dropped. Nothing is lost — `raw_worklog` is immutable, so any dropped detail is one pointer-lookup away.

**Delegate coordination.** Delegates share this exact behavior. The only difference: a delegate returns just its **final** answer to its parent, but its full work lands in the shared `raw_worklog` under its `agent_id`, so a later teammate can loop back over it via the index.

```
<worklog_folder>/<run_id>/     # e.g. wip/bvms-assistant/<run_id>/
  raw_worklog.log        # ← shared, append-only single source of truth (delimited blocks + line ranges)
  cognitive_index.jsonl  # ← shared, one ~10–20-token pointer per block → raw_worklog line range
  context_window.log     # ← per-agent working set (compacts to 50% over budget)
  response_window.log    # ← per-agent latest answer (flushed to raw + index, then cleared each iteration)
  todo.md                # ← TodoTool checklist (re-injected each iteration)
# <worklog_folder>/index.db    # optional SQLite FTS5 over raw_worklog + cognitive_index (LogSearch)
```

---

## 9. Goals → Components

| Goal (user)                                                                     | Realized by                                                                                                                                                                        |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Single recursive class anyone can configure (one object)                        | `ProgressiveAgentSLM` + `AgentConfig` + `config/load.py`                                                                                                                           |
| **Goal**: stay focused on the user-set goal                                     | `cognitive_behavior` policies + double-check / re-iterate loop (reuse `AnswerEvaluator`)                                                                                           |
| **Knowledge**: text files + Supabase vector DB + own long-term memory           | `SupabaseTool` (primary, pgvector) + `FileKnowledgeTool` + `VectorMemoryTool` (writable, cross-run)                                                                                |
| **Tools**: KB, files, search, write, todo, memory, skills, diagrams, python     | `ToolRegistry` + `tools/` (`SupabaseTool`, `ReadFileTool`, `SearchFileTool`, `WriteFileTool`, `TodoTool`, `VectorMemoryTool`, `SkillTool`, `GenerateDiagramTool`, `RunPythonTool`) |
| **Cognition**: index the worklog, retrieve only what's needed, compact safely   | `CognitiveIndex` (pointer map) + `Reflector` 50% compaction (reuse `KnowledgeCompression` + `IterationSummarizer`)                                                                 |
| **Delegate**: route by description, break into sub-agents, collect results      | Recursive `delegates` + `Router` (`description`-routed `delegate:<agent_id>`) dispatch                                                                                             |
| **Worklog**: one append-only shared source of truth + per-agent working windows | Four-file `worklog_folder` subsystem (`raw_worklog` + `cognitive_index` shared; `context_window` + `response_window` per-agent)                                                    |
| Local/SLM-first with a model **ladder** (single per-model retry budget)         | `ModelChain` (ladder + `max_retries_untill_switching_models`)                                                                                                                      |
| Per-step logging to terminal + files for full-text search                       | `RunLogger` (block/JSONL) + `LogSearch` (SQLite FTS5 over the worklog logs)                                                                                                        |
| Workflow configurable via JSON **and** Python                                   | `config/load.py` (`example.json` + `schema.json`) + `ProgressiveAgentSLM(...)`                                                                                                     |

---

## 10. Design Decisions

| Topic                | Decision                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent & control flow | **Recursive progressive loop** — each step assembles the four-tier prompt (fractions of the active model), applies `cognitive_behavior` policies, calls tools / routes to delegates, then folds context+answer into the `cognitive_index`; iterate until the model ladder is exhausted.                                                                                                                                                                                                               |
| Delegation           | **Follow `AssistantOrchestra`** routing (`_parse_agent_routing`), generalized to `delegate:<agent_id>`; a parent routes by reading each delegate's `description`. Delegates inherit `models` + `max_retries_untill_switching_models`.                                                                                                                                                                                                                                                                 |
| Models (defaults)    | **Per-agent ladder** (highest→lowest): first reachable model wins (the budget is proportional, so any model fits). Each model gets one `max_retries_untill_switching_models` budget (default 5) covering **both** quality self-eval failures **and** infra errors; success resets the ladder to the top; the run ends when the ladder is exhausted. **OpenRouter** cloud as automatic fallback or promoted to top; `max_tokens: "auto"` uses the platform context and every tier is a fraction of it. |
| Worklog & memory     | **Four-file `worklog_folder` subsystem.** Shared **append-only** `raw_worklog.log` (single source of truth) + `cognitive_index.jsonl` (pointer map); per-agent `context_window.log` + `response_window.log`. Blocks flush at completion via one serialized writer; **`cognitive` is an index, not a compressed blob**; progressive reflection compacts working views to 50%.                                                                                                                          |
| Tool safety          | **Trust-local / ungated** (home-lab); `WriteFileTool` / `SearchFileTool` / `ReadFileTool` resolve paths under the run's `worklog_folder` with path-traversal / absolute-escape rejection (OWASP A01/A03); `skills` load **trusted-local files only**. Optional **`require_approval` (default false)** on `RunPythonTool` / `WriteFileTool`. ⚠️ Autonomous code execution can be destructive; revisit before any non-local use.                                                                        |
| Tool-call protocol   | **Both** — native Ollama `/api/chat` tool-calling when supported; **prompted-JSON + robust parser** fallback for small models.                                                                                                                                                                                                                                                                                                                                                                        |
| Logging & search     | **JSONL events + per-run Markdown transcript + SQLite FTS5 index** for full-text search.                                                                                                                                                                                                                                                                                                                                                                                                              |
| Sequencing           | **Phased** — MVP core agent first, then full tools/reflection, then workflow config, then hardening.                                                                                                                                                                                                                                                                                                                                                                                                  |
| Workflow config      | **JSON (`example.json`) + Python construction**, both via `config/load.py` with delegate inheritance + `schema.json` validation.                                                                                                                                                                                                                                                                                                                                                                      |
| Isolation            | All new code under `src/framework/`. Existing files minimally touched (async `SupabaseVectorStore`, Ollama `/api/chat`).                                                                                                                                                                                                                                                                                                                                                                              |

---

## 11. Target Package Layout

```
src/framework/
  __init__.py
  ProgressiveAgentSLM.py         # the single recursive agent class: owns context_window_breakdown, models, cognitive_behavior, tools, delegates; runs the progressive loop and recurses into delegates
  AgentConfig.py                 # parsed config: agent_id, description, system_prompt, worklog_folder, context_window_breakdown, max_retries_untill_switching_models, models[], cognitive_behavior[], tools[], delegates[] (+ inheritance from parent)
  ContextWindow.py               # four-tier fractional budget over the active model's max_tokens: conversation_history_awareness / cognitive_reflection_behavior / current_working_attention / (remainder=answer); cascade-on-zero + 50% compaction
  ModelChain.py                  # per-agent ladder → first reachable model; single per-model retry budget (max_retries_untill_switching_models) covering quality + infra; success resets to top; platform factory; max_tokens "auto"
  CognitiveBehavior.py           # renders cognitive_behavior when → then rules into the system prompt
  ToolRegistry.py                # Tool base + dispatch; each tool carries a `when` guidance string
  agents/
    Reflector.py                 # progressive reflection: compacts context_window + cognitive_index to 50% when over budget; raw_worklog stays intact (index, not a compressed blob)
    Router.py                    # reads each delegate.description → picks delegate(s) for a sub-question (generalized _parse_agent_routing → delegate:<agent_id>)
  tools/
    SupabaseTool.py              # PRIMARY: pgvector RPC via SupabaseVectorStore.async_query; optional parallel DocumentRanking when ranking=true
    ReadFileTool.py              # read a file (resolved under worklog_folder; traversal-safe)
    SearchFileTool.py            # name/content search (ripgrep-style) → path + line + snippet; traversal-safe
    WriteFileTool.py             # write a file (traversal-safe); optional require_approval; reuses FileHanlder
    TodoTool.py                  # rewrites <worklog_folder>/todo.md checklist; re-injected each iteration (anti-drift)
    VectorMemoryTool.py          # writable cross-run memory: recall()/remember() over a Supabase memory table (reuses Embedding)
    SkillTool.py                 # on-demand procedure packs from skills_dir (progressive disclosure; trusted-local)
    GenerateDiagramTool.py       # emits Mermaid for the visualize_diagram policy
    RunPythonTool.py             # wraps tools/PythonCodeExecute; optional require_approval (default false)
    FileKnowledgeTool.py         # files-type knowledge source
  logging/
    RunLogger.py                 # owns the worklog run dir; terminal + block events; single serialized writer
    Worklog.py                   # coordinator for the four-file subsystem (raw_worklog + cognitive_index + context_window + response_window)
    RawWorklog.py                # append-only raw_worklog.log; append(block) → [start_line, end_line]
    CognitiveIndex.py            # cognitive_index.jsonl pointer map; append(pointer)/search()/compact(0.5)
    ContextWindowLog.py          # per-agent context_window.log; stream()/retrieve(index)/compact(0.5)
    ResponseWindow.py            # per-agent response_window.log; write()/flush→raw+index/clear()
    LogSearch.py                 # SQLite FTS5 index (<worklog_folder>/index.db) over raw_worklog + cognitive_index + search() + CLI
  config/
    load.py                      # build a ProgressiveAgentSLM tree from JSON or a Python dict; applies delegate inheritance
    schema.json                  # JSON schema for validation
  example.json                   # the canonical bvms-assistant config (§13)

progressive_agent_slm_demo.py    # entry point: load config → ProgressiveAgentSLM → create_chat_backend + uvicorn (port 8001)
```

---

## 12. Phases & Tasks

> Phases 0–1 were built against the earlier delegate-registry design; their primitives exist but
> need **rework** to the recursive four-tier-budget model below — hence 🟡, not ✅. `[~]` = exists,
> needs rework.

### Phase 0 — Foundation primitives 🟡

- [~] `ContextWindow.py`: four-tier **fractional** budget (`conversation_history_awareness` / `cognitive_reflection_behavior` / `current_working_attention` / remainder=answer) over the active model's `max_tokens`, cascade-on-zero donation, budget-bounded trimming (§3). _(new)_
- [~] `ModelChain.py`: per-agent **ladder** → first reachable model; single per-model retry budget `max_retries_untill_switching_models` (default 5) covering quality self-eval **and** infra failures; success resets to the top model; platform factory (`ollama`→`Ollama`, `open_router`→`OpenRouter`); `max_tokens: "auto"` sizing (§4). _(reworks `ModelRegistry`)_
- [x] Make `SupabaseVectorStore` async: `async_query` + `async_get_documents_string` via `httpx.AsyncClient` (sync preserved). _(IMPROVEMENTS.md §2)_
- [~] `logging/` four-file **worklog** subsystem (§8): append-only `RawWorklog` (block append → line range) + `CognitiveIndex` (pointer map, cheap keyword summaries) + per-agent `ContextWindowLog` + `ResponseWindow`, coordinated by `Worklog` behind **one serialized writer**; `RunLogger` owns `<worklog_folder>/<run_id>/`. _(reworks the old worklog.md/events.jsonl/transcript.md)_
- [ ] Progressive reflection: compact `context_window.log` + `cognitive_index` to **50%** when over the `current_working_attention` / `cognitive_reflection_behavior` budgets (merge pointers / drop stale blocks; recoverable from raw). _(new)_

### Phase 1 — Recursive core agent (runnable vertical slice) 🟡

- [~] `AgentConfig.py`: parse `agent_id`, `description`, `system_prompt`, `worklog_folder`, `context_window_breakdown`, `max_retries_untill_switching_models` (default 5), `models[]`, `cognitive_behavior[]`, `tools[]`, `delegates[]`; apply parent→delegate inheritance of the model ladder + retry budget + shared `worklog_folder`.
- [~] `ProgressiveAgentSLM.py`: the single recursive class. Per step — retrieve relevant blocks from `raw_worklog` via `cognitive_index` into `context_window`, assemble the four-tier prompt, select a model from the ladder, apply `cognitive_behavior` policies, route to delegates by `description` / prune tools by `when`, emit the answer (remainder tier) into `response_window`, flush the block to `raw_worklog` + `cognitive_index`, quick self-eval (switch model on repeated failure). Recurse into `delegates`; stop when the model ladder is exhausted.
- [~] `agents/Router.py`: choose delegate(s) per sub-question by `description` via the generalized `_parse_agent_routing` (`delegate:<agent_id>`); prune the tool menu by each tool's `when`. _(reworks Forwarder)_
- [~] `agents/Reflector.py`: the cognitive-accumulation compressor (reuse `KnowledgeCompression` + `IterationSummarizer`).
- [~] `ToolRegistry.py` + `tools/SupabaseTool.py` (primary; `function_name` + `ranking`) + `tools/ReadFileTool.py` + `tools/TodoTool.py`; each tool carries its `when` guidance (used for menu pruning).
- [~] Wire `RunLogger` + the four-file `Worklog` subsystem (single serialized writer); `progressive_agent_slm_demo.py` via `create_chat_backend` (port 8001).

### Phase 2 — Full tools, cognitive_behavior policies, model routing ⬜

- [ ] Remaining tools: `SearchFileTool` + `WriteFileTool` (traversal-safe under `worklog_folder`), `VectorMemoryTool` (cross-run memory over a Supabase table), `SkillTool` (progressive-disclosure procedure packs), `GenerateDiagramTool` (Mermaid), `RunPythonTool` (wrap `PythonCodeExecute`, optional `require_approval`), `FileKnowledgeTool`.
- [ ] `CognitiveBehavior.py`: render `cognitive_behavior` `when → then` rules into the system prompt; ship the baseline set (deep_think, double_check, visualize_diagram, say_no).
- [ ] Supabase ranking path: parallel `DocumentRanking` batches (reuse `RagAssistant.stream`) when `ranking: true`.
- [ ] Budget enforcement: measure tokens (tokenizer or char-approx), trim each tier to budget, implement cascade-on-zero donation.
- [ ] `logging/LogSearch.py`: SQLite FTS5 index (`<worklog_folder>/index.db`) over `raw_worklog` + `cognitive_index` + search + CLI over all runs.

### Phase 3 — Config loader (JSON + Python) ⬜

- [ ] `config/load.py` + `config/schema.json`: build a `ProgressiveAgentSLM` tree from `example.json` (or a Python dict) with validation + delegate inheritance.
- [ ] Round-trip the canonical `example.json` (§13) end-to-end as a worked example + regression check; authoring README.

### Phase 4 — Hardening ⬜

- [ ] Unit tests: config loader/inheritance, four-tier budgeting + cascade, `cognitive_index` pointer append + 50% compaction (line-range integrity), model-ladder switch (single retry budget) + success-reset, router description-routing parser, Supabase tool, four-file `Worklog` append/read behind one writer, `RunLogger` JSONL+FTS round-trip.
- [ ] Integration smoke test with a stub model implementing `.stream`.
- [ ] Timeouts/retries (reuse 429/backoff from `OpenRouter`); model fall-through.
- [ ] Optional `require_approval` (default false) on `RunPythonTool` / any shell tool.

---

## 13. Example: The `bvms-assistant` Config

The canonical configuration (live copy: `src/framework/example.json`). It defines a top orchestrator with **two RAG-backed delegates** — each delegate is itself a full `ProgressiveAgentSLM` with its own proportional `context_window_breakdown` and Supabase function (the code delegate also pins its own `models`). The same tree can be authored in JSON or built in Python; both produce the same agent and drop into `create_chat_backend`.

### 13a. JSON (declarative, recursive)

```json
{
  "agent_id": "bvms-assistant",
  "description": "Specialized Agent that can answer technical question about BVMS (BBC Voyage Management System).",
  "worklog_folder": "wip/bvms-assistant",
  "system_prompt": "You are a helpful assistant that answers questions about BVMS (BBC Voyage Management System) by combining domain knowledge, code analysis, and diagrams. You can delegate to specialist sub-agents when needed.",
  "max_retries_untill_switching_models": 5,

  "models": [
    {
      "platform": "ollama",
      "name": "gpt-oss:20b",
      "url": "http://localhost:11434",
      "max_tokens": 62000
    },
    {
      "platform": "open_router",
      "name": "anthropic/claude-3.5-sonnet",
      "url": "https://openrouter.ai/api/v1",
      "max_tokens": "auto"
    }
  ],

  "context_window_breakdown": {
    "conversation_history_awareness": 0.025,
    "cognitive_reflection_behavior": 0.325,
    "current_working_attention": 0.525
  },

  "cognitive_behavior": [
    {
      "id": "deep_think",
      "when": "The question is complex or spans multiple topics.",
      "then": "Break it into sub-questions and decide which delegate(s) and tool(s) each part needs before answering."
    },
    {
      "id": "double_check",
      "when": "All delegates and tools for this iteration have returned their results.",
      "then": "Verify the gathered evidence actually answers the question; if gaps remain and iterations are left, run another round to fill them."
    },
    {
      "id": "visualize_diagram",
      "when": "The answer involves a workflow, an architecture, or relationships between components.",
      "then": "Call GenerateDiagramTool to produce a Mermaid diagram that illustrates the concept alongside the text."
    },
    {
      "id": "say_no",
      "when": "No clear answer can be found after exhausting the relevant delegates and tools.",
      "then": "Tell the user honestly that the answer is not available and suggest how to refine the question. Never invent an answer."
    }
  ],

  "tools": [
    {
      "type": "ReadFileTool",
      "when": "The user references a specific local file whose contents are needed to answer."
    },
    {
      "type": "SearchFileTool",
      "when": "You need to locate a file by name/glob or find where a term/symbol appears before reading it."
    },
    {
      "type": "WriteFileTool",
      "require_approval": true,
      "when": "You must persist an artifact (notes, generated code, a report) to disk inside the sandbox root."
    },
    {
      "type": "TodoTool",
      "when": "At the start of a multi-step task, and whenever the plan changes: write/refresh the run's checklist so the agent stays on task across iterations."
    },
    {
      "type": "VectorMemoryTool",
      "when": "Recall durable facts learned in previous runs, or remember a new durable fact worth reusing later."
    },
    {
      "type": "GenerateDiagramTool",
      "when": "A visual diagram would make a workflow or architecture clearer (see the visualize_diagram policy)."
    }
  ],

  "delegates": [
    {
      "agent_id": "bvms-general-knowledge",
      "description": "Business workflow & domain knowledge about BVMS — architecture, components, features, typical use cases. Ask this delegate 'how does BVMS work / what does it do' questions.",
      "context_window_breakdown": {
        "conversation_history_awareness": 0,
        "cognitive_reflection_behavior": 0,
        "current_working_attention": 0.725
      },
      "tools": [
        {
          "type": "Supabase",
          "function_name": "match_n8n_documents_bvms_neo",
          "ranking": true,
          "when": "Primary source for how BVMS works: architecture, components, business workflows, and features."
        }
      ]
    },
    {
      "agent_id": "bvms-code-knowledge",
      "description": "Deep technical & code aspects of BVMS — internal workings, code structure, APIs, implementation details. Ask this delegate 'how is it built / where in the code' questions.",
      "context_window_breakdown": {
        "conversation_history_awareness": 0,
        "cognitive_reflection_behavior": 0.225,
        "current_working_attention": 0.425
      },
      "models": [
        {
          "platform": "ollama",
          "name": "qwen3.6:27b",
          "url": "http://localhost:11434",
          "max_tokens": 64000
        }
      ],
      "tools": [
        {
          "type": "Supabase",
          "function_name": "match_n8n_code_bvms_neo",
          "ranking": true,
          "when": "Primary source for code-level questions: internals, code structure, APIs, and implementation details."
        },
        {
          "type": "RunPythonTool",
          "when": "A quick calculation or code snippet must be executed to verify behavior."
        }
      ]
    }
  ]
}
```

`bvms-general-knowledge` omits `models` and `max_retries_untill_switching_models`, so it **inherits** them from the parent; `bvms-code-knowledge` pins its own bigger local model but still inherits the retry budget. Both share the parent's `worklog_folder` (one `raw_worklog.log` + `cognitive_index` for the whole run) while keeping their own `context_window.log` + `response_window.log`. Because every tier is a **fraction** of the active model's `max_tokens`, no request can overflow: the parent's `0.025 / 0.325 / 0.525` resolve to ≈ 1,550 / 20,150 / 32,550 of gpt-oss's 62,000 (≈ 7,750 left to answer); the general delegate folds its two zeroed front tiers into ~0.725 of working attention, and the code delegate keeps a modest 0.225 cognitive slice on its 64k model.

### 13b. Python (equivalent, programmatic)

```python
from src.framework.ProgressiveAgentSLM import ProgressiveAgentSLM
from src.framework.config.load import load_agent
from src.ChatBackend import create_chat_backend

# Option A — load the JSON tree above (applies delegate inheritance automatically)
assistant = load_agent("src/framework/example.json")

# Option B — build the same tree directly
assistant = ProgressiveAgentSLM(
    agent_id="bvms-assistant",
    description="Specialized agent that answers technical questions about BVMS (BBC Voyage Management System).",
    worklog_folder="wip/bvms-assistant",
    system_prompt="You are a helpful assistant that answers questions about BVMS by combining "
                  "domain knowledge, code analysis, and diagrams, delegating to specialists when needed.",
    context_window_breakdown=dict(conversation_history_awareness=0.025,
                                  cognitive_reflection_behavior=0.325,
                                  current_working_attention=0.525),
    max_retries_untill_switching_models=5,
    models=[
        dict(platform="ollama", name="gpt-oss:20b", url="http://localhost:11434", max_tokens=62000),
        dict(platform="open_router", name="anthropic/claude-3.5-sonnet",
             url="https://openrouter.ai/api/v1", max_tokens="auto"),
    ],
    cognitive_behavior=[
        dict(id="deep_think",   when="The question is complex.",            then="Decompose and route to delegate(s)/tool(s)."),
        dict(id="double_check", when="All delegates/tools have returned.",   then="Verify; re-iterate if gaps remain."),
        dict(id="say_no",       when="No answer after exhausting sources.",  then="Say so honestly; never invent."),
    ],
    tools=[
        dict(type="ReadFileTool", when="A referenced local file is needed."),
        dict(type="TodoTool", when="Keep the run checklist current."),
        dict(type="VectorMemoryTool", when="Recall/remember durable facts across runs."),
    ],
    delegates=[
        ProgressiveAgentSLM(
            agent_id="bvms-general-knowledge",
            description="Domain & workflow knowledge about BVMS.",
            context_window_breakdown=dict(conversation_history_awareness=0,
                                          cognitive_reflection_behavior=0,
                                          current_working_attention=0.725),
            tools=[dict(type="Supabase", function_name="match_n8n_documents_bvms_neo",
                        ranking=True, when="How BVMS works: architecture, features.")],
        ),  # inherits parent models + retry budget
        ProgressiveAgentSLM(
            agent_id="bvms-code-knowledge",
            description="Code & technical internals of BVMS.",
            context_window_breakdown=dict(conversation_history_awareness=0,
                                          cognitive_reflection_behavior=0.225,
                                          current_working_attention=0.425),
            models=[dict(platform="ollama", name="qwen3.6:27b",
                         url="http://localhost:11434", max_tokens=64000)],
            tools=[dict(type="Supabase", function_name="match_n8n_code_bvms_neo",
                        ranking=True, when="Code-level questions: internals, APIs.")],
        ),
    ],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_chat_backend(assistant), host="0.0.0.0", port=8001, timeout_keep_alive=300)
```

> A delegate that omits `models` / `max_retries_untill_switching_models` inherits the parent's, and
> shares the run's `worklog_folder`. Each finished block is flushed into the shared append-only
> `raw_worklog.log` and mapped in `cognitive_index` (§8), so the two delegates can loop back over each
> other's work by index lookup rather than replaying the whole log.

---

## 14. Key Reuse Map (concrete)

| Existing asset                                                   | Reused for                                                                                   |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `AssistantOrchestra.stream`                                      | `ProgressiveAgentSLM` per-step loop (route → execute → accumulate → reflect → iterate)       |
| `AssistantOrchestra._parse_agent_routing` / `_parse_eval_result` | `Router` delegate selection (`delegate:<agent_id>`) + double-check evaluation parsing        |
| `AssistantOrchestra.add_agent` / `agents` registry               | The recursive `delegates` registry (each keyed by `agent_id` + `description`)                |
| `all_agent_responses` + `IterationSummarizer` compaction         | Seed for `raw_worklog` blocks + the 50% progressive-reflection compaction                    |
| `KnowledgeCompression`, `IterationSummarizer`                    | `Reflector` — the 50% compaction of `context_window` + `cognitive_index` (not a blob)        |
| `KeywordExtractor`, `SimpleEntityExtractor`                      | Cheap ~10–20-token `cognitive_index` summaries + keywords (LLM summary only when needed)     |
| `SupabaseVectorStore` + `Embedding`                              | `VectorMemoryTool` — writable cross-run memory table (`remember`/`recall`)                   |
| `FileHanlder` / `PythonCodeExecute`                              | `WriteFileTool` / `SearchFileTool` / `RunPythonTool` (traversal-safe under `worklog_folder`) |
| `RagAssistant.stream` (parallel `DocumentRanking` batches)       | `SupabaseTool` ranking path (`ranking: true`)                                                |
| `SupabaseVectorStore.async_query`                                | `SupabaseTool` — the primary capability                                                      |
| `Task` + DI-kwargs pattern                                       | `Router`, `Reflector` agents                                                                 |
| `AnswerEvaluator`, `FinalThoughtSummarizer`                      | `double_check` policy + final recap from the worklog                                         |
| `PythonCodeExecute`                                              | `RunPythonTool` (optional `require_approval`, default false)                                 |
| `Ollama` (`/api/generate`) / `OpenRouter` (429 backoff)          | The per-agent `models` chain via the platform factory (local-first, cloud fallback)          |
| `ChatBackend.create_chat_backend`                                | Unchanged streaming integration point                                                        |

---

## 15. Verification

1. **Unit**: config loader + delegate inheritance, four-tier **fractional** budgeting (trim + cascade-on-zero over each model's `max_tokens`), `cognitive_index` pointer append + 50% compaction, model-ladder switch (single retry budget covering quality + infra) + success-reset, `Router` description-routing selection parser, `SupabaseTool`, four-file `Worklog` append/read (line-range integrity) behind one writer, `RunLogger` JSONL+FTS round-trip.
2. **Integration smoke**: load `example.json` with a stub model — assert the tree builds, the parent routes to a delegate by `description`, the delegate calls its Supabase tool and writes blocks under its own `agent_id`, `cognitive_index` grows yet stays ≤ its budget, and `raw_worklog.log` + `cognitive_index.jsonl` (+ per-agent `context_window.log` / `response_window.log`) exist and FTS search returns the run.
3. **Manual**: launch `progressive_agent_slm_demo.py` via uvicorn, ask a multi-step BVMS question, confirm streamed think/route/delegate/answer, per-block worklog flushing + index-and-retrieve, and on-disk logs searchable via the `LogSearch` CLI.
4. **Budget**: assert no request exceeds the selected model's `max_tokens`, and that a delegate omitting `models` inherits the parent's chain.

---

## 16. Open Questions

| #   | Question                                                                                                      | Recommendation / Resolution                                                                                                                                                                                                                                       | Decision   |
| --- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| 1   | Recursion — is every delegate a full `ProgressiveAgentSLM`?                                                   | Yes; core to the design. Recursion depth is bounded by the finite delegate tree; per-agent work is bounded by `max_retries_untill_switching_models` + ladder exhaustion.                                                                                          | ✅ Decided |
| 2   | Memory model — is `cognitive` compressed knowledge or an index?                                               | An **index** (pointer map into append-only `raw_worklog`); four-file **worklog** subsystem replaces the old `runs/` artifacts.                                                                                                                                    | ✅ Decided |
| 3   | Model switching — what counts as a "failed attempt"?                                                          | A single per-model budget `max_retries_untill_switching_models` (default 5) counts **both** a quality failure (from the quick self-eval) **and** an infra failure (timeout/HTTP); when it is spent, drop to the next model. Success resets the ladder to the top. | ✅ Decided |
| 4   | Ladder exhaustion — loop, stop, or ladder-as-escalation?                                                      | **Ladder-as-escalation** — walk top-down once; the run stops when the last model exhausts its retry budget (no separate global iteration cap).                                                                                                                    | ✅ Decided |
| 5   | Per-step (per-policy) model choice?                                                                           | **No** — `cognitive_behavior` stays declarative (system-prompt + todo); model choice is global via the ladder.                                                                                                                                                    | ✅ Decided |
| 6   | Routing signal — how are delegates vs. tools selected?                                                        | **Delegates** are chosen by `description` only (agent-level `when` removed); **tools** keep a `when` that a cheap pre-pass uses to prune the menu before the SLM picks.                                                                                           | ✅ Decided |
| 7   | Token measurement for budgeting — real per-model tokenizer, or char≈token approximation?                      | Char-approx (reuse `CHARS_PER_TOKEN`) for P1; pluggable tokenizer in P2.                                                                                                                                                                                          | _TBD_      |
| 8   | `cognitive_index` summaries — cheap keyword extraction or LLM per block?                                      | Keyword/entity extraction by default (`KeywordExtractor`); LLM summary only when needed.                                                                                                                                                                          | _TBD_      |
| 9   | `VectorMemory` scope & backing store — cross-run? Supabase table or local?                                    | Cross-run persistent; a dedicated Supabase memory table reusing `Embedding` (local store as a fallback).                                                                                                                                                          | _TBD_      |
| 10  | `worklog_folder` lifecycle — one ephemeral `<worklog_folder>/<run_id>/` per question; `VectorMemory` durable? | Yes — `<worklog_folder>/<run_id>/` is per-run; durable cross-run knowledge lives in `VectorMemory`.                                                                                                                                                               | _TBD_      |

---

## 17. Logging Artifacts & Event Schema

The four-file `worklog` subsystem per run (see §8), replacing the old `runs/` artifacts:

- **`raw_worklog.log`** — shared, **append-only** single source of truth. Every finished block (any model, main or delegate) is patched in as a delimited block with a stable `[start_line, end_line]`. Never rewritten.
- **`cognitive_index.jsonl`** — shared **pointer map**: one record per block (schema below), used to retrieve only the relevant blocks back into a working window.
- **`context_window.log`** — per-agent working set; compacted to 50% over its `current_working_attention` budget.
- **`response_window.log`** — per-agent latest answer; flushed to raw + index, then cleared each iteration.
- **`<worklog_folder>/index.db`** _(optional)_ — SQLite FTS5 over `raw_worklog` + `cognitive_index` for `LogSearch`.

Each `cognitive_index.jsonl` record (a **pointer**, not a full event):

```json
{
  "block_id": "run-agent-iter-seq",
  "ts": "ISO-8601Z",
  "agent_id": "emitter agent_id (or 'root')",
  "iteration": 1,
  "phase": "route | act | observe | reflect | delegate | answer",
  "actor": "router | reflector | tool:NAME | delegate:<agent_id>",
  "raw_lines": [1200, 1264],
  "summary": "≈10–20-token gist of the block",
  "keywords": ["voyage", "approval", "saga"],
  "tokens": 0
}
```

`raw_worklog.log` is the verbatim source of truth; `cognitive_index.jsonl` is the retrieval map over
it; per-agent `context_window.log` holds only the blocks pulled back in; `response_window.log` holds
the current answer. Compaction only ever touches the derived views — `raw_worklog` is immutable, so
any detail is one pointer-lookup away.

---

_Last updated: 2026-07-29_
