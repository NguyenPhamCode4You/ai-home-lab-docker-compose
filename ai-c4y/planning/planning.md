# ProgressiveAgentSLM — Planning & Progress Tracker

> **ProgressiveAgentSLM** is a single, **recursive** agent class optimized for **local / small
> language models (SLMs)**. One instance owns an identity, a four-tier **token budget**
> (`context_window`), a **ladder** of **models** (local→cloud, with per-model retry/switch limits),
> a set of **reasoning** policies (`when → then`), a set of **tools** (Supabase vector search,
> todo, write-file, search-file, vector-memory, skills), and a set of **delegates** — which are
> themselves `ProgressiveAgentSLM` instances. The agent _progressively_ builds a lightweight
> **cognitive index** over an **append-only worklog** (its single source of truth), retrieving only
> the blocks it needs back into a bounded working window — so quality comes from disciplined memory
> handling, not a bigger model. Every agent and delegate reads and writes the same worklog in the
> run's **wip** folder, so teammates can loop back over each other's work.
>
> Any model slot can be escalated, plug-and-play, to a more capable **cloud** model (OpenRouter). The
> class reuses existing primitives (`Task`, model clients, `SupabaseVectorStore`, `DocumentRanking`,
> `PythonCodeExecute`, `KnowledgeCompression`, `IterationSummarizer`, `AnswerEvaluator`,
> `FinalThoughtSummarizer`) and drops into `create_chat_backend` unchanged.

**Status legend:** ⬜ Not started · 🟡 In progress · ✅ Done · ⛔ Blocked

---

## 1. Vision & Design Philosophy

- **One recursive class.** Everything is a `ProgressiveAgentSLM`. A "team" is simply an agent whose `delegates` are other agents — composition _is_ recursion; there is no separate orchestrator type. Each agent carries its own `agent_id` + `description` so any parent can decide when to hand it a sub-question.
- **Progressive cognition by indexing, not stuffing.** The context window is partitioned into four tiers (§3), each backed by a file in the run's **wip** folder (§8). Instead of accumulating everything in the prompt, the agent appends its work to an **append-only `raw_worklog.log`** and builds a **`cognitive_index`** — a compact map of ~10–20-token pointers into that log. To think, it looks up the index and pulls only the relevant blocks back into a bounded `context_window.log`. On small models, quality comes from disciplined memory handling — not a bigger model.
- **Local & SLM-first, cloud optional.** `models` is a priority **ladder** (highest → lowest). Local Ollama models do the frequent work; a cloud model (OpenRouter) sits lower as an automatic fallback, or is promoted to the top for hard steps. Each model gets a bounded number of self-evaluation attempts before the agent **switches to the next model** on the ladder (§4).
- **Behavior by policy, not by code.** `reasoning` is a list of `when → then` rules rendered into the system prompt every iteration — it both steers how a small model thinks (deep-think, double-check, visualize, say-no) and acts as the run's **todo checklist**. Policies are declarative only (no per-policy models); a non-programmer shapes behavior without touching Python.
- **One append-only worklog, shared by the whole team.** Every agent and delegate writes finished blocks into the same `raw_worklog.log` (the single source of truth) through one serialized writer, and indexes them in `cognitive_index`. Delegates deliver their final answer to the parent when done, but their work stays in the shared log so any later agent can **loop back** over it via the index.
- **`when`-gated routing.** Delegates and tools each carry an optional `when`; a cheap pre-pass prunes the menu to the entries whose `when` matches, then the small model picks from the short list — fewer options, better selection. The top agent's own `when` gates when it answers directly vs. delegates.
- **Reuse, don't rebuild.** Async streaming generators that `yield` chunks, DI via constructor kwargs, `Task`-subclass agents, prompt-based JSON with robust regex fallbacks, JSON-file config/state. New code lives under `src/framework/`; existing files are touched minimally.

---

## 2. The `ProgressiveAgentSLM` Object

A single class configured by one object (JSON or Python). Every field has a sensible default; only `agent_id`, `description`, and at least one `model` are required.

| Field                                            | Type        | Meaning                                                                                                                                                                                                                     |
| ------------------------------------------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`                                       | str         | Stable identifier. Used by a parent to address this agent (`delegate:<agent_id>`) and as its section in the shared worklog.                                                                                                 |
| `description`                                    | str         | One-line capability summary. Read by a parent agent to decide **when** to delegate here.                                                                                                                                    |
| `when`                                           | str \| null | **Optional gate** (§7). For a delegate: the condition under which the parent should route to it. For the top agent: when it should answer **directly** vs. delegate. Used to prune the routing menu before the model picks. |
| `wip`                                            | str         | Directory for the run's four-file worklog subsystem (§8). Delegates share the parent's `wip` (one shared log per run).                                                                                                      |
| `context_window`                                 | object      | The four-tier token budget (§3), each tier backed by a wip file — the heart of the design.                                                                                                                                  |
| `max_iterations_untill_give_up`                  | int \| null | Global cap on total self-iterations before aborting. Default **50**. `null` → iterate until the user cancels.                                                                                                               |
| `max_iterations_untill_give_up_and_switch_model` | int         | Per-model quality-failure budget. Default **5**. After this many failed self-evaluations on the current model, **switch to the next model** on the ladder (§4).                                                             |
| `max_infra_retries_per_model`                    | int         | **Separate** budget for infra failures (timeout / HTTP error) per model. Default **3**. Exhausting it falls through to the next model without consuming the quality budget.                                                 |
| `models`                                         | list        | Priority **ladder** (§4), highest first. Each model gets its own quality + infra budgets; a successful iteration resets the ladder to the top model.                                                                        |
| `reasoning`                                      | list        | `when → then` behavioral policies (§5) rendered into the system prompt each iteration; also the run's todo checklist. Declarative only — no per-policy models.                                                              |
| `tools`                                          | list        | Capabilities the agent may call, each with a `when` guidance string (§6): Supabase, todo, write-file, search-file, vector-memory, skills, …                                                                                 |
| `delegates`                                      | list        | Nested `ProgressiveAgentSLM` configs (§7). The agent routes `when`-matched sub-questions to them by `agent_id` / `description`.                                                                                             |

> **Inheritance:** a delegate that omits `models`, `max_iterations_untill_give_up`, `max_iterations_untill_give_up_and_switch_model`, or `max_infra_retries_per_model` **inherits the parent's**. It also shares the parent's `wip` (hence the shared `raw_worklog.log` + `cognitive_index`), while keeping its **own** `context_window.log` + `response_window.log`. `context_window`, `reasoning`, `tools`, and `when` are per-agent (not inherited), so each delegate is independently budgeted and specialized.

---

## 3. `context_window` — the four-tier progressive token budget

Each tier is a **named token budget backed by a file** in the run's `wip` folder (§8). Instead of stuffing accumulated history into the prompt, the agent keeps the full record in an append-only `raw_worklog.log` and a `cognitive_index` map over it; the tiers below bound what actually enters the prompt each step.

| Tier                            | Default | Backing file (§8)       | Holds                                                                                                                                 | Budget / compaction rule                                                                                                                                                              |
| ------------------------------- | ------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_awareness_tokens` | 800     | _(in-prompt header)_    | The ongoing user-facing chat history the agent may see.                                                                               | If **0**, its budget is **donated to the next tier** — the agent "stops listening to chat" and thinks harder.                                                                         |
| `cognitive_tokens`              | —       | `cognitive_index.jsonl` | The **index**: one ~10–20-token pointer per block → its line range in `raw_worklog.log`. **Not** compressed knowledge — a lookup map. | Grows one entry per block. When `cognitive_index` **+** `context_window` exceed budget, a **progressive reflection** compacts both to **50%** (merging pointers into coarser ranges). |
| `context_tokens`                | —       | `context_window.log`    | The current working set: blocks pulled from `raw_worklog` via the index, retrieved knowledge, tool outputs, the sub-question.         | Streamed into each iteration; when over budget, compacted to **50%** (stale blocks dropped — still recoverable from `raw_worklog`).                                                   |
| `answering_tokens`              | —       | `response_window.log`   | The latest answer the agent is emitting for this iteration.                                                                           | Hard output cap. Flushed to `raw_worklog` + indexed, then **cleared** for the next iteration.                                                                                         |
| _(unbounded)_                   | —       | `raw_worklog.log`       | Every finished block from every agent/delegate — the **single source of truth**.                                                      | **Append-only, never rewritten.** No budget; this is what makes the 50% compactions above safe (nothing is truly lost).                                                               |

**Prompt assembly per step** (the system prompt is separate overhead):

```
[ system: description + reasoning(when→then, todo) + when-gated tool/delegate guidance ]
[ conversation awareness       ≤ conversation_awareness_tokens ]
[ cognitive index (relevant pointers) → pulled blocks   ≤ context_tokens ]
[ current context / KB / tools ≤ context_tokens ]
[ question ]
→ answer                       ≤ answering_tokens  (response_window.log)
```

**Core loop invariant — index & retrieve, then compact:**

```
per block b produced (delegate answer / tool result / iteration answer):
    raw_worklog.append(b)                      # append-only source of truth
    cognitive_index.append(pointer(b))         # {block_id, agent, iter, raw_lines, summary≈10-20 tok, keywords}

per iteration:
    context_window ← retrieve(cognitive_index, question)   # pull only relevant blocks from raw_worklog
    if size(context_window) + size(cognitive_index) > budget:
        reflect_and_compact(target = 0.5 * current_size)   # merge pointers / drop stale blocks (recoverable)
    response_window ← answer(prompt)                        # ≤ answering_tokens
    flush(response_window → raw_worklog + cognitive_index); clear(response_window)
```

The total request size ≈ the sum of the four in-prompt tiers (+ system overhead), which is used to **auto-infer** the model token requirement (§4). Because `raw_worklog` is immutable, `cognitive` is a pure **index** (not a compressed blob), and compaction only ever touches the derived views — the agent can shrink its working memory aggressively and still recover any detail by following a pointer back into the raw log.

---

## 4. Models — per-agent priority chain

`models` is an ordered list, highest priority first. Each entry:

| Key          | Required   | Meaning                                                                                                 |
| ------------ | ---------- | ------------------------------------------------------------------------------------------------------- |
| `platform`   | yes        | `ollama` (local) or `open_router` (cloud). Maps to the existing `Ollama` / `OpenRouter` clients.        |
| `name`       | yes        | Model name on that platform.                                                                            |
| `url`        | for ollama | Endpoint (defaults to `OLLAMA_URL`).                                                                    |
| `max_tokens` | no         | Context ceiling. A number caps it; `"auto"` (or omitted) sizes the request to the `context_window` sum. |

**Selection & the ladder.** Walk the list top-down; the active model is the first whose `max_tokens` ≥ the required budget (auto-inferred from §3) **and** that is reachable. The list is a **ladder** with two independent, per-model budgets:

- **Quality budget — `max_iterations_untill_give_up_and_switch_model` (default 5).** After each iteration the agent runs a **quick self-evaluation**; a "not good enough" verdict is a _quality failure_. When the current model accrues this many quality failures, the agent **switches to the next model** on the ladder (and resets the per-model counter to 0).
- **Infra budget — `max_infra_retries_per_model` (default 3).** A timeout / HTTP / unreachable error is an _infra failure_, tracked **separately** (a slow GPU must not look like a wrong answer). Exhausting it falls through to the next model immediately, without consuming the quality budget.
- **Success resets the ladder.** When a model handles an iteration successfully, the ladder pointer resets to the **top** model for the next iteration (the cheapest capable model is always tried first).
- **Stopping.** The run stops when the ladder is **exhausted** (the last model uses up its quality budget) **or** total iterations reach `max_iterations_untill_give_up` (default 50) — whichever comes first. With a 10-model ladder at 5 each, both limits coincide at 50.

This is the per-agent generalization of a role-based registry — local-first with cloud as an automatic backstop, or cloud promoted by putting it first.

```json
"models": [
  { "platform": "ollama",      "name": "gpt-oss:20b",                 "url": "http://localhost:11434", "max_tokens": 62000 },
  { "platform": "open_router", "name": "anthropic/claude-3.5-sonnet", "max_tokens": "auto" }
]
```

---

## 5. Reasoning — `when → then` behavioral policies

`reasoning` is a list of rules that shape the agent's behavior. Each rule renders into the system prompt **every iteration** as "**When** _condition_, **then** _action_." This serves two jobs at once: it steers how a small model thinks, and it acts as the run's **todo checklist** the model re-reads each pass to stay on task. Policies are **declarative only** — they carry no per-policy `models`; model choice is governed globally by the ladder (§4), so authoring stays simple and one policy can't fragment the model routing.

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
| `ReadFileTool`        | `root`                                          | Read a file's contents (sandboxed to `root`, default the `wip` folder).                                                                                                                                                                                                                                               |
| `SearchFileTool`      | `root`, `kind: name\|content`, `glob?`          | Locate files by name/glob or find where a term/symbol appears (ripgrep-style); returns path + line + snippet. Read-only, sandboxed.                                                                                                                                                                                   |
| `WriteFileTool`       | `root`, `mode: overwrite\|append`, `approval`   | Persist an artifact (notes, generated code, a report). **Sandboxed to `root`; path traversal / absolute escapes rejected** (OWASP A01/A03). Optional approval hook (default allow, home-lab). Reuses `FileHanlder`.                                                                                                   |
| `TodoTool`            | —                                               | Maintains the run's checklist (`todo.md` in `wip`). The model **rewrites the whole list** (`[{id, content, status: pending\|in_progress\|completed}]`); the loop re-injects it each iteration (anti-drift).                                                                                                           |
| `VectorMemoryTool`    | `function_name` (recall), `write_function_name` | The agent's **own, cross-run, writable** long-term memory (distinct from the read-only KB). `recall(query, k)` + `remember(text, tags?)`, backed by a Supabase memory table reusing `Embedding`. Naturally embeds `cognitive_index` summaries for semantic recall.                                                    |
| `SkillTool`           | `skills_dir`                                    | On-demand **procedure packs** (progressive disclosure): each skill file has `{ id, description, when }` frontmatter + a body of steps. Only id/description/when are always visible; the body loads when its `when` matches. **Trusted-local files only** (loading external skill text is a prompt-injection surface). |
| `GenerateDiagramTool` | —                                               | Emits Mermaid for the `visualize_diagram` policy.                                                                                                                                                                                                                                                                     |
| `RunPythonTool`       | `approval`                                      | Wraps `PythonCodeExecute`; optional approval (default allow). ⚠️ Autonomous execution — revisit before any non-local use.                                                                                                                                                                                             |

---

## 7. Delegates — recursive composition

`delegates` is a list of **nested `ProgressiveAgentSLM` configs**. There is no separate "sub-agent" type — a delegate is a full agent with its own `context_window`, `tools`, `when`, and optional `reasoning` / `models` / `delegates`. The parent:

1. **Prunes then routes.** A cheap pre-pass keeps only the delegates and tools whose **`when`** matches the current sub-question (the parent's own `when` decides if it should just answer directly). The small model then picks from that short menu via the proven `_parse_agent_routing` JSON pattern, generalized to `delegate:<agent_id>`. Fewer options → far more reliable SLM routing.
2. **Hands the sub-question down.** The delegate runs its **own** full progressive loop with its own `context_window.log` + `response_window.log`, but writes finished blocks into the **shared** `raw_worklog.log` + `cognitive_index` (one per run) under its own `agent_id`.
3. **Delivers when done.** Unlike the parent's live stream, a delegate returns only its **final** answer to the parent; the parent folds that block into its own `context_window` (by index lookup) and continues. Because the delegate's full work remains in the shared log, any **later** agent or delegate can loop back over it via the index.

Depth is bounded by `max_iterations_untill_give_up` at each level plus an overall recursion cap. Two RAG-backed delegates (`bvms-general-knowledge`, `bvms-code-knowledge`), each owning a Supabase function and a `when`, is the canonical example (§13).

---

## 8. The Worklog — the four-file `wip` memory subsystem

The worklog is a **four-file subsystem** living in the run's `wip` folder (`wip/<run_id>/`, from the `wip` config field). It replaces the old `runs/` artifacts. `raw_worklog.log` + `cognitive_index` are **shared** by the whole team (single source of truth); `context_window.log` + `response_window.log` are **per-agent**.

| File                    | Scope     | Written by                        | Role                                                                                                                                                                                                 |
| ----------------------- | --------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `raw_worklog.log`       | shared    | one **serialized writer** per run | **Append-only, never rewritten.** Every finished block (any model, main or delegate) is patched in as a delimited block with a stable line range. The single source of truth everyone loops back to. |
| `cognitive_index.jsonl` | shared    | the same writer                   | One **pointer record per block**: a ~10–20-token summary + the `raw_worklog` line range. The searchable **map** used to pull only relevant blocks back into a working window.                        |
| `context_window.log`    | per-agent | the owning agent                  | The agent's current working set, streamed to as it works; compacted to 50% when it exceeds `context_tokens`.                                                                                         |
| `response_window.log`   | per-agent | the owning agent                  | The agent's **latest** answer only; flushed to `raw_worklog` + `cognitive_index`, then **cleared** each iteration.                                                                                   |

**A "block"** is one unit of finished work — a delegate's answer, a tool result, or an iteration's answer. Blocks are **flushed at completion** (not token-by-token): the writer buffers the output, then appends the whole block so line ranges stay intact and parallel delegates never interleave.

**The write path, per block:**

1. The agent streams into its own `context_window.log` / `response_window.log` while working.
2. On block completion, it enqueues the block to the run's **single writer**, which:
   a. appends the block to `raw_worklog.log` and records its `[start_line, end_line]`;
   b. appends one record to `cognitive_index.jsonl` (a cheap ~10–20-token summary via `KeywordExtractor` / `SimpleEntityExtractor`, an LLM summary only when needed).
3. `response_window.log` is cleared for the next iteration.

**The read path (index-and-retrieve).** To assemble its next prompt an agent does **not** replay the whole log; it queries `cognitive_index` (by keyword, and later by `VectorMemoryTool` embeddings), takes the matching line ranges, and pulls **only those blocks** from `raw_worklog` into `context_window.log`. This is RAG over the team's own worklog — the core trick that keeps SLM prompts small.

**Progressive reflection (compaction).** When `context_window.log` **+** `cognitive_index` exceed their budgets (`context_tokens`, `cognitive_tokens`), a reflection compacts **both to 50% of current size**: index pointers are merged into coarser line ranges, and stale context blocks are dropped. Nothing is lost — `raw_worklog` is immutable, so any dropped detail is one pointer-lookup away.

**Delegate coordination.** Delegates share this exact behavior. The only difference: a delegate returns just its **final** answer to its parent, but its full work lands in the shared `raw_worklog` under its `agent_id`, so a later teammate can loop back over it via the index.

```
wip/<run_id>/
  raw_worklog.log        # ← shared, append-only single source of truth (delimited blocks + line ranges)
  cognitive_index.jsonl  # ← shared, one ~10–20-token pointer per block → raw_worklog line range
  context_window.log     # ← per-agent working set (compacts to 50% over budget)
  response_window.log    # ← per-agent latest answer (flushed to raw + index, then cleared each iteration)
  todo.md                # ← TodoTool checklist (re-injected each iteration)
# wip/index.db           # optional SQLite FTS5 over raw_worklog + cognitive_index (LogSearch)
```

---

## 9. Goals → Components

| Goal (user)                                                                         | Realized by                                                                                                                                                                        |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Single recursive class anyone can configure (one object)                            | `ProgressiveAgentSLM` + `AgentConfig` + `config/load.py`                                                                                                                           |
| **Goal**: stay focused on the user-set goal                                         | `reasoning` policies + double-check / re-iterate loop (reuse `AnswerEvaluator`)                                                                                                    |
| **Knowledge**: text files + Supabase vector DB + own long-term memory               | `SupabaseTool` (primary, pgvector) + `FileKnowledgeTool` + `VectorMemoryTool` (writable, cross-run)                                                                                |
| **Tools**: KB, files, search, write, todo, memory, skills, diagrams, python         | `ToolRegistry` + `tools/` (`SupabaseTool`, `ReadFileTool`, `SearchFileTool`, `WriteFileTool`, `TodoTool`, `VectorMemoryTool`, `SkillTool`, `GenerateDiagramTool`, `RunPythonTool`) |
| **Cognition**: index the worklog, retrieve only what's needed, compact safely       | `CognitiveIndex` (pointer map) + `Reflector` 50% compaction (reuse `KnowledgeCompression` + `IterationSummarizer`)                                                                 |
| **Delegate**: `when`-gated routing, break into sub-agents, collect results          | Recursive `delegates` + `Router` (`when`-pruned `delegate:<agent_id>`) dispatch                                                                                                    |
| **Worklog**: one append-only shared source of truth + per-agent working windows     | Four-file `wip` subsystem (`raw_worklog` + `cognitive_index` shared; `context_window` + `response_window` per-agent)                                                               |
| Local/SLM-first with a model **ladder** (per-model switch + separate infra retries) | `ModelChain` (ladder + `max_iterations_untill_give_up_and_switch_model` + `max_infra_retries_per_model`)                                                                           |
| Per-step logging to terminal + files for full-text search                           | `RunLogger` (block/JSONL) + `LogSearch` (SQLite FTS5 over the wip logs)                                                                                                            |
| Workflow configurable via JSON **and** Python                                       | `config/load.py` (`example.json` + `schema.json`) + `ProgressiveAgentSLM(...)`                                                                                                     |

---

## 10. Design Decisions

| Topic                | Decision                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent & control flow | **Recursive progressive loop** — each step assembles the four-tier prompt, applies reasoning policies, calls tools / routes to delegates, then folds context+answer into `cognitive`; iterate up to `max_iterations_untill_give_up`.                                                                                                                                                                                                               |
| Delegation           | **Follow `AssistantOrchestra`** routing (`_parse_agent_routing`), generalized to `delegate:<agent_id>`; a parent routes by reading each delegate's `description`. Delegates inherit `models` + `max_iterations_untill_give_up`.                                                                                                                                                                                                                    |
| Models (defaults)    | **Per-agent ladder** (highest→lowest): first reachable model that fits the budget wins. Each model gets `max_iterations_untill_give_up_and_switch_model` quality attempts (from the quick self-eval) + a **separate** `max_infra_retries_per_model`; success resets the ladder to the top; abort at `max_iterations_untill_give_up` (50). **OpenRouter** cloud as automatic fallback or promoted to top; `max_tokens: "auto"` sizes to the budget. |
| Worklog & memory     | **Four-file `wip` subsystem.** Shared **append-only** `raw_worklog.log` (single source of truth) + `cognitive_index.jsonl` (pointer map); per-agent `context_window.log` + `response_window.log`. Blocks flush at completion via one serialized writer; **`cognitive` is an index, not a compressed blob**; progressive reflection compacts working views to 50%.                                                                                  |
| Tool safety          | **Trust-local / ungated** (home-lab), but `WriteFileTool` / `SearchFileTool` / `ReadFileTool` are **sandboxed to a `root`** (default the `wip` folder) with path-traversal rejection (OWASP A01/A03); `skills` load **trusted-local files only**. Optional **no-op approval hook (default allow)** on `RunPythonTool` / `WriteFileTool`. ⚠️ Autonomous code execution can be destructive; revisit before any non-local use.                        |
| Tool-call protocol   | **Both** — native Ollama `/api/chat` tool-calling when supported; **prompted-JSON + robust parser** fallback for small models.                                                                                                                                                                                                                                                                                                                     |
| Logging & search     | **JSONL events + per-run Markdown transcript + SQLite FTS5 index** for full-text search.                                                                                                                                                                                                                                                                                                                                                           |
| Sequencing           | **Phased** — MVP core agent first, then full tools/reflection, then workflow config, then hardening.                                                                                                                                                                                                                                                                                                                                               |
| Workflow config      | **JSON (`example.json`) + Python construction**, both via `config/load.py` with delegate inheritance + `schema.json` validation.                                                                                                                                                                                                                                                                                                                   |
| Isolation            | All new code under `src/framework/`. Existing files minimally touched (async `SupabaseVectorStore`, Ollama `/api/chat`).                                                                                                                                                                                                                                                                                                                           |

---

## 11. Target Package Layout

```
src/framework/
  __init__.py
  ProgressiveAgentSLM.py         # the single recursive agent class: owns context_window, models, reasoning, tools, delegates; runs the progressive loop and recurses into delegates
  AgentConfig.py                 # parsed config: agent_id, description, when, wip, context_window, max_iterations_untill_give_up (+ _and_switch_model, max_infra_retries_per_model), models[], reasoning[], tools[], delegates[] (+ inheritance from parent)
  ContextWindow.py               # four-tier budget mapped to the wip files: conversation_awareness / cognitive_index / context_window / response_window; cascade-on-zero + 50% compaction; auto-infers required model tokens
  ModelChain.py                  # per-agent ladder → first model that fits + is reachable; per-model quality budget (max_iterations_untill_give_up_and_switch_model) + separate infra budget (max_infra_retries_per_model); success resets to top; platform factory; max_tokens "auto"
  ReasoningPolicy.py             # renders when → then rules into the system prompt
  ToolRegistry.py                # Tool base + dispatch; each tool carries a `when` guidance string
  agents/
    Reflector.py                 # progressive reflection: compacts context_window + cognitive_index to 50% when over budget; raw_worklog stays intact (index, not a compressed blob)
    Router.py                    # reads each delegate.description → picks delegate(s) for a sub-question (generalized _parse_agent_routing → delegate:<agent_id>)
  tools/
    SupabaseTool.py              # PRIMARY: pgvector RPC via SupabaseVectorStore.async_query; optional parallel DocumentRanking when ranking=true
    ReadFileTool.py              # sandboxed read (root, default wip)
    SearchFileTool.py            # sandboxed name/content search (ripgrep-style) → path + line + snippet
    WriteFileTool.py             # sandboxed write (root, path-traversal rejected); optional approval; reuses FileHanlder
    TodoTool.py                  # rewrites wip/todo.md checklist; re-injected each iteration (anti-drift)
    VectorMemoryTool.py          # writable cross-run memory: recall()/remember() over a Supabase memory table (reuses Embedding)
    SkillTool.py                 # on-demand procedure packs from skills_dir (progressive disclosure; trusted-local)
    GenerateDiagramTool.py       # emits Mermaid for the visualize_diagram policy
    RunPythonTool.py             # wraps tools/PythonCodeExecute; optional approval (default allow)
    FileKnowledgeTool.py         # files-type knowledge source
  logging/
    RunLogger.py                 # owns the wip run dir; terminal + block events; single serialized writer
    Worklog.py                   # coordinator for the four-file subsystem (raw_worklog + cognitive_index + context_window + response_window)
    RawWorklog.py                # append-only raw_worklog.log; append(block) → [start_line, end_line]
    CognitiveIndex.py            # cognitive_index.jsonl pointer map; append(pointer)/search()/compact(0.5)
    ContextWindowLog.py          # per-agent context_window.log; stream()/retrieve(index)/compact(0.5)
    ResponseWindow.py            # per-agent response_window.log; write()/flush→raw+index/clear()
    LogSearch.py                 # SQLite FTS5 index (wip/index.db) over raw_worklog + cognitive_index + search() + CLI
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

- [~] `ContextWindow.py`: four-tier budget (`conversation_awareness` / `cognitive` / `context` / `answering`), cascade-on-zero donation, budget-bounded trimming, required-token auto-inference (§3). _(new)_
- [~] `ModelChain.py`: per-agent **ladder** → first reachable model that fits the budget; per-model quality budget `max_iterations_untill_give_up_and_switch_model` (from the quick self-eval) + **separate** `max_infra_retries_per_model`; success resets to the top model; platform factory (`ollama`→`Ollama`, `open_router`→`OpenRouter`); `max_tokens: "auto"` sizing (§4). _(reworks `ModelRegistry`)_
- [x] Make `SupabaseVectorStore` async: `async_query` + `async_get_documents_string` via `httpx.AsyncClient` (sync preserved). _(IMPROVEMENTS.md §2)_
- [~] `logging/` four-file **wip** subsystem (§8): append-only `RawWorklog` (block append → line range) + `CognitiveIndex` (pointer map, cheap keyword summaries) + per-agent `ContextWindowLog` + `ResponseWindow`, coordinated by `Worklog` behind **one serialized writer**; `RunLogger` owns `wip/<run_id>/`. _(reworks the old worklog.md/events.jsonl/transcript.md)_
- [ ] Progressive reflection: compact `context_window.log` + `cognitive_index` to **50%** when over `context_tokens` / `cognitive_tokens` (merge pointers / drop stale blocks; recoverable from raw). _(new)_

### Phase 1 — Recursive core agent (runnable vertical slice) 🟡

- [~] `AgentConfig.py`: parse `agent_id`, `description`, `when`, `wip`, `context_window`, `max_iterations_untill_give_up` (default 50, `null`→infinite), `max_iterations_untill_give_up_and_switch_model` (default 5), `max_infra_retries_per_model` (default 3), `models[]`, `reasoning[]`, `tools[]`, `delegates[]`; apply parent→delegate inheritance of the model ladder + iteration budgets + shared `wip`.
- [~] `ProgressiveAgentSLM.py`: the single recursive class. Per step — retrieve relevant blocks from `raw_worklog` via `cognitive_index` into `context_window`, assemble the four-tier prompt, select a model from the ladder, apply reasoning policies, `when`-prune then route to delegates/tools, emit ≤ `answering_tokens` into `response_window`, flush the block to `raw_worklog` + `cognitive_index`, quick self-eval (switch model on repeated failure). Recurse into `delegates`; stop at `max_iterations_untill_give_up`.
- [~] `agents/Router.py`: `when`-prune the delegate/tool menu, then choose delegate(s) per sub-question via the generalized `_parse_agent_routing` (`delegate:<agent_id>`); the parent's own `when` gates direct-answer. _(reworks Forwarder)_
- [~] `agents/Reflector.py`: the cognitive-accumulation compressor (reuse `KnowledgeCompression` + `IterationSummarizer`).
- [~] `ToolRegistry.py` + `tools/SupabaseTool.py` (primary; `function_name` + `ranking`) + `tools/ReadFileTool.py` + `tools/TodoTool.py`; each tool carries its `when` guidance (used for menu pruning).
- [~] Wire `RunLogger` + the four-file `Worklog` subsystem (single serialized writer); `progressive_agent_slm_demo.py` via `create_chat_backend` (port 8001).

### Phase 2 — Full tools, reasoning policies, model routing ⬜

- [ ] Remaining tools: `SearchFileTool` + `WriteFileTool` (sandboxed to `root`), `VectorMemoryTool` (cross-run memory over a Supabase table), `SkillTool` (progressive-disclosure procedure packs), `GenerateDiagramTool` (Mermaid), `RunPythonTool` (wrap `PythonCodeExecute`, optional approval), `FileKnowledgeTool`.
- [ ] `ReasoningPolicy.py`: render `when → then` rules into the system prompt; ship the baseline set (deep_think, double_check, visualize_diagram, say_no).
- [ ] Supabase ranking path: parallel `DocumentRanking` batches (reuse `RagAssistant.stream`) when `ranking: true`.
- [ ] Budget enforcement: measure tokens (tokenizer or char-approx), trim each tier to budget, implement cascade-on-zero donation.
- [ ] `logging/LogSearch.py`: SQLite FTS5 index (`wip/index.db`) over `raw_worklog` + `cognitive_index` + search + CLI over all runs.

### Phase 3 — Config loader (JSON + Python) ⬜

- [ ] `config/load.py` + `config/schema.json`: build a `ProgressiveAgentSLM` tree from `example.json` (or a Python dict) with validation + delegate inheritance.
- [ ] Round-trip the canonical `example.json` (§13) end-to-end as a worked example + regression check; authoring README.

### Phase 4 — Hardening ⬜

- [ ] Unit tests: config loader/inheritance, four-tier budgeting + cascade, `cognitive_index` pointer append + 50% compaction (line-range integrity), model-ladder switch (quality vs. infra budgets) + success-reset, router `when`-pruning parser, Supabase tool, four-file `Worklog` append/read behind one writer, `RunLogger` JSONL+FTS round-trip.
- [ ] Integration smoke test with a stub model implementing `.stream`.
- [ ] Timeouts/retries (reuse 429/backoff from `OpenRouter`); model fall-through.
- [ ] Optional approval hook (default allow) on `RunPythonTool` / any shell tool.

---

## 13. Example: The `bvms-assistant` Config

The canonical configuration (live copy: `src/framework/example.json`). It defines a top orchestrator with **two RAG-backed delegates** — each delegate is itself a full `ProgressiveAgentSLM` with its own four-tier budget and its own Supabase function. The same tree can be authored in JSON or built in Python; both produce the same agent and drop into `create_chat_backend`.

### 13a. JSON (declarative, recursive)

```json
{
  "agent_id": "bvms-assistant",
  "description": "Top orchestrator. Answers BVMS questions by combining domain knowledge, code analysis, and diagrams, delegating to specialist sub-agents when needed.",
  "when": "Answer directly only for simple/general questions; otherwise decompose and delegate.",
  "wip": "wip/bvms-assistant",

  "context_window": {
    "conversation_awareness_tokens": 800,
    "cognitive_tokens": 7200,
    "context_tokens": 24000,
    "answering_tokens": 9200
  },
  "max_iterations_untill_give_up": 50,
  "max_iterations_untill_give_up_and_switch_model": 5,
  "max_infra_retries_per_model": 3,

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
      "max_tokens": "auto"
    }
  ],

  "reasoning": [
    {
      "id": "deep_think",
      "when": "The question is complex or spans multiple topics.",
      "then": "Break it into sub-questions; decide which delegate(s)/tool(s) each part needs."
    },
    {
      "id": "double_check",
      "when": "All delegates and tools for this iteration have returned.",
      "then": "Verify the evidence answers the question; re-iterate if gaps remain and iterations are left."
    },
    {
      "id": "visualize_diagram",
      "when": "The answer involves a workflow, architecture, or relationships.",
      "then": "Call GenerateDiagramTool to produce a Mermaid diagram alongside the text."
    },
    {
      "id": "say_no",
      "when": "No clear answer after exhausting the relevant delegates and tools.",
      "then": "Say honestly the answer is not available; never invent one."
    }
  ],

  "tools": [
    {
      "type": "ReadFileTool",
      "root": "wip/bvms-assistant",
      "when": "A referenced local file's contents are needed."
    },
    {
      "type": "SearchFileTool",
      "root": "wip/bvms-assistant",
      "when": "Locate a file or find where a term/symbol appears before reading."
    },
    {
      "type": "WriteFileTool",
      "root": "wip/bvms-assistant",
      "approval": false,
      "when": "Persist an artifact (notes, code, a report) inside the sandbox."
    },
    {
      "type": "TodoTool",
      "when": "Start/refresh the run checklist so the agent stays on-task across iterations."
    },
    {
      "type": "VectorMemoryTool",
      "function_name": "match_agent_memory",
      "write_function_name": "insert_agent_memory",
      "when": "Recall a durable fact from past runs, or remember a new one."
    },
    {
      "type": "SkillTool",
      "skills_dir": "skills",
      "when": "A recurring, well-defined procedure applies; load its steps on demand."
    },
    {
      "type": "GenerateDiagramTool",
      "when": "A visual diagram would make a workflow or architecture clearer."
    }
  ],

  "delegates": [
    {
      "agent_id": "bvms-general-knowledge",
      "description": "Business workflow & domain knowledge about BVMS — architecture, components, features.",
      "when": "The question is about how BVMS behaves for the business (not code internals).",
      "context_window": {
        "conversation_awareness_tokens": 1500,
        "cognitive_tokens": 4000,
        "context_tokens": 28000,
        "answering_tokens": 10000
      },
      "tools": [
        {
          "type": "Supabase",
          "function_name": "match_n8n_documents_bvms_neo",
          "ranking": true,
          "when": "Primary source for how BVMS works: architecture, components, workflows, features."
        }
      ]
    },
    {
      "agent_id": "bvms-code-knowledge",
      "description": "Deep technical & code aspects of BVMS — internals, code structure, APIs.",
      "when": "The question needs code-level ground truth: internals, structure, or APIs.",
      "context_window": {
        "conversation_awareness_tokens": 1500,
        "cognitive_tokens": 6000,
        "context_tokens": 34000,
        "answering_tokens": 18000
      },
      "tools": [
        {
          "type": "Supabase",
          "function_name": "match_n8n_code_bvms_neo",
          "ranking": true,
          "when": "Primary source for code-level questions: internals, structure, APIs."
        },
        {
          "type": "RunPythonTool",
          "approval": false,
          "when": "A quick calculation or snippet must be run to verify behavior."
        }
      ]
    }
  ]
}
```

The two delegates omit `models` and the iteration budgets, so they **inherit** them from the parent, and they share the parent's `wip` (one `raw_worklog.log` + `cognitive_index` for the whole run) while keeping their own `context_window.log` + `response_window.log`. Budgets sum to 41,200 / 43,500 / 59,500 tokens respectively — all within the local model's 62,000 ceiling.

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
    description="Top orchestrator for BVMS questions.",
    when="Answer directly only for simple/general questions; otherwise delegate.",
    wip="wip/bvms-assistant",
    context_window=dict(conversation_awareness_tokens=800, cognitive_tokens=7200,
                        context_tokens=24000, answering_tokens=9200),
    max_iterations_untill_give_up=50,
    max_iterations_untill_give_up_and_switch_model=5,
    max_infra_retries_per_model=3,
    models=[
        dict(platform="ollama", name="gpt-oss:20b", url="http://localhost:11434", max_tokens=62000),
        dict(platform="open_router", name="anthropic/claude-3.5-sonnet", max_tokens="auto"),
    ],
    reasoning=[
        dict(id="deep_think",   when="The question is complex.",            then="Decompose and route to delegate(s)/tool(s)."),
        dict(id="double_check", when="All delegates/tools have returned.",   then="Verify; re-iterate if gaps remain."),
        dict(id="say_no",       when="No answer after exhausting sources.",  then="Say so honestly; never invent."),
    ],
    tools=[
        dict(type="ReadFileTool", root="wip/bvms-assistant", when="A referenced local file is needed."),
        dict(type="TodoTool", when="Keep the run checklist current."),
        dict(type="VectorMemoryTool", function_name="match_agent_memory",
             write_function_name="insert_agent_memory", when="Recall/remember durable facts across runs."),
    ],
    delegates=[
        ProgressiveAgentSLM(
            agent_id="bvms-general-knowledge",
            description="Domain & workflow knowledge about BVMS.",
            context_window=dict(conversation_awareness_tokens=1500, cognitive_tokens=4000,
                                context_tokens=28000, answering_tokens=10000),
            tools=[dict(type="Supabase", function_name="match_n8n_documents_bvms_neo",
                        ranking=True, when="How BVMS works: architecture, features.")],
        ),  # inherits parent models + max_iterations
        ProgressiveAgentSLM(
            agent_id="bvms-code-knowledge",
            description="Code & technical internals of BVMS.",
            context_window=dict(conversation_awareness_tokens=1500, cognitive_tokens=6000,
                                context_tokens=34000, answering_tokens=18000),
            tools=[dict(type="Supabase", function_name="match_n8n_code_bvms_neo",
                        ranking=True, when="Code-level questions: internals, APIs.")],
        ),
    ],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_chat_backend(assistant), host="0.0.0.0", port=8001, timeout_keep_alive=300)
```

> A delegate that omits `models` / the iteration budgets inherits the parent's, and shares the run's
> `wip`. Each finished block is flushed into the shared append-only `raw_worklog.log` and mapped in
> `cognitive_index` (§8), so the two delegates can loop back over each other's work by index lookup
> rather than replaying the whole log.

---

## 14. Key Reuse Map (concrete)

| Existing asset                                                   | Reused for                                                                               |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `AssistantOrchestra.stream`                                      | `ProgressiveAgentSLM` per-step loop (route → execute → accumulate → reflect → iterate)   |
| `AssistantOrchestra._parse_agent_routing` / `_parse_eval_result` | `Router` delegate selection (`delegate:<agent_id>`) + double-check evaluation parsing    |
| `AssistantOrchestra.add_agent` / `agents` registry               | The recursive `delegates` registry (each keyed by `agent_id` + `description`)            |
| `all_agent_responses` + `IterationSummarizer` compaction         | Seed for `raw_worklog` blocks + the 50% progressive-reflection compaction                |
| `KnowledgeCompression`, `IterationSummarizer`                    | `Reflector` — the 50% compaction of `context_window` + `cognitive_index` (not a blob)    |
| `KeywordExtractor`, `SimpleEntityExtractor`                      | Cheap ~10–20-token `cognitive_index` summaries + keywords (LLM summary only when needed) |
| `SupabaseVectorStore` + `Embedding`                              | `VectorMemoryTool` — writable cross-run memory table (`remember`/`recall`)               |
| `FileHanlder` / `PythonCodeExecute`                              | `WriteFileTool` / `SearchFileTool` / `RunPythonTool` (sandboxed to `root`)               |
| `RagAssistant.stream` (parallel `DocumentRanking` batches)       | `SupabaseTool` ranking path (`ranking: true`)                                            |
| `SupabaseVectorStore.async_query`                                | `SupabaseTool` — the primary capability                                                  |
| `Task` + DI-kwargs pattern                                       | `Router`, `Reflector` agents                                                             |
| `AnswerEvaluator`, `FinalThoughtSummarizer`                      | `double_check` policy + final recap from the worklog                                     |
| `PythonCodeExecute`                                              | `RunPythonTool` (optional approval, default allow)                                       |
| `Ollama` (`/api/generate`) / `OpenRouter` (429 backoff)          | The per-agent `models` chain via the platform factory (local-first, cloud fallback)      |
| `ChatBackend.create_chat_backend`                                | Unchanged streaming integration point                                                    |

---

## 15. Verification

1. **Unit**: config loader + delegate inheritance, four-tier budgeting (trim + cascade-on-zero + auto token inference), `cognitive_index` pointer append + 50% compaction, model-ladder switch (quality vs. infra) + success-reset, `Router` `when`-pruned selection parser, `SupabaseTool`, four-file `Worklog` append/read (line-range integrity) behind one writer, `RunLogger` JSONL+FTS round-trip.
2. **Integration smoke**: load `example.json` with a stub model — assert the tree builds, the parent `when`-prunes then routes to a delegate, the delegate calls its Supabase tool and writes blocks under its own `agent_id`, `cognitive_index` grows yet stays ≤ its budget, and `raw_worklog.log` + `cognitive_index.jsonl` (+ per-agent `context_window.log` / `response_window.log`) exist and FTS search returns the run.
3. **Manual**: launch `progressive_agent_slm_demo.py` via uvicorn, ask a multi-step BVMS question, confirm streamed think/route/delegate/answer, per-block worklog flushing + index-and-retrieve, and on-disk logs searchable via the `LogSearch` CLI.
4. **Budget**: assert no request exceeds the selected model's `max_tokens`, and that a delegate omitting `models` inherits the parent's chain.

---

## 16. Open Questions

| #   | Question                                                                                 | Recommendation / Resolution                                                                                                                                                                 | Decision   |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| 1   | Recursion — is every delegate a full `ProgressiveAgentSLM`?                              | Yes; core to the design. Bound depth via `max_iterations_untill_give_up`.                                                                                                                   | ✅ Decided |
| 2   | Memory model — is `cognitive` compressed knowledge or an index?                          | An **index** (pointer map into append-only `raw_worklog`); four-file `wip` subsystem replaces the old `runs/` artifacts.                                                                    | ✅ Decided |
| 3   | Model switching — what counts as a "failed attempt"?                                     | **Quality** failure from the per-iteration quick self-eval drives switching (budget 5/model); **infra** failures use a **separate** budget (3/model). Success resets the ladder to the top. | ✅ Decided |
| 4   | Ladder exhaustion — loop, stop, or ladder-as-escalation?                                 | **Ladder-as-escalation** — walk once; abort at `max_iterations_untill_give_up` (50) or when the last model exhausts its budget.                                                             | ✅ Decided |
| 5   | Per-reasoning-step models?                                                               | **No** — reasoning stays declarative (system-prompt + todo); model choice is global via the ladder.                                                                                         | ✅ Decided |
| 6   | `when` gating — advisory or enforced?                                                    | **Hybrid** — a cheap pre-pass prunes the delegate/tool menu to `when`-matches, then the SLM picks; the top agent's `when` gates direct-answer.                                              | ✅ Decided |
| 7   | Token measurement for budgeting — real per-model tokenizer, or char≈token approximation? | Char-approx (reuse `CHARS_PER_TOKEN`) for P1; pluggable tokenizer in P2.                                                                                                                    | _TBD_      |
| 8   | `cognitive_index` summaries — cheap keyword extraction or LLM per block?                 | Keyword/entity extraction by default (`KeywordExtractor`); LLM summary only when needed.                                                                                                    | _TBD_      |
| 9   | `VectorMemory` scope & backing store — cross-run? Supabase table or local?               | Cross-run persistent; a dedicated Supabase memory table reusing `Embedding` (local store as a fallback).                                                                                    | _TBD_      |
| 10  | `wip` lifecycle — one ephemeral `wip/<run_id>/` per question; `VectorMemory` durable?    | Yes — `wip/<run_id>/` is per-run; durable cross-run knowledge lives in `VectorMemory`.                                                                                                      | _TBD_      |

---

## 17. Logging Artifacts & Event Schema

The four-file `wip` subsystem per run (see §8), replacing the old `runs/` artifacts:

- **`raw_worklog.log`** — shared, **append-only** single source of truth. Every finished block (any model, main or delegate) is patched in as a delimited block with a stable `[start_line, end_line]`. Never rewritten.
- **`cognitive_index.jsonl`** — shared **pointer map**: one record per block (schema below), used to retrieve only the relevant blocks back into a working window.
- **`context_window.log`** — per-agent working set; compacted to 50% over `context_tokens`.
- **`response_window.log`** — per-agent latest answer; flushed to raw + index, then cleared each iteration.
- **`wip/index.db`** _(optional)_ — SQLite FTS5 over `raw_worklog` + `cognitive_index` for `LogSearch`.

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

_Last updated: 2026-07-21_
