# ProgressiveAgentSLM — Planning & Progress Tracker

> **ProgressiveAgentSLM** is a single, **recursive** agent class tuned for **local / small language
> models (SLMs)**. One instance owns an identity, a `system_prompt`, a four-tier **context-window
> budget** (`context_window_breakdown`, expressed as **fractions** of the active model's context), a
> **ladder** of **models** (local→cloud, each with one retry budget), a set of **cognitive_behavior**
> policies (`when → then`), a set of **tools** (SQLite vector search, todo, write-file, search-file,
> vector-memory, skills, diagrams, python — each tool may run its own tool-calling model), a set of
> **working_folders** it may read / search (e.g.
> source code), and a set of **delegates** — which are themselves `ProgressiveAgentSLM` instances.
>
> The agent _progressively_ builds a lightweight **cognitive index** over an **append-only, segmented
> worklog** (sharded into per-iteration files under `worklog/`, its single source of truth) and
> retrieves only the blocks it needs back into a bounded working window — so quality comes from
> **disciplined memory handling, not a bigger model**. A background **metadata agent** distills every
> flushed block into a `knowledge_graph` (entities, keywords, a 25-word summary, workflow &
> relationships) that the index can jump to **by file / iteration / line** — or, optionally, query from
> a **graph** or **vector** database. Every agent and delegate shares the run's **worklog_folder** (so
> teammates can loop back over each other's work) and may read the user's **working_folders** side by
> side; subprocess fan-out runs sequentially or in parallel per **`parallel_supprocess`**. Any model
> slot can be escalated, plug-and-play, to a more capable **cloud** model (OpenRouter).
>
> The class reuses existing primitives (`Task`, model clients, `SqliteVectorStore` (sqlite-vec),
> `DocumentRanking`, `PythonCodeExecute`, `KnowledgeCompression`, `IterationSummarizer`,
> `AnswerEvaluator`, `FinalThoughtSummarizer`) and drops into `create_chat_backend` unchanged.

**Status legend:** ⬜ Not started · 🟡 In progress · ✅ Done · ⛔ Blocked

> **Revision 2026-08-08 — what changed & why (the memory model is now an explicit four-layer
> hierarchy, L1 → L4):**
>
> 1. **Four memory layers.** The worklog subsystem is reframed as **L1 raw → L2 facts → L3 situational
>    → L4 behavior** (§8): each layer is _derived_ from the one below and is progressively **hotter**
>    (closer to the live prompt) and smaller. This is a storage / refinement taxonomy that _composes_
>    with the §3 context-tier budget (which decides how much of each layer enters the prompt).
> 2. **L2 becomes first-class & searchable.** The distilled fact store (`knowledge/facts.db`,
>    sqlite-vec + FTS) is now **on by default** (was an optional mirror), fed by the metadata agent, and
>    queried by a dedicated **`KnowledgeSearchTool`** — "prepared tool code" for efficient knowledge
>    search over the run's own facts (§6, §8.3).
> 3. **L3 gains an in-prompt situational digest.** A **situational summarizer** distils L2 into
>    `situational.md` — a compact "what I know so far vs. the goal" that is **always injected** into the
>    situational tier of the prompt, regenerated only when L2 changes materially (§8.2, §3).
> 4. **Layer ↔ tier mapping.** L4 = the byte-stable **cached prefix**; L3 = the always-in-prompt
>    **situational tier**; L2 = pulled in **on demand by search tool**; L1 = pulled in **by pointer
>    seek** — so promotion up the layers is also promotion toward the prompt (§3, §8).

> **Revision 2026-08-07 — what changed & why (folded in from the Hermes study, see
> `analysis-against-hermes.md`):**
>
> 1. **Prompt-cache discipline.** The four-tier prompt is now assembled as a **byte-stable prefix**
>    (run-constant `system_prompt` + `cognitive_behavior` + tool / delegate descriptions) plus a
>    **volatile suffix** (retrieved blocks + answer). Rebuilding the prefix mid-run forces a full KV /
>    prompt-cache re-prefill — the dominant latency cost on a local SLM — so the prefix is held
>    identical until a **compaction**, the single sanctioned cache-invalidation event (§3).
> 2. **Enforcement, not just prompting.** The critical `cognitive_behavior` policies are now backed by
>    **deterministic turn-end guards** (`double_check` → verify-on-stop, `say_no` → grounding gate,
>    anti-drift → tool-loop guard) because SLMs ignore prompt-only rules (§5).
> 3. **Work vs. failover split.** `max_retries_until_switching_models` now triggers **model failover
>    only**; a **separate `max_iterations`** total-work budget (parent 200 / delegate 50, with a
>    **refund** for batched tool turns) bounds a run and a deep delegate tree independently (§2, §4).
> 4. **Adaptive compaction.** Reflection compacts **only enough to fit** (not a fixed 50%), protects
>    **head + tail**, and **updates** the prior summary (iterative, goal-tracking) rather than replacing
>    it (§3, §8).
> 5. **Hardened boundaries.** Delegates use a **typed immutable contract** (frozen request / result +
>    state machine + restricted toolset + byte caps) (§7); file tools add a **sensitive-path deny-list**
>    and instructional reads forbid pagination (§10); every external read is **byte- and deadline-
>    bounded** (§4); block text is **redacted on egress** to any other model (§8.2).
> 6. **Cheap-first, curated KG.** The metadata agent seeds entities / keywords / edges deterministically
>    (incl. lexical overlap) **before** any LLM call, and a background curator marks records
>    `stale` / `archived` — **never hard-deletes** (§8.2). Token budgeting is fixed to a single **`char/4`**
>    heuristic for both estimate and threshold (Open Q#8).

> **Revision 2026-08-06 — what changed & why (this pass):**
>
> 1. **Vector store is now embedded SQLite, not Supabase Postgres.** Every knowledge / memory / mirror
>    store is a local **`sqlite-vec`** `.db` file you can copy or read directly — no server. Tools take
>    `{ db_file, table }` instead of a pgvector `function_name`; the primary tool type is renamed
>    `Supabase` → **`SqliteVector`**, backed by a new `SqliteVectorStore` (reusing `Embedding`) (§6, §8.3).
> 2. **Graph store is now embedded & file-based, not Neo4j.** The optional `graph_db` mirror defaults to
>    **Kuzu** — "the SQLite of graph databases": Cypher over a single local `path`, no server — with a
>    zero-dependency **SQLite nodes/edges** fallback (`type: "sqlite"`, traversed by recursive CTEs).
>    Both knowledge-graph mirrors are now plain local files (§8.3).
> 3. **Tools carry their own `models` ladder.** A tool also drives an LLM (plan the call, read / rank
>    results, write artifacts), so each tool entry may pin its **own `models`** — typically a leaner
>    local model tuned for tool-calling — and **inherits the agent's `models`** when omitted (§6).

> **Revision 2026-08-02 — what changed & why (this pass):**
>
> 1. **The worklog is segmented, not one big file.** The single `raw_worklog.jsonl` becomes an
>    append-only **segment set** under `worklog/` (sharded by iteration, optional size cap). _Why:_ a
>    run no longer grows one unbounded file, and the index can **jump straight to a segment file +
>    iteration + line**, so old work is reachable in O(1) instead of by scanning (§8.1).
> 2. **The `cognitive_index` addresses blocks by `{segment, iteration, line, offset}`** (not just
>    `block_id`), so the agent can request the log **by file name, iteration number, or line**.
> 3. **A metadata agent builds a `knowledge_graph`.** On each flush a background indexer distills the
>    block into `{entities, keywords, 25-word summary, workflow, relationships}` and appends it to
>    `knowledge_graph.jsonl` — retrieval by meaning + structure, not just text (§8.2).
> 4. **Optional graph + vector database backends.** The `knowledge_graph` can be mirrored to a **graph
>    DB** (nodes / edges, queryable via GraphQL / Cypher) and/or a **vector DB**, so old worklogs are
>    retrieved **dynamically**, not only by reading files. Both default **off** (file-only) (§8.3).
> 5. **`working_folders`.** A list of external directories (e.g. source code) the agent may
>    **read / search** side by side with the worklog — separate from, and never mutated like, the log.
> 6. **`parallel_supprocess` (default 1).** One knob controls whether subprocess fan-out — delegates,
>    tool calls, per-block metadata, DB upserts — runs **sequentially (1)** or in a **bounded parallel
>    pool (>1)**.

> **Revision 2026-08-01 — what changed & why (improvements applied this pass):**
>
> 1. **The worklog is now JSON, not text.** `raw_worklog.log` → **`raw_worklog.jsonl`** (append-only
>    **JSON Lines**): each finished block is one self-contained JSON record on its own line. _Why:_
>    typed and structured, no fragile custom-delimiter parsing, still strictly append-only, still
>    greppable, and it drops straight into SQLite FTS5. (JSON Lines — not one big `.json` array —
>    because you can append a line without rewriting the whole file.)
> 2. **Blocks are addressed by a stable `block_id`, not by line ranges.** `cognitive_index` now joins
>    to the worklog by `block_id` instead of `[start_line, end_line]`. _Why:_ line ranges broke the
>    moment anything was reformatted or compacted; a `block_id` join never shifts, and an optional
>    `block_id → byte-offset` map gives **O(1)** block fetch.
> 3. **One clear storage split.** Shared team memory is **structured JSON** (`*.jsonl` — durable,
>    addressable); per-agent working windows stay **plain-text scratch** (`*.log` — streamed,
>    disposable). See §8.
> 4. **Typo fixed:** `max_retries_untill_switching_models` → **`max_retries_until_switching_models`**
>    (also updated in `example.json`).
> 5. **Clarity:** added an iteration-loop diagram (§3), tightened dense tables, and made file /
>    terminology naming consistent throughout.

---

## 1. Vision & Design Philosophy

- **One recursive class.** Everything is a `ProgressiveAgentSLM`. A "team" is simply an agent whose
  `delegates` are other agents — composition _is_ recursion; there is no separate orchestrator type.
  Each agent carries its own `agent_id` + `description`, and the `description` alone is the signal a
  parent reads to decide when to hand it a sub-question.
- **Progressive cognition by indexing, not stuffing.** Each iteration the model's context is
  partitioned into four proportional tiers (§3) — fractions of whatever model is active. Instead of
  piling everything into the prompt, the agent appends its work to an **append-only, segmented
  worklog** (`worklog/seg-*.jsonl`) and builds a **`cognitive_index`** — a compact map of ~10–20-token
  pointers into that log. To think, it looks up the index and pulls only the relevant blocks back into
  a bounded working set (`context_window.log`). On small models, quality comes from disciplined memory
  handling — not a bigger model.
- **Local & SLM-first, cloud optional.** `models` is a priority **ladder** (highest → lowest). Local
  Ollama models do the frequent work; a cloud model (OpenRouter) sits lower as an automatic fallback,
  or is promoted to the top for hard steps. Each model gets one bounded retry budget —
  `max_retries_until_switching_models` — that counts **both** quality (self-eval) **and** infra
  (timeout / HTTP) failures before the agent **switches to the next model** on the ladder (§4).
- **Behavior by policy, not by code.** `cognitive_behavior` is a list of `when → then` rules rendered
  into the system prompt every iteration — it both steers how a small model thinks (deep-think,
  double-check, visualize, say-no) and acts as the run's **todo checklist**. Policies are declarative
  only (no per-policy models); a non-programmer can shape behavior without touching Python.
- **One append-only worklog, shared by the whole team.** Every agent and delegate appends finished
  blocks to the same **segmented worklog** (the single source of truth) through one serialized writer,
  and maps them in `cognitive_index`. Delegates deliver their final answer to the parent when done,
  but their work stays in the shared log so any later agent can **loop back** over it via the index.
- **Route by description, guide tools by `when`.** A parent routes a sub-question to a delegate purely
  by reading each delegate's `description` — no separate gate to maintain. Tools still carry a `when`
  guidance string injected next to the tool, so a small model calls it at the right moment (and so the
  menu can be pruned, §7).
- **Reuse, don't rebuild.** Async streaming generators that `yield` chunks, DI via constructor
  kwargs, `Task`-subclass agents, prompt-based JSON with robust regex fallbacks, JSON-file
  config / state. New code lives under `src/framework/`; existing files are touched minimally.

---

## 2. The `ProgressiveAgentSLM` Object

A single class configured by one object (JSON or Python). Every field has a sensible default; only
`agent_id`, `description`, and — on the root agent — at least one `model` are required.

| Field                                | Type        | Meaning                                                                                                                                                                                                                                                                                                              |
| ------------------------------------ | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`                           | str         | Stable identifier. A parent addresses this agent as `delegate:<agent_id>`, and it labels the agent's blocks in the shared worklog.                                                                                                                                                                                   |
| `description`                        | str         | One-line capability summary. The **sole** signal a parent reads to decide whether to delegate here — no separate gate.                                                                                                                                                                                               |
| `system_prompt`                      | str \| null | The agent's base persona / instructions, rendered at the top of the `cognitive_reflection_behavior` tier (§3). Optional; when omitted, a default is built from `description` + `cognitive_behavior`. Per-agent (not inherited).                                                                                      |
| `worklog_folder`                     | str         | Directory for the run's worklog subsystem (§8). Delegates **share** the parent's `worklog_folder` — one shared log per run.                                                                                                                                                                                          |
| `working_folders`                    | list        | External directories the agent may **read / search** side by side with the log (e.g. source code), each `{ path, description }`. Read-only; never mutated (writes stay in the worklog). Inherited by delegates.                                                                                                      |
| `parallel_supprocess`                | int         | Max concurrent subprocesses for parallelizable work — delegate fan-out, tool calls, per-block metadata, DB upserts. **1** = strictly sequential (default); **>1** = bounded parallel pool. Inherited by delegates.                                                                                                   |
| `knowledge_graph`                    | object      | Config for the metadata / knowledge-graph subsystem (§8): the indexer model, the `knowledge_graph.jsonl` sink, and optional `graph_db` / `vector_db` mirrors. Inherited by delegates.                                                                                                                                |
| `context_window_breakdown`           | object      | The four-tier budget, expressed as **fractions** of the active model's `max_tokens` (§3) — the heart of the design. Real token counts are inferred per model.                                                                                                                                                        |
| `max_retries_until_switching_models` | int         | Per-model **failover** budget only — counts consecutive quality (self-eval) **and** infra (timeout / HTTP) failures on the _current_ model. Default **5**. When spent, **switch to the next model**; it does **not** cap total work (§4).                                                                            |
| `max_iterations`                     | int         | Separate **total-work** budget: max progressive iterations for this agent (parent default **200**, delegate default **50**). Batched / programmatic tool turns are **refunded** so they don't burn it; bounds a deep delegate tree independently of the ladder (§4). Inherited (delegates default to a smaller cap). |
| `models`                             | list        | Priority **ladder** (§4), highest first. Each model carries its own `max_retries_until_switching_models`; a successful iteration resets the ladder to the top model.                                                                                                                                                 |
| `cognitive_behavior`                 | list        | `when → then` behavioral policies (§5) rendered into the system prompt each iteration; also the run's todo checklist. Declarative only — no per-policy models.                                                                                                                                                       |
| `tools`                              | list        | Capabilities the agent may call, each with a `when` guidance string and an **optional own `models`** ladder (§6): SQLite vector, todo, write-file, search-file, vector-memory, skills, …                                                                                                                             |
| `delegates`                          | list        | Nested `ProgressiveAgentSLM` configs (§7). The parent routes sub-questions to them by reading each one's `agent_id` / `description`.                                                                                                                                                                                 |

> **Inheritance.** A delegate that omits `models`, `max_retries_until_switching_models`, or
> `max_iterations` **inherits the parent's** (though `max_iterations` defaults to a smaller delegate
> cap), and likewise inherits `working_folders`, `parallel_supprocess`, and `knowledge_graph`.
> It shares the parent's `worklog_folder` (hence the shared segmented worklog + `cognitive_index` +
> `knowledge_graph.jsonl`) while keeping its **own** `context_window.log` + `response_window.log`.
> `context_window_breakdown`, `system_prompt`, `cognitive_behavior`, and `tools` are per-agent (not
> inherited), so each delegate is independently budgeted and specialized.

> **Working folders.** `working_folders` are the directories the agent _works on_ — typically source
> code — kept **separate** from the `worklog_folder` where it _records_ its thinking. `ReadFileTool` /
> `SearchFileTool` may resolve paths under any `working_folders` root **and** the worklog;
> `WriteFileTool` stays sandboxed to the worklog, so source is never mutated. Each entry's
> `description` tells the agent what lives in that folder. Every access is confined to a configured
> root with traversal / absolute-escape rejection (OWASP A01/A03).

> **Parallelism.** `parallel_supprocess` (default **1**) is the one concurrency knob: `1` runs every
> subprocess step — delegate fan-out, independent tool calls, per-block metadata generation, DB
> upserts — **sequentially**; `>1` runs them in a **bounded parallel pool** of that size. Because it is
> inherited, it bounds fan-out at every level, so a deep delegate tree can't explode into unbounded
> concurrency.

---

## 3. `context_window_breakdown` — the four-tier proportional budget

The budget is expressed as **fractions of the active model's `max_tokens`**, not absolute token
counts — so the same config runs unchanged on models with different context sizes, and each tier's
real allowance is inferred at runtime as `fraction × max_tokens`. Only **three** tiers are declared;
the **remainder is reserved for the answer**. Rather than stuffing accumulated history into the
prompt, the agent keeps the full record in the append-only **segmented worklog** (`worklog/seg-*.jsonl`)
and a `cognitive_index` map over it; the tiers below bound what actually enters the prompt each step.
Each tier draws from a **memory layer** (§8): the stable prefix is **L4** (behavior), the situational
tier is **L3**, and the working attention pulls in **L2** (facts, by search tool) and **L1** (raw, by
pointer seek) on demand — promotion up the layers is promotion toward the prompt.

| Tier                             | Default | Holds                                                                                                                                                                                                                          | Budget / compaction rule                                                                                                                                                                          |
| -------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_history_awareness` | 0.025   | The **L3 situational digest** (§8): a compact "what I know so far vs. the goal" distilled from L2, plus a brief recap of recent turns — just enough to stay coherent (the full record lives in L1 / L2). Always in the prompt. | Set **0** for a stateless / one-shot agent; the freed budget is **donated to the next tier** so the agent "thinks harder". Raise it when situational awareness matters more than raw working set. |
| `cognitive_reflection_behavior`  | 0.325   | The cognition workspace: `system_prompt` + `cognitive_behavior` policies, tool + delegate descriptions and usage notes, and the internal reasoning / reflection trace used to pick the next step or switch models.             | Hosts `cognitive_index` retrieval + reflection; when it and `current_working_attention` exceed budget, a progressive reflection compacts both **adaptively** (only enough to fit).                |
| `current_working_attention`      | 0.525   | The working set for this run: the current user question plus everything retrieved from tools, delegates, and the past worklog (blocks pulled from the segmented `worklog/` via the index).                                     | Compacted **adaptively** when over budget (stale blocks dropped — still recoverable from the segments).                                                                                           |
| _(remainder ≈ 0.125)_            | —       | The answer the agent emits this iteration (backed by `response_window.log`, §8).                                                                                                                                               | Hard output cap = `max_tokens − Σ(declared tiers)`. Flushed to the segmented `worklog/` + indexed, then **cleared** for the next iteration.                                                       |
| _(unbounded)_                    | —       | The segmented `worklog/seg-*.jsonl` — every finished block from every agent / delegate, the **single source of truth**.                                                                                                        | **Append-only, never rewritten.** No budget; this is what makes the adaptive compactions above safe (nothing is truly lost).                                                                      |

> The three declared fractions default to **0.025 / 0.325 / 0.525 = 0.875**, leaving **≈ 0.125** to
> answer. They must sum to **< 1**; the loader rejects a breakdown that leaves no room for the answer
> (§12 Phase 3). For `gpt-oss:20b` (`max_tokens: 62000`) they resolve to ≈ **1,550 / 20,150 / 32,550**
> tokens, with **≈ 7,750** left for the answer; swap in a bigger-context model and every tier scales up
> automatically.

**How one iteration works:**

```mermaid
flowchart LR
    Q["User / parent<br/>sub-question"] --> R["Retrieve<br/>cognitive_index.search →<br/>worklog.fetch(segment, line)"]
    R --> A["Assemble 4-tier prompt<br/>(fractions of active model max_tokens)"]
    A --> M{"Act"}
    M -->|tool| T["Tool call"]
    M -->|delegate| D["Route by description"]
    M -->|answer| W["Write response_window"]
    T --> W
    D --> W
    W --> F["Flush block →<br/>worklog/seg + cognitive_index + knowledge_graph"]
    F --> E{"Good enough?<br/>quick self-eval"}
    E -->|"yes"| DONE["Return answer"]
    E -->|"no, budget left"| R
    E -->|"failed × budget"| S["Switch to next model ↓ ladder"]
    S --> R
```

**Prompt assembly per step — a _stable prefix_ + a _volatile suffix_ (prompt-cache-safe):**

The tiers are ordered so everything **constant for the run** sits in a **byte-stable prefix** the
model's KV cache (Ollama / llama.cpp prefill) or a cloud provider's prompt cache can reuse every
iteration; only the retrieved working set and the answer change per step. Rebuilding the prefix mid-run
forces a full re-prefill — the dominant latency cost on a 20B model over a 62k window — so the prefix is
held **byte-identical until a compaction genuinely forces a rebuild**, the single sanctioned
cache-invalidation event.

```
── stable prefix (constant per run → cached, never rebuilt except on compaction) ───────────
[ system_prompt + cognitive_behavior(when→then) + tool/delegate descriptions        ⊂ f_cog  × max_tokens ]
── volatile suffix (changes each iteration) ────────────────────────────────────────────────
[ conversation_history_awareness:  brief rolling summary of recent turns            ≤ f_conv × max_tokens ]
[ cognitive_reflection_behavior:   this-step reasoning / reflection trace + todo    (remainder of f_cog)  ]
[ current_working_attention:       question + retrieved blocks (via cognitive_index) ≤ f_work × max_tokens ]
→ answer:                          the response for this iteration                  ≤ (1 − Σf) × max_tokens
```

**Core loop invariant — index & retrieve, then compact:**

```
per block b produced (delegate answer / tool result / iteration answer):
    loc ← worklog.append(b)                           # append to the current segment; returns {block_id, segment, iteration, line, offset}
    cognitive_index.append(pointer(loc, b))           # {block_id, segment, iteration, line, offset, summary≈10-20 tok, keywords, tokens}
    metadata_agent.enqueue(b, loc)                    # off critical path (parallel_supprocess): entities/keywords/25-word summary/workflow/relationships → knowledge_graph.jsonl (+ optional graph/vector DB)

per iteration:
    ids     ← cognitive_index.search(question)        # by keyword/summary now; via graph/vector DB when enabled
    working ← worklog.fetch(ids)                      # jump by {segment, iteration, line, offset} ⇒ O(1)
    if size(working) + size(cognitive_reflection) > budget:
        reflect_and_compact(target = fit_under(budget))   # adaptive: shrink only enough to fit; protect head+tail; update the prior summary (iterative, goal-tracking); drop/merge pointers — blocks stay in the segments (recoverable)
    response_window ← respond(prompt)                 # ≤ (1 − Σf) × max_tokens
    if final and not verify_on_stop(response_window):     # enforced double_check: evidence must cover the question
        continue                                          # inject one more round while max_iterations remains
    flush(response_window → worklog + cognitive_index + metadata_agent); clear(response_window)
```

Every tier is a slice of the **selected** model's `max_tokens`, so the assembled request can **never**
exceed that model's context — no separate size-inference step is needed (§4). Because the segmented
`worklog/seg-*.jsonl` is immutable and `cognitive_index` is a pure **index** (not a compressed blob)
that addresses blocks by `{segment, iteration, line, offset}`, compaction only ever touches the
derived views — the agent can shrink its working memory aggressively and still recover any detail by
seeking one pointer back into the raw segments.

---

## 4. Models — per-agent priority ladder

`models` is an ordered list, highest priority first. Each entry:

| Key          | Required | Meaning                                                                                                                                                                      |
| ------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `platform`   | yes      | `ollama` (local) or `open_router` (cloud). Maps to the existing `Ollama` / `OpenRouter` clients.                                                                             |
| `name`       | yes      | Model name on that platform.                                                                                                                                                 |
| `url`        | no       | Platform endpoint (e.g. `http://localhost:11434` for Ollama, `https://openrouter.ai/api/v1` for OpenRouter). Defaults to the platform's env default.                         |
| `max_tokens` | no       | Context ceiling. A number sets it; `"auto"` (or omitted) uses the platform's advertised context. Every `context_window_breakdown` fraction is taken against this value (§3). |

**Selection & the ladder.** Walk the list top-down; the active model is the first **reachable** one.
Because the budget is proportional to whatever model is chosen (§3), any model fits — there is no
minimum-size gate. The list is a **ladder** with **one** per-model budget:

- **Retry budget — `max_retries_until_switching_models` (default 5).** A single counter per model
  covering **both** failure kinds: a "not good enough" verdict from the per-iteration quick
  self-evaluation (a _quality_ failure) **and** a timeout / HTTP / unreachable error (an _infra_
  failure). When the current model's counter reaches the budget, the agent **switches to the next
  model** on the ladder and resets the counter to 0.
- **Success resets the ladder.** When a model handles an iteration successfully, the ladder pointer
  resets to the **top** model for the next iteration (the cheapest capable model is always tried
  first).
- **Stopping — two independent limits.** A run ends when **either** the model ladder is **exhausted**
  (the last model spends its `max_retries_until_switching_models`) **or** the agent's separate
  **`max_iterations`** total-work budget is hit (§2). Keeping _failover_ and _total work_ apart means a
  run that is making progress but keeps failing self-eval on one model doesn't prematurely burn the
  ladder, and a run that never fails still can't spin forever. Batched / programmatic tool turns are
  **refunded** against `max_iterations`.
- **Bounded I/O.** Every model call bounds its read with a **byte cap and a wall-clock deadline** (a
  stalled local endpoint must not hang the run); a deadline hit counts as one infra failure.

This is the per-agent generalization of a role-based registry — local-first with cloud as an automatic
backstop, or cloud promoted to the top for hard steps.

```json
"models": [
  { "platform": "ollama",      "name": "gpt-oss:20b",                 "url": "http://localhost:11434",       "max_tokens": 62000 },
  { "platform": "open_router", "name": "anthropic/claude-3.5-sonnet", "url": "https://openrouter.ai/api/v1", "max_tokens": "auto" }
]
```

---

## 5. `cognitive_behavior` — `when → then` behavioral policies

`cognitive_behavior` is a list of rules that shape the agent's behavior. Each rule renders into the
system prompt **every iteration** as "**When** _condition_, **then** _action_." This does two jobs at
once: it steers how a small model thinks, and it acts as the run's **todo checklist** the model
re-reads each pass to stay on task. The rendered rules live in the `cognitive_reflection_behavior`
tier (§3). Policies are **declarative only** — they carry no per-policy `models`; model choice is
governed globally by the ladder (§4), so authoring stays simple and one policy can't fragment the
model routing.

| Key    | Meaning                                                                                        |
| ------ | ---------------------------------------------------------------------------------------------- |
| `id`   | Short label for the policy (e.g. `deep_think`, `double_check`, `visualize_diagram`, `say_no`). |
| `when` | The condition / trigger, in plain language.                                                    |
| `then` | The action the agent should take when the condition holds.                                     |

**Recommended baseline policies:** **deep_think** (decompose complex questions before answering),
**double_check** (verify the gathered evidence actually answers the question; re-iterate if gaps
remain), **visualize_diagram** (emit a diagram when structure / relationships matter), **say_no**
(answer honestly when the KB has no answer rather than hallucinate).

> **Enforced, not just prompted.** Small models routinely _ignore_ prompt-only guidance, so the
> **critical** policies are declarative on the surface **and backed by a deterministic turn-end guard**
> in the loop (they stay authorable as `when → then`, but do not depend on the SLM choosing to obey):
>
> - **`double_check` → verify-on-stop.** When the agent tries to emit a final answer, a guard checks
>   (via `AnswerEvaluator`) that the gathered evidence actually covers the question; if not — and
>   `max_iterations` remains — it injects **one** more bounded retrieval round instead of returning.
> - **`say_no` → grounding gate.** If retrieval returned nothing above a similarity floor, the guard
>   forces the honest-refusal branch rather than trusting the model to pick it.
> - **anti-drift → tool-loop guard.** Tools are classed idempotent-vs-mutating; a repeated identical
>   call is detected and warned / short-circuited so an SLM can't spin on one tool.
>
> Non-critical policies (e.g. `visualize_diagram`) stay prompt-only. Guards are pure decisions; the
> loop owns whether a decision becomes a nudge, a synthetic result, or a halt.

---

## 6. Tools — capabilities with `when` guidance

Each tool entry tells the agent **what** the tool is and **when** to use it. The `when` string is
injected next to the tool in the prompt so a small model calls it at the right moment.

**SqliteVector (primary tool).** Vector search over an **embedded SQLite** store (the `sqlite-vec`
extension) — a single local `.db` file you can copy or read directly, no server. The most useful
capability for these RAG agents.

| Key       | Meaning                                                                                                    |
| --------- | ---------------------------------------------------------------------------------------------------------- |
| `type`    | `SqliteVector`.                                                                                            |
| `db_file` | Path to the local `.db` file holding the embedded vectors (e.g. `knowledge/bvms_docs.db`).                 |
| `table`   | The vector table to query inside that file (e.g. `bvms_documents`).                                        |
| `ranking` | If `true`, re-rank retrieved chunks with parallel `DocumentRanking` (reuse `RagAssistant.stream` batches). |
| `when`    | Guidance: when this knowledge source is the right one to query.                                            |

All other tools follow the same `{ type, when, … }` shape, and each `when` is used both to guide the
model and to **prune the menu** (§7): only tools whose `when` matches the current step are shown. The
SqliteVector wrapper is built on the async `SqliteVectorStore.async_query` (sqlite-vec + `Embedding`).

**Tools can pin their own `models` ladder.** A tool doesn't just execute code — it usually drives an
LLM (to plan the call, read / rank results, or write an artifact). So each tool entry may carry its
**own `models`** list (same shape as §4) — typically a **leaner local model tuned for tool-calling**
(e.g. `qwen3.5:9b`) rather than the agent's heavy main ladder. A tool that omits `models` **inherits
the agent's top-level `models`**; its `max_retries_until_switching_models` follows the same ladder
semantics (§4).

**Standard tool catalog** (industry-conventional shapes, reusing existing primitives):

| Tool                  | Shape (beyond `type` + `when`) | Behavior                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SqliteVector`        | `db_file`, `table`, `ranking`  | **Primary.** Embedded vector search via `SqliteVectorStore.async_query` (sqlite-vec, single `.db` file); optional parallel `DocumentRanking`. Read-only domain knowledge base.                                                                                                                                                                                                                                       |
| `ReadFileTool`        | —                              | Read a file's contents. Paths resolve under any `working_folders` root **or** the run's `worklog_folder`; `..` / absolute escapes rejected (OWASP A01/A03).                                                                                                                                                                                                                                                          |
| `SearchFileTool`      | `glob?`                        | Locate files by name / glob or find where a term / symbol appears (ripgrep-style) across the `working_folders` + `worklog_folder`; returns path + line + snippet. Read-only, traversal-safe.                                                                                                                                                                                                                         |
| `WriteFileTool`       | `require_approval?`            | Persist an artifact (notes, generated code, a report) **inside the `worklog_folder`** — `working_folders` (source) are read-only, never written. Path traversal / absolute escapes rejected (OWASP A01/A03). `require_approval: true` gates the write; default **false** → runs without prompting (home-lab). Reuses `FileHanlder`.                                                                                  |
| `TodoTool`            | —                              | Maintains the run's checklist (`todo.md` in the `worklog_folder`). The model **rewrites the whole list** (`[{id, content, status: pending\|in_progress\|completed}]`); the loop re-injects it each iteration (anti-drift).                                                                                                                                                                                           |
| `VectorMemoryTool`    | `db_file`, `table`             | The agent's **own, cross-run, writable** long-term memory (distinct from the read-only KB). `recall(query, k)` + `remember(text, tags?)`, backed by a local **SQLite** memory table (sqlite-vec) reusing `Embedding`. Naturally embeds `cognitive_index` summaries for semantic recall.                                                                                                                              |
| `KnowledgeSearchTool` | `db_file?`, `table?`           | **L2 search (prepared tool code).** Efficient search over the run's own distilled **fact store** (`knowledge/facts.db`, sqlite-vec + FTS, fed by the metadata agent §8.2) — vector + keyword + graph lookups over entities / facts / relationships. Distinct from `SqliteVector` (external domain KB): this queries what the agent has _learned this run_. Defaults to the run's L2 store when `db_file` is omitted. |
| `SkillTool`           | `skills_dir`                   | On-demand **procedure packs** (progressive disclosure): each skill file has `{ id, description, when }` frontmatter + a body of steps. Only id / description / when are always visible; the body loads when its `when` matches. **Trusted-local files only** (loading external skill text is a prompt-injection surface).                                                                                            |
| `GenerateDiagramTool` | —                              | Emits Mermaid for the `visualize_diagram` policy.                                                                                                                                                                                                                                                                                                                                                                    |
| `RunPythonTool`       | `require_approval?`            | Wraps `PythonCodeExecute`; `require_approval: true` gates execution; default **false** → runs without prompting. ⚠️ Autonomous execution — revisit before any non-local use.                                                                                                                                                                                                                                         |

---

## 7. Delegates — recursive composition

`delegates` is a list of **nested `ProgressiveAgentSLM` configs**. There is no separate "sub-agent"
type — a delegate is a full agent with its own `system_prompt`, `context_window_breakdown`, `tools`,
and optional `cognitive_behavior` / `models` / `delegates`. The parent:

1. **Routes by description.** For a sub-question the small model picks a delegate by reading each one's
   `description` — via the proven `_parse_agent_routing` JSON pattern, generalized to
   `delegate:<agent_id>`. Delegates are **not** gated by a separate `when`; a clear `description` is
   the whole contract (tools are still menu-pruned by their own `when`, §6). Fewer moving parts → more
   reliable SLM routing.
2. **Hands the sub-question down.** The delegate runs its **own** full progressive loop with its own
   `context_window.log` + `response_window.log`, but appends finished blocks to the **shared** segmented
   worklog + `cognitive_index` (one per run) under its own `agent_id`.
3. **Delivers when done.** Unlike the parent's live stream, a delegate returns only its **final**
   answer to the parent; the parent folds that block into its own working set (by index lookup) and
   continues. Because the delegate's full work remains in the shared log, any **later** agent or
   delegate can loop back over it via the index.

**Typed, isolated boundary.** A parent never hands a delegate a live agent object; it hands a
**frozen request** (`{ goal, context, role, allowed_toolsets?, blocked_tools? }`, with goal / context /
result **byte-capped**) and receives a **frozen result** (`{ state, summary, block_id }`). Each delegate
carries an explicit **state** (`pending → running → succeeded | failed | cancelled`), a `depth`, and a
**restricted toolset** (a delegate need not — and usually should not — expose every parent tool). This
immutable contract is what makes fan-out under `parallel_supprocess` and cancellation safe.

Depth is bounded by an overall recursion cap; per-agent work is bounded by each delegate's own
**`max_iterations`** (default 50, smaller than the parent's) and the model ladder. Two RAG-backed
delegates (`bvms-general-knowledge`, `bvms-code-knowledge`), each owning an embedded SQLite vector
store, is the canonical example (§13).

---

## 8. The Worklog — a four-layer memory (L1 → L4)

The worklog lives in the run's `worklog_folder` (`<worklog_folder>/<run_id>/`) and is organized as a
**four-layer memory hierarchy** — raw at the bottom, refined at the top. Each layer is _derived_ from
the one below by a background step, and each is progressively **hotter** (closer to the live prompt)
and smaller:

| Layer                | Holds                                                                                    | Storage                                                                                               | Reaches the model by                                     | Derived by                        |
| -------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | --------------------------------- |
| **L1 — raw**         | Every iteration's raw output + tool-call results, verbatim                               | `worklog/seg-*.jsonl` (append-only segments) + per-agent `context_window.log` / `response_window.log` | explicit `{segment, offset}` **seek**                    | — (single source of truth)        |
| **L2 — facts**       | Compressed / reflected high-quality facts, entities, relationships from L1               | `knowledge_graph.jsonl` (log) **+ `knowledge/facts.db`** (sqlite-vec + FTS)                           | on demand, via **`KnowledgeSearchTool`** (§6)            | **metadata agent** (§8.2)         |
| **L3 — situational** | "What I know so far vs. the goal" digest + the retrieval index over L1 / L2              | `situational.md` (digest) + `cognitive_index.jsonl` (index)                                           | **always in the prompt** (situational tier, §3)          | **situational summarizer** (§8.2) |
| **L4 — behavior**    | System prompt, `cognitive_behavior` policies / disciplines, tool / delegate descriptions | the agent config (`AgentConfig`)                                                                      | **always in the prompt** (byte-stable cached prefix, §3) | authored / config (static)        |

> Two orthogonal taxonomies compose here: **these four _memory layers_ decide where knowledge lives and
> how it is refined; the four _context tiers_ (§3) decide how much of each layer enters the prompt each
> step.** The mapping is direct — **L4 = stable cached prefix; L3 = the always-in-prompt situational
> tier; L2 = pulled in on demand by search tool; L1 = pulled in by pointer seek.** Direction note: unlike
> CPU caches, **L1 is the coldest / rawest / largest and L4 the hottest / most-refined / smallest**
> (ascending abstraction).

The three artifact groups below still hold; they are just now named by layer. It rests on **one clear
split**, plus a **derived knowledge layer**:

- **L1 — shared raw source of truth = structured JSON.** An append-only, **segmented** raw worklog
  (`worklog/seg-*.jsonl`) + a `cognitive_index.jsonl` pointer map (the L3 index) — durable, addressable,
  the single source of truth for the run.
- **L1 — per-agent working windows = plain-text scratch** (`context_window.log` + `response_window.log`) —
  streamed to as the agent thinks, then discarded / compacted.
- **L2 — derived facts = a metadata knowledge graph + fact store** (`knowledge_graph.jsonl` **+**
  `knowledge/facts.db`, sqlite-vec + FTS; optionally mirrored to an embedded Kuzu graph) — built by a
  background metadata agent from every flushed block, and distilled once more into the **L3**
  `situational.md` digest.

The tiers in §3 are the _prompt-side_ budget; these files are the _on-disk_ storage it draws from.

### 8.1 Segmented raw worklog — no more single big file

Instead of one unbounded `raw_worklog.jsonl`, finished blocks are appended to **rolling segment
files** under `worklog/`: one segment **per iteration** by default (`seg-<iter>.jsonl`), rolled to a
fresh segment whenever it crosses an optional size cap (`worklog.max_segment_lines`, default 2000).
Each block is still one self-contained JSON line keyed by a stable `block_id`; segmentation only
changes _where_ the line lives, never the append-only guarantee.

_Why segment:_ a long run no longer grows one giant file, and the index can **jump straight to a
segment file + iteration + line**, so any past block is one seek away instead of a full scan.

| File / dir              | Scope     | Format | Role                                                                                                                                                             |
| ----------------------- | --------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `worklog/seg-*.jsonl`   | shared    | JSONL  | **Append-only, never rewritten.** Rolling segments of finished blocks (one JSON record per line, keyed by `block_id`). The single source of truth.               |
| `cognitive_index.jsonl` | shared    | JSONL  | One **pointer per block** → `{ block_id, segment, iteration, line, offset, summary, keywords }`. The map used to jump to and pull back only the relevant blocks. |
| `knowledge_graph.jsonl` | shared    | JSONL  | One **metadata record per block** (entities, keywords, 25-word summary, workflow, relationships) from the metadata agent (§8.2). Feeds the optional DBs (§8.3).  |
| `context_window.log`    | per-agent | text   | The agent's current working set; compacted adaptively when it exceeds the `current_working_attention` budget.                                                    |
| `response_window.log`   | per-agent | text   | The agent's **latest** answer only; flushed to the worklog + index + metadata agent, then **cleared** each iteration.                                            |
| `todo.md`               | shared    | text   | `TodoTool` checklist, re-injected each iteration.                                                                                                                |
| `index.db` _(optional)_ | shared    | SQLite | FTS5 over the segments + `cognitive_index.jsonl` for `LogSearch`.                                                                                                |

**A "block"** is one unit of finished work — a delegate's answer, a tool result, or an iteration's
answer. Blocks are **flushed at completion** (not token-by-token) through one **serialized writer**,
so `block_id`s stay unique and parallel delegates never interleave.

**Segment block record** (one JSON line — the verbatim source of truth):

```json
{
  "block_id": "run7-bvms-code-knowledge-iter3-002",
  "ts": "2026-08-02T12:34:56Z",
  "agent_id": "bvms-code-knowledge",
  "iteration": 3,
  "phase": "delegate",
  "actor": "tool:SqliteVector",
  "content": "…the full verbatim block text…",
  "tokens": 512
}
```

**Index pointer record** — now carries the block's physical location, so the agent can jump **by file
name, iteration, or line**:

```json
{
  "block_id": "run7-bvms-code-knowledge-iter3-002",
  "segment": "worklog/seg-003.jsonl",
  "iteration": 3,
  "line": 2,
  "offset": 5342,
  "agent_id": "bvms-code-knowledge",
  "phase": "delegate",
  "summary": "≈10–20-token gist",
  "keywords": ["voyage", "approval", "saga"],
  "tokens": 512
}
```

**Write path, per block.** The agent streams into its own `context_window.log` / `response_window.log`;
on completion it enqueues the block to the run's single writer, which (1) appends it to the current
`worklog/seg-*.jsonl` and returns `{ block_id, segment, iteration, line, offset }`, (2) appends one
pointer to `cognitive_index.jsonl`, and (3) hands the block to the **metadata agent** (§8.2). Then
`response_window.log` is cleared.

**Read path (index-and-retrieve).** To assemble its next prompt an agent does **not** replay the log;
it searches `cognitive_index` (keyword / summary now; graph or vector DB later, §8.3), takes the
matching pointers, and **seeks** just those blocks by `{ segment, offset }` into `context_window.log`.
This is RAG over the team's own worklog — the trick that keeps SLM prompts small.

**Progressive reflection (compaction).** When `context_window.log` + `cognitive_index` exceed their
budgets, a reflection compacts **both adaptively** (only enough to fit; merge / drop pointers, release
stale blocks — protecting head + tail). Nothing is lost — the segments are immutable, so any dropped
detail is one `{ segment, offset }` seek away.

**Delegate coordination.** A delegate returns just its **final** answer to its parent, but its full
work lands in the shared segments under its `agent_id`, so any later teammate can loop back over it via
the index.

### 8.2 Metadata agent → `knowledge_graph.jsonl`

A lightweight **metadata agent** — the **L1 → L2 promoter** — turns each flushed block into one
structured knowledge record and appends it to `knowledge_graph.jsonl` (and upserts it into the L2 fact
store `knowledge/facts.db`, §8.3):

| Field           | Meaning                                                                                       | Built by                                         |
| --------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `entities`      | Named things in the block — services, tables, APIs, domain terms.                             | `SimpleEntityExtractor` (LLM fallback when hard) |
| `keywords`      | Salient search terms.                                                                         | `KeywordExtractor`                               |
| `summary`       | A **≤25-word** gist of the block.                                                             | ladder model (cheap)                             |
| `workflow`      | The process / steps the block describes, if any.                                              | ladder model                                     |
| `relationships` | Directed edges between entities (`{ from, type, to }`, e.g. `VoyageService —calls→ FuelSvc`). | ladder model                                     |

```json
{
  "block_id": "run7-bvms-code-knowledge-iter3-002",
  "segment": "worklog/seg-003.jsonl",
  "iteration": 3,
  "entities": ["VoyageService", "FuelOptimizationService", "Voyage"],
  "keywords": ["voyage", "approval", "saga"],
  "summary": "VoyageService coordinates approval across services with a saga; fuel optimization runs before commit.",
  "workflow": "Create Voyage → validate → optimize fuel → approve → emit VoyageApproved",
  "relationships": [
    {
      "from": "VoyageService",
      "type": "calls",
      "to": "FuelOptimizationService"
    },
    { "from": "VoyageService", "type": "writes", "to": "Voyage" }
  ]
}
```

The metadata agent runs **off the critical path**: blocks are enqueued and processed sequentially or
in a bounded pool per `parallel_supprocess` (§2). Its records are what the `cognitive_index` and the
optional DBs (§8.3) grow richer from — semantic recall over the run's own history.

> **Cheap-first, curated, and egress-safe.**
>
> - **Cheap first.** `entities` / `keywords` / `relationships` are seeded by the deterministic
>   extractors (`KeywordExtractor` / `SimpleEntityExtractor`) and lexical overlap **before** any LLM
>   call; the ladder model is invoked only for the `summary` / `workflow`, or when extraction is weak.
> - **Redact on egress.** A block's text may cross to a _different_ model (the metadata / ladder model,
>   a delegate, a cloud escalation, or an optional DB), so secrets / PII are **redacted at that
>   boundary** before the text leaves the agent.
> - **Curate, never delete.** A background curator may mark `knowledge_graph` records / mirrored nodes
>   `stale` or `archived` (recoverable) and consolidate duplicates — it **never hard-deletes**, so the
>   segments remain the immutable source of truth.

> **From L2 to L3 — the situational digest.** After the metadata agent updates L2, a lightweight
> **situational summarizer** (reuse `IterationSummarizer` / `KnowledgeCompression`) refreshes the run's
> **L3 digest** (`situational.md`): a compact, goal-relative "state of knowledge so far" that is injected
> into the situational tier of every prompt (§3). It is regenerated **only when L2 changes materially**
> (a cheap-model, threshold-triggered step), so the always-in-prompt layer stays current without paying
> a summary cost every iteration. The fact store `knowledge/facts.db` (sqlite-vec + FTS) is the
> queryable form of L2, searched by `KnowledgeSearchTool` (§6).

### 8.3 The L2 fact store + optional cross-run mirrors — embedded & file-based

The **L2 fact store** (`knowledge/facts.db`, sqlite-vec + FTS) is **on by default**: the metadata agent
upserts every distilled record into it so `KnowledgeSearchTool` (§6) can search the run's own facts in
one seek — no server, a single local `.db` you can copy or read directly. For _cross-run_ recall (loop
back over an **earlier** run's knowledge), the `knowledge_graph` config (§2) can additionally mirror each
record into these **embedded, file-based** backends (still no server):

| Backend       | Config (`knowledge_graph.*`)                   | What it enables                                                                                                                                                                                                                                                                                                                                  |
| ------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Graph DB**  | `graph_db: { enabled, type, path }`            | Entities → nodes, `relationships` → edges in an **embedded Kuzu** database (the "SQLite of graph databases") at a single local `path`, queried with **Cypher** (e.g. "what calls `FuelOptimizationService`?"). Set `type: "sqlite"` to keep nodes/edges as tables in one `.db` file traversed by recursive CTEs instead (zero extra dependency). |
| **Vector DB** | `vector_db: { enabled, type, db_file, table }` | Embeds each summary + entities into a local **SQLite** vector store (`sqlite-vec`, single `db_file`). **Semantic** recall over past worklogs via the same `SqliteVectorStore`.                                                                                                                                                                   |

The **L2 fact store (vector) is default-on**; the **graph mirror and cross-run reuse default off**. All
live in a **file you can copy / read directly** — no service. When a mirror is on,
`cognitive_index.search()` can resolve a query against the graph or vector DB **dynamically** instead of
only reading files — so a later run can loop back over an earlier run's knowledge without re-reading it.
Mirror upserts run under `parallel_supprocess`, like the metadata step.

```
<worklog_folder>/<run_id>/           # e.g. wip/bvms-assistant/<run_id>/
  worklog/
    seg-001.jsonl                    # ← L1: append-only raw segments (rolled per iteration / size cap)
    seg-002.jsonl
  knowledge/
    facts.db                         # ← L2: fact store (sqlite-vec + FTS) — distilled facts, searched by KnowledgeSearchTool
  cognitive_index.jsonl              # ← L3: pointer/index map → {block_id, segment, iteration, line, offset, summary, keywords}
  knowledge_graph.jsonl              # ← L2: metadata agent output: entities, keywords, 25-word summary, workflow, relationships
  situational.md                     # ← L3: situational digest ("what I know so far") — injected into the prompt each step
  context_window.log                 # ← L1: per-agent working set (compacts adaptively over budget)
  response_window.log                # ← L1: per-agent latest answer (flushed, then cleared)
  todo.md                            # ← TodoTool checklist (re-injected each iteration)
# <worklog_folder>/index.db          # ← optional SQLite FTS5 over segments + cognitive_index (LogSearch)
# knowledge_graph.kuzu / .db         # ← optional cross-run mirrors of knowledge_graph.jsonl (Kuzu graph / SQLite vector, §8.3)
```

---

## 9. Goals → Components

| Goal (user)                                                                     | Realized by                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Single recursive class anyone can configure (one object)                        | `ProgressiveAgentSLM` + `AgentConfig` + `config/load.py`                                                                                                                                                                                                    |
| **Goal**: stay focused on the user-set goal                                     | `cognitive_behavior` policies + double-check / re-iterate loop (reuse `AnswerEvaluator`)                                                                                                                                                                    |
| **Knowledge**: text files + embedded SQLite vector DB + own long-term memory    | `SqliteVectorTool` (primary, sqlite-vec) + `FileKnowledgeTool` + `VectorMemoryTool` (writable, cross-run SQLite)                                                                                                                                            |
| **Tools**: KB, files, search, write, todo, memory, skills, diagrams, python     | `ToolRegistry` + `tools/` (`SqliteVectorTool`, `ReadFileTool`, `SearchFileTool`, `WriteFileTool`, `TodoTool`, `VectorMemoryTool`, `SkillTool`, `GenerateDiagramTool`, `RunPythonTool`)                                                                      |
| **Cognition**: index the worklog, retrieve only what's needed, compact safely   | `CognitiveIndex` (pointer map, `block_id`-keyed) + `Reflector` **adaptive** compaction (head+tail-protected, iterative summary; reuse `KnowledgeCompression` + `IterationSummarizer`)                                                                       |
| **Delegate**: route by description, break into sub-agents, collect results      | Recursive `delegates` + `Router` (`description`-routed `delegate:<agent_id>`) dispatch                                                                                                                                                                      |
| **Worklog**: segmented append-only source of truth + per-agent working windows  | `worklog/seg-*.jsonl` segments + `cognitive_index.jsonl` (pointer map: `{segment, iteration, line, offset}`) shared; `context_window` + `response_window` per-agent                                                                                         |
| **Knowledge graph**: distill each block into entities/keywords/summary/workflow | `MetadataAgent` → `knowledge_graph.jsonl` (reuse `KeywordExtractor` / `SimpleEntityExtractor` + ladder model); optional embedded Kuzu graph / SQLite vector mirrors                                                                                         |
| **Memory layers**: raw → facts → situational → behavior (L1 → L4)               | L1 `worklog/seg-*.jsonl` · L2 `MetadataAgent` → `knowledge_graph.jsonl` + `FactStore` (`knowledge/facts.db`, `KnowledgeSearchTool`) · L3 `SituationalSummary` → `situational.md` + `CognitiveIndex` · L4 `system_prompt` + `cognitive_behavior` + delegates |
| **Working folders**: read / search external source dirs beside the log          | `working_folders[]` (`{ path, description }`) resolved read-only by `ReadFileTool` / `SearchFileTool`                                                                                                                                                       |
| **Parallelism**: run subprocess fan-out sequentially or in a bounded pool       | `parallel_supprocess` (default 1) via a shared `ParallelExecutor`                                                                                                                                                                                           |
| Local/SLM-first with a model **ladder** (single per-model retry budget)         | `ModelChain` (ladder + `max_retries_until_switching_models`)                                                                                                                                                                                                |
| Per-step logging to terminal + files for full-text search                       | `RunLogger` (block / JSONL) + `LogSearch` (SQLite FTS5 over the worklog logs)                                                                                                                                                                               |
| Workflow configurable via JSON **and** Python                                   | `config/load.py` (`example.json` + `schema.json`) + `ProgressiveAgentSLM(...)`                                                                                                                                                                              |

---

## 10. Design Decisions

| Topic                | Decision                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Agent & control flow | **Recursive progressive loop** — each step assembles the four-tier prompt (fractions of the active model), applies `cognitive_behavior` policies, calls tools / routes to delegates, then folds context + answer into `cognitive_index`; iterate until the model ladder is exhausted.                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Delegation           | **Follow `AssistantOrchestra`** routing (`_parse_agent_routing`), generalized to `delegate:<agent_id>`; a parent routes by reading each delegate's `description`. Delegates inherit `models` + `max_retries_until_switching_models`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Models (defaults)    | **Per-agent ladder** (highest→lowest): first reachable model wins (the budget is proportional, so any model fits). Each model gets one `max_retries_until_switching_models` budget (default 5) covering **both** quality self-eval failures **and** infra errors; success resets the ladder to the top; the run ends when the ladder is exhausted **or** the separate `max_iterations` total-work budget is hit (failover and total-work budgets are kept **orthogonal**). **OpenRouter** cloud as automatic fallback or promoted to top; `max_tokens: "auto"` uses the platform context, and every tier is a fraction of it.                                                                                                  |
| Worklog & memory     | **Segmented `worklog_folder` subsystem.** Shared **append-only** raw segments (`worklog/seg-*.jsonl`, rolled per iteration / size cap) + `cognitive_index.jsonl` (pointer map keyed by `block_id`, addressing `{segment, iteration, line, offset}`); per-agent `context_window.log` + `response_window.log` (plain-text scratch). One serialized writer; **`cognitive` is an index, not a compressed blob**; reflection compacts working views **adaptively** (only enough to fit, protecting head + tail) via **iterative goal-tracking summaries**.                                                                                                                                                                          |
| Storage format       | **Append-only JSON Lines**, **segmented** into `worklog/seg-*.jsonl` (one self-contained block per line, keyed by `block_id`) — chosen over text-with-line-ranges (fragile under compaction) and over one monolithic file (unbounded, can't jump). Enables typed metadata, O(1) fetch via `{segment, offset}`, jump by file / iteration / line, and direct FTS5 indexing.                                                                                                                                                                                                                                                                                                                                                      |
| Knowledge graph      | A background **metadata agent** distills every flushed block into `{entities, keywords, ≤25-word summary, workflow, relationships}` → `knowledge_graph.jsonl`, optionally mirrored to an **embedded graph DB** (Kuzu / Cypher, or a SQLite nodes/edges fallback) and/or an **embedded SQLite vector DB** (sqlite-vec) for dynamic recall over past worklogs. Both are file-based and default **off** (file-only).                                                                                                                                                                                                                                                                                                              |
| Memory layers        | **Four-layer hierarchy L1 → L4** (§8): **L1** raw worklog (seek-only), **L2** distilled facts in `knowledge_graph.jsonl` + a **default-on** `knowledge/facts.db` (searched by `KnowledgeSearchTool`), **L3** situational digest `situational.md` + `cognitive_index` (always in the prompt), **L4** behavior / `system_prompt` / policies / delegates (cached prefix). Layers map onto the §3 tiers: L4 = prefix, L3 = situational tier, L2 = on-demand search, L1 = pointer seek.                                                                                                                                                                                                                                             |
| Working folders      | `working_folders[]` are read / searched (never mutated) side by side with the log; `WriteFileTool` stays sandboxed to the `worklog_folder`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Parallelism          | One knob — `parallel_supprocess` (default **1**, sequential) — bounds concurrent subprocess fan-out (delegates, tools, metadata, DB upserts); `>1` = bounded pool, inherited by delegates.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Tool safety          | **Trust-local / ungated** (home-lab); `WriteFileTool` / `SearchFileTool` / `ReadFileTool` resolve paths under the run's `worklog_folder` with path-traversal / absolute-escape rejection (OWASP A01/A03), **plus a content-based sensitive-path deny-list** (`.ssh` / `.env` / cloud-credential stores / `/etc/*`) that blocks reads & writes even inside an allowed root; `skills` load **trusted-local files only**; instructional reads (skills / prompts) forbid **`offset`/`limit` pagination** (a small model reads page 1 and skips the rest). Optional **`require_approval` (default false)** on `RunPythonTool` / `WriteFileTool`. ⚠️ Autonomous code execution can be destructive; revisit before any non-local use. |
| Tool-call protocol   | **Both** — native Ollama `/api/chat` tool-calling when supported; **prompted-JSON + robust parser** fallback for small models.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Tool models          | Each tool may pin its **own `models` ladder** (a leaner local model tuned for tool-calling); a tool that omits `models` **inherits the agent's** top-level ladder, with the same retry-budget semantics (§4, §6).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Logging & search     | **JSONL events + per-run block records + SQLite FTS5 index** for full-text search — with a **trigram tokenizer** (substring / CJK), **incremental bounded merge** (indexing never blocks writes), **query char caps**, and a **resumable rebuild with progress**.                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Prompt caching       | **Stable prefix + volatile suffix.** Everything constant per run (`system_prompt`, `cognitive_behavior`, tool / delegate descriptions) sits in a byte-stable prefix so the model KV-cache / prompt-cache is reused every iteration; only the retrieved working set + answer change. The prefix is rebuilt **only** on a forced compaction — the single sanctioned cache-invalidation event (§3).                                                                                                                                                                                                                                                                                                                               |
| Policy enforcement   | **Enforced, not just prompted.** Critical `cognitive_behavior` policies are declarative _and_ backed by deterministic turn-end guards — `double_check` → verify-on-stop, `say_no` → grounding gate, anti-drift → tool-loop guard — because SLMs ignore prompt-only rules (§5).                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Work vs. failover    | **Two orthogonal budgets.** `max_retries_until_switching_models` triggers _model failover_ only; a separate `max_iterations` caps _total work_ (parent 200 / delegate 50), with a **refund** for batched tool turns. Either limit can end a run (§2, §4).                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Egress redaction     | Block text may cross to a different model (metadata / ladder model, delegate, cloud escalation, optional DB); secrets / PII are **redacted at that boundary** before leaving the agent (§8.2).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Sequencing           | **Phased** — MVP core agent first, then full tools / reflection, then workflow config, then hardening.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Workflow config      | **JSON (`example.json`) + Python construction**, both via `config/load.py` with delegate inheritance + `schema.json` validation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Isolation            | All new code under `src/framework/`. Existing files minimally touched (new `SqliteVectorStore` (sqlite-vec) reusing `Embedding`, Ollama `/api/chat`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

---

## 11. Target Package Layout

```
src/framework/
  __init__.py
  ProgressiveAgentSLM.py         # the single recursive agent class: owns context_window_breakdown, models, cognitive_behavior, tools, delegates; runs the progressive loop and recurses into delegates
  AgentConfig.py                 # parsed config: agent_id, description, system_prompt, worklog_folder, working_folders[], parallel_supprocess, knowledge_graph, context_window_breakdown, max_retries_until_switching_models, models[], cognitive_behavior[], tools[], delegates[] (+ inheritance from parent)
  ContextWindow.py               # four-tier fractional budget over the active model's max_tokens: conversation_history_awareness / cognitive_reflection_behavior / current_working_attention / (remainder=answer); cascade-on-zero; stable-prefix/volatile-suffix assembly (prompt-cache-safe); adaptive compaction
  ModelChain.py                  # per-agent ladder → first reachable model; per-model FAILOVER budget (max_retries_until_switching_models) covering quality + infra; success resets to top; platform factory; max_tokens "auto"; byte+deadline-bounded reads
  IterationBudget.py             # thread-safe TOTAL-WORK counter, separate from failover: consume()/refund() (batched tool turns don't count); parent 200 / delegate 50; either this or ladder exhaustion ends a run
  CognitiveBehavior.py           # renders cognitive_behavior when → then rules into the system prompt
  ToolRegistry.py                # Tool base + dispatch; each tool carries a `when` guidance string + an optional own `models` ladder (inherits the agent's when omitted)
  ParallelExecutor.py            # bounded fan-out helper: runs subprocess steps (delegates, tools, metadata, DB upserts) sequentially (parallel_supprocess=1) or in a bounded pool (>1)
  agents/
    Reflector.py                 # progressive reflection (pluggable engine: should_compress()/compress()): compacts context_window + cognitive_index ADAPTIVELY (only enough to fit) when over budget; protects head+tail; updates the prior summary (iterative); segments stay intact (index, not a compressed blob)
    Router.py                    # reads each delegate.description → picks delegate(s) for a sub-question (generalized _parse_agent_routing → delegate:<agent_id>)
    Guards.py                    # enforced turn-end policy guards: double_check→verify-on-stop (AnswerEvaluator), say_no→grounding gate (similarity floor), anti-drift→tool-loop guard (idempotent-vs-mutating + repeat detection)
  tools/
    SqliteVectorTool.py          # PRIMARY: embedded vector search via SqliteVectorStore.async_query (sqlite-vec, single .db file); optional parallel DocumentRanking when ranking=true
    ReadFileTool.py              # read a file (resolved under worklog_folder/working_folders; traversal-safe + sensitive-path deny-list)
    SearchFileTool.py            # name/content search (ripgrep-style) → path + line + snippet; traversal-safe + deny-list
    WriteFileTool.py             # write a file (sandboxed to worklog_folder; traversal-safe + deny-list); optional require_approval; reuses FileHanlder
    TodoTool.py                  # rewrites <worklog_folder>/todo.md checklist; re-injected each iteration (anti-drift)
    VectorMemoryTool.py          # writable cross-run memory: recall()/remember() over a local SQLite memory table (sqlite-vec; reuses Embedding)
    KnowledgeSearchTool.py       # L2 search (prepared tool code): vector+FTS(+graph) over the run's own fact store knowledge/facts.db; distinct from SqliteVector (external KB)
    SkillTool.py                 # on-demand procedure packs from skills_dir (progressive disclosure; trusted-local)
    GenerateDiagramTool.py       # emits Mermaid for the visualize_diagram policy
    RunPythonTool.py             # wraps tools/PythonCodeExecute; optional require_approval (default false)
    FileKnowledgeTool.py         # files-type knowledge source
  logging/
    RunLogger.py                 # owns the worklog run dir; terminal + block events; single serialized writer
    Worklog.py                   # coordinator (segmented raw + cognitive_index + knowledge_graph + context_window + response_window)
    RawWorklog.py                # append-only, SEGMENTED worklog/seg-*.jsonl; append(block) → {block_id, segment, iteration, line, offset}; rolls per iteration / max_segment_lines; O(1) seek fetch()
    CognitiveIndex.py            # cognitive_index.jsonl pointer map (L3 index); append(pointer{segment,iteration,line,offset})/search()/compact(adaptive); resolves via graph/vector DB when enabled
    SituationalSummary.py        # L3 digest: distils L2 → situational.md ("what I know so far vs. the goal"); regenerated on material L2 change (reuse IterationSummarizer/KnowledgeCompression); injected into the situational tier
    MetadataAgent.py             # L1→L2 promoter: distills each flushed block → knowledge_graph.jsonl (entities, keywords, ≤25-word summary, workflow, relationships) + upserts FactStore; CHEAP-FIRST (KeywordExtractor/SimpleEntityExtractor + lexical overlap before any LLM); ladder model only for summary/workflow; redacts on egress; background curator marks stale/archived (never hard-deletes)
    FactStore.py                 # L2 fact store: default-on knowledge/facts.db (sqlite-vec + FTS); metadata agent upserts distilled records; queried by KnowledgeSearchTool
    KnowledgeGraph.py            # knowledge_graph.jsonl store + optional cross-run mirrors: GraphStore (Kuzu/Cypher, or SQLite nodes/edges) + SqliteVectorStore upsert (sqlite-vec)
    ContextWindowLog.py          # per-agent context_window.log; stream()/retrieve(index)/compact(adaptive)
    ResponseWindow.py            # per-agent response_window.log; write()/flush→raw+index+metadata/clear()
    LogSearch.py                 # SQLite FTS5 index (<worklog_folder>/index.db) over worklog/seg-*.jsonl + cognitive_index.jsonl + knowledge_graph.jsonl + search() + CLI
  config/
    load.py                      # build a ProgressiveAgentSLM tree from JSON or a Python dict; applies delegate inheritance
    schema.json                  # JSON schema for validation
  example.json                   # the canonical bvms-assistant config (§13)

progressive_agent_slm_demo.py    # entry point: load config → ProgressiveAgentSLM → create_chat_backend + uvicorn (port 8001)
```

---

## 12. Phases & Tasks

> Phases 0–1 were built against the earlier delegate-registry design; their primitives exist but need
> **rework** to the recursive four-tier-budget model below — hence 🟡, not ✅. `[~]` = exists, needs
> rework.

### Phase 0 — Foundation primitives 🟡

- [~] `ContextWindow.py`: four-tier **fractional** budget (`conversation_history_awareness` /
  `cognitive_reflection_behavior` / `current_working_attention` / remainder=answer) over the active
  model's `max_tokens`, cascade-on-zero donation, budget-bounded trimming (§3). _(new)_
- [~] `ModelChain.py`: per-agent **ladder** → first reachable model; single per-model retry budget
  `max_retries_until_switching_models` (default 5) covering quality self-eval **and** infra failures;
  success resets to the top model; platform factory (`ollama`→`Ollama`, `open_router`→`OpenRouter`);
  `max_tokens: "auto"` sizing (§4). _(reworks `ModelRegistry`)_
- [~] **SQLite vector store** — `SqliteVectorStore` (`sqlite-vec`): `async_query` +
  `async_get_documents_string` over a local `.db` file (reuses `Embedding`). Replaces the
  Supabase / pgvector backend; the earlier async `SupabaseVectorStore` work is superseded. _(new)_
- [~] `logging/` **worklog** subsystem (§8): append-only **segmented** `RawWorklog` (rolls per
  iteration / `max_segment_lines`; append → `{block_id, segment, iteration, line, offset}`) +
  `CognitiveIndex` (pointer map addressing `{segment, iteration, line, offset}`, cheap keyword
  summaries) + per-agent `ContextWindowLog` + `ResponseWindow`, coordinated by `Worklog` behind **one
  serialized writer**; `RunLogger` owns `<worklog_folder>/<run_id>/`. _(reworks the old
  worklog.md/events.jsonl/transcript.md; the single `raw_worklog.jsonl` is now segmented)_
- [ ] `ParallelExecutor`: bounded fan-out driven by `parallel_supprocess` (default 1 = sequential; >1
      = bounded pool) for delegates, independent tool calls, metadata, and DB upserts. _(new)_
- [ ] `IterationBudget`: thread-safe **total-work** counter separate from model failover — `consume()` /
      **`refund()`** (batched / programmatic tool turns don't count); parent default 200, delegate 50 (§2, §4). _(new)_
- [ ] Progressive reflection (**pluggable engine** with a `should_compress()` / `compress()` lifecycle):
      compact `context_window.log` + `cognitive_index` **adaptively** (only enough to fit) when over the
      `current_working_attention` / `cognitive_reflection_behavior` budgets — **protect head + tail**,
      **update** (not replace) the prior summary, merge / drop pointers (recoverable from the segments). _(new)_
- [ ] Bounded I/O helper: every model / tool read is capped by **bytes + wall-clock deadline** (a stalled
      local endpoint must not hang the run); a deadline hit is one infra failure (§4). _(new)_

### Phase 1 — Recursive core agent (runnable vertical slice) 🟡

- [~] `AgentConfig.py`: parse `agent_id`, `description`, `system_prompt`, `worklog_folder`,
  `working_folders[]`, `parallel_supprocess` (default 1), `context_window_breakdown`,
  `max_retries_until_switching_models` (default 5), `max_iterations` (parent 200 / delegate 50),
  `models[]`, `cognitive_behavior[]`, `tools[]`, `knowledge_graph`, `delegates[]`; apply parent→delegate
  inheritance of the model ladder + failover budget + `max_iterations` + shared `worklog_folder` +
  `working_folders` + `parallel_supprocess` + `knowledge_graph`.
- [~] `ProgressiveAgentSLM.py`: the single recursive class. Per step — retrieve relevant blocks from the
  segmented worklog via `cognitive_index` into `context_window`, assemble the four-tier prompt **as a
  byte-stable prefix + volatile suffix** (§3), select a model from the ladder, apply `cognitive_behavior`
  policies, route to delegates by `description` / prune tools by `when`, emit the answer (remainder tier)
  into `response_window`, flush the block to the segmented worklog + `cognitive_index.jsonl` +
  `knowledge_graph.jsonl`, quick self-eval (switch model on repeated failure). Recurse into `delegates`;
  stop when the model ladder is exhausted **or `max_iterations` is spent**.
- [~] `agents/Router.py`: choose delegate(s) per sub-question by `description` via the generalized
  `_parse_agent_routing` (`delegate:<agent_id>`); prune the tool menu by each tool's `when`. _(reworks
  Forwarder)_
- [~] `agents/Reflector.py`: the cognitive-accumulation compressor (reuse `KnowledgeCompression` +
  `IterationSummarizer`).
- [~] `ToolRegistry.py` + `tools/SqliteVectorTool.py` (primary; `db_file` + `table` + `ranking`) +
  `tools/ReadFileTool.py` + `tools/TodoTool.py`; file tools resolve paths under the run's
  `worklog_folder` **and** any `working_folders` root (read-only), traversal-safe; each tool carries
  its `when` guidance (used for menu pruning) and an optional own `models` ladder (inherits the
  agent's when omitted).
- [~] Wire `RunLogger` + the segmented `Worklog` subsystem (single serialized writer);
  `progressive_agent_slm_demo.py` via `create_chat_backend` (port 8001).

### Phase 2 — Full tools, cognitive_behavior policies, model routing ⬜

- [ ] Remaining tools: `SearchFileTool` (read / search `working_folders` + `worklog_folder`) +
      `WriteFileTool` (writes sandboxed to `worklog_folder`), `VectorMemoryTool` (cross-run memory over a
      local SQLite table, sqlite-vec), `KnowledgeSearchTool` (**L2** search over the run's own fact store),
      `SkillTool` (progressive-disclosure procedure packs), `GenerateDiagramTool`
      (Mermaid), `RunPythonTool` (wrap `PythonCodeExecute`, optional `require_approval`),
      `FileKnowledgeTool`.
- [ ] `CognitiveBehavior.py`: render `cognitive_behavior` `when → then` rules into the system prompt;
      ship the baseline set (deep_think, double_check, visualize_diagram, say_no).
- [ ] **Enforcement guards** behind the critical policies (§5): `double_check` → **verify-on-stop**
      (block a final answer whose evidence doesn't cover the question via `AnswerEvaluator`; inject one
      more round while `max_iterations` remains); `say_no` → **grounding gate** (force honest refusal when
      retrieval is below a similarity floor); anti-drift → **tool-loop guard** (idempotent-vs-mutating
      classification + repeated-call detection). _(new)_
- [ ] Safety hardening: **sensitive-path deny-list** on file tools (beyond traversal checks),
      **no `offset`/`limit`** on instructional reads, and **egress redaction** of block text before it
      crosses to any other model (§8.2, §10). _(new)_
- [ ] `SqliteVector` ranking path: parallel `DocumentRanking` batches (reuse `RagAssistant.stream`) when
      `ranking: true`.
- [ ] Budget enforcement: measure tokens (tokenizer or char-approx), trim each tier to budget,
      implement cascade-on-zero donation.
- [ ] `logging/MetadataAgent.py` (**L1 → L2 promoter**): distill each flushed block → `knowledge_graph.jsonl`
      (`entities`, `keywords`, ≤25-word `summary`, `workflow`, `relationships`) via `KeywordExtractor` /
      `SimpleEntityExtractor` + a ladder model **and upsert the L2 fact store**; run under
      `parallel_supprocess` (§8.2). _(new)_
- [ ] `logging/FactStore.py` + `tools/KnowledgeSearchTool.py`: the **default-on L2 fact store**
      (`knowledge/facts.db`, sqlite-vec + FTS) + the **L2 search tool** (vector + keyword (+ graph) over the
      run's own facts; distinct from `SqliteVector`) (§6, §8.3). _(new)_
- [ ] `logging/SituationalSummary.py` (**L2 → L3**): maintain `situational.md` — a compact goal-relative
      "what I know so far" digest, regenerated on **material L2 change** (threshold-triggered, cheap model),
      injected into the situational tier each step (§3, §8.2). _(new)_
- [ ] `logging/KnowledgeGraph.py`: optional **embedded cross-run** mirrors of `knowledge_graph.jsonl` into a
      **graph DB** (Kuzu / Cypher, or SQLite nodes/edges) and/or a **SQLite vector DB**
      (`SqliteVectorStore`, sqlite-vec); `cognitive_index.search` resolves against them when enabled.
      Both default **off** (§8.3). _(new)_
- [ ] `logging/LogSearch.py`: SQLite FTS5 index (`<worklog_folder>/index.db`) over `worklog/seg-*.jsonl`
  - `cognitive_index.jsonl` + `knowledge_graph.jsonl` + search + CLI over all runs — **trigram
    tokenizer** (substring / CJK), **incremental bounded merge** (never blocks writes), **query char
    caps**, and a **resumable rebuild with progress** (§8).
- [ ] `VectorMemoryTool` I/O discipline: **background prefetch pre-turn / sync post-turn** with a bounded
      drain timeout, so long-term memory never blocks the critical path (§6). _(new)_

### Phase 3 — Config loader (JSON + Python) ⬜

- [ ] `config/load.py` + `config/schema.json`: build a `ProgressiveAgentSLM` tree from `example.json`
      (or a Python dict) with validation + delegate inheritance; the schema covers `working_folders[]`,
      `parallel_supprocess`, and `knowledge_graph` (incl. `graph_db` / `vector_db`).
- [ ] Round-trip the canonical `example.json` (§13) end-to-end as a worked example + regression check;
      authoring README.

### Phase 4 — Hardening ⬜

- [ ] Unit tests: config loader / inheritance (incl. `working_folders` / `parallel_supprocess` /
      `knowledge_graph` / `max_iterations`), four-tier budgeting + cascade, **stable-prefix / volatile-suffix
      assembly stays byte-identical across iterations** (cache-safety), `cognitive_index` pointer append +
      **adaptive** compaction (head+tail protection, iterative summary, `block_id` integrity), **segmented
      worklog** append + jump by `{segment, iteration, line, offset}` + segment rollover, **metadata agent**
      `knowledge_graph.jsonl` fields + **cheap-first** extraction + **egress redaction**, **`IterationBudget`
      consume / refund** + parent-vs-delegate caps, **`ParallelExecutor`** sequential-vs-pool
      (`parallel_supprocess`), optional graph / vector mirrors, model-ladder **failover** switch + success-reset
      (independent of `max_iterations`), **enforcement guards** (verify-on-stop / grounding gate / tool-loop),
      **file-tool deny-list** + traversal rejection, router description-routing parser, Supabase tool, `Worklog`
      append / read behind one writer, `RunLogger` JSONL + FTS round-trip (trigram / incremental merge).
- [ ] Integration smoke test with a stub model implementing `.stream`.
- [ ] Timeouts / retries (reuse 429 / backoff from `OpenRouter`); model fall-through; **byte + deadline
      bounded reads** (§4).
- [ ] Optional `require_approval` (default false) on `RunPythonTool` / any shell tool.

---

## 13. Example: The `bvms-assistant` Config

The canonical configuration (live copy: `src/framework/example.json`). It defines a top orchestrator
with **two RAG-backed delegates** — each delegate is itself a full `ProgressiveAgentSLM` with its own
proportional `context_window_breakdown` and embedded SQLite vector store (the code delegate also pins
its own `models`). The same tree can be authored in JSON or built in Python; both produce the same agent and
drop into `create_chat_backend`.

### 13a. JSON (declarative, recursive)

```json
{
  "agent_id": "bvms-assistant",
  "description": "Specialized Agent that can answer technical question about BVMS (BBC Voyage Management System).",
  "worklog_folder": "wip/bvms-assistant",
  "working_folders": [
    {
      "path": "bvms/be-source-code",
      "description": "BVMS backend source code"
    },
    {
      "path": "bvms/fe-source-code",
      "description": "BVMS frontend source code"
    }
  ],
  "parallel_supprocess": 1,
  "system_prompt": "You are a helpful assistant that answers questions about BVMS (BBC Voyage Management System) by combining domain knowledge, code analysis, and diagrams. You can delegate to specialist sub-agents when needed.",
  "max_retries_until_switching_models": 5,

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

  "knowledge_graph": {
    "file": "knowledge_graph.jsonl",
    "metadata_model": "inherit",
    "worklog": { "segment_by": "iteration", "max_segment_lines": 2000 },
    "graph_db": {
      "enabled": false,
      "type": "kuzu",
      "path": "knowledge_graph.kuzu"
    },
    "vector_db": {
      "enabled": false,
      "type": "sqlite",
      "db_file": "knowledge_graph.db",
      "table": "worklog_knowledge"
    }
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
          "type": "SqliteVector",
          "db_file": "knowledge/bvms_docs.db",
          "table": "bvms_documents",
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
          "type": "SqliteVector",
          "db_file": "knowledge/bvms_code.db",
          "table": "bvms_code",
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

`bvms-general-knowledge` omits `models` and `max_retries_until_switching_models`, so it **inherits**
them from the parent; `bvms-code-knowledge` pins its own bigger local model but still inherits the
retry budget. Both share the parent's `worklog_folder` (one segmented worklog + `cognitive_index` +
`knowledge_graph.jsonl` for the whole run) while keeping their own `context_window.log` + `response_window.log`. Because every tier
is a **fraction** of the active model's `max_tokens`, no request can overflow: the parent's
`0.025 / 0.325 / 0.525` resolve to ≈ 1,550 / 20,150 / 32,550 of gpt-oss's 62,000 (≈ 7,750 left to
answer); the general delegate folds its two zeroed front tiers into ~0.725 of working attention, and
the code delegate keeps a modest 0.225 cognitive slice on its 64k model.

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
    working_folders=[dict(path="bvms/be-source-code", description="BVMS backend source code"),
                     dict(path="bvms/fe-source-code", description="BVMS frontend source code")],
    parallel_supprocess=1,
    knowledge_graph=dict(file="knowledge_graph.jsonl", metadata_model="inherit",
                         graph_db=dict(enabled=False, type="kuzu", path="knowledge_graph.kuzu"),
                         vector_db=dict(enabled=False, type="sqlite", db_file="knowledge_graph.db",
                                        table="worklog_knowledge")),
    system_prompt="You are a helpful assistant that answers questions about BVMS by combining "
                  "domain knowledge, code analysis, and diagrams, delegating to specialists when needed.",
    context_window_breakdown=dict(conversation_history_awareness=0.025,
                                  cognitive_reflection_behavior=0.325,
                                  current_working_attention=0.525),
    max_retries_until_switching_models=5,
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
        dict(type="ReadFileTool", when="A referenced local file is needed.",
             models=[dict(platform="ollama", name="qwen3.5:9b", url="http://localhost:11434", max_tokens=32000)]),
        dict(type="TodoTool", when="Keep the run checklist current."),  # inherits parent models
        dict(type="VectorMemoryTool", db_file="memory/agent_memory.db", table="agent_memory",
             when="Recall/remember durable facts across runs."),
    ],
    delegates=[
        ProgressiveAgentSLM(
            agent_id="bvms-general-knowledge",
            description="Domain & workflow knowledge about BVMS.",
            context_window_breakdown=dict(conversation_history_awareness=0,
                                          cognitive_reflection_behavior=0,
                                          current_working_attention=0.725),
            tools=[dict(type="SqliteVector", db_file="knowledge/bvms_docs.db", table="bvms_documents",
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
            tools=[dict(type="SqliteVector", db_file="knowledge/bvms_code.db", table="bvms_code",
                        ranking=True, when="Code-level questions: internals, APIs.")],
        ),
    ],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_chat_backend(assistant), host="0.0.0.0", port=8001, timeout_keep_alive=300)
```

> A delegate that omits `models` / `max_retries_until_switching_models` inherits the parent's, and
> shares the run's `worklog_folder`. Each finished block is appended to the shared append-only
> segmented worklog and mapped in `cognitive_index` (§8), so the two delegates can loop back over each
> other's work by index lookup rather than replaying the whole log.

---

## 14. Key Reuse Map (concrete)

| Existing asset                                                   | Reused for                                                                                                            |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `AssistantOrchestra.stream`                                      | `ProgressiveAgentSLM` per-step loop (route → execute → accumulate → reflect → iterate)                                |
| `AssistantOrchestra._parse_agent_routing` / `_parse_eval_result` | `Router` delegate selection (`delegate:<agent_id>`) + double-check evaluation parsing                                 |
| `AssistantOrchestra.add_agent` / `agents` registry               | The recursive `delegates` registry (each keyed by `agent_id` + `description`)                                         |
| `all_agent_responses` + `IterationSummarizer` compaction         | Seed for the segmented worklog blocks + the adaptive progressive-reflection compaction                                |
| `KnowledgeCompression`, `IterationSummarizer`                    | `Reflector` — the adaptive compaction of `context_window` + `cognitive_index` (not a blob)                            |
| `KeywordExtractor`, `SimpleEntityExtractor`                      | Cheap ~10–20-token `cognitive_index` summaries + `knowledge_graph` entities / keywords (LLM summary only when needed) |
| `SqliteVectorStore` (sqlite-vec) + `Embedding`                   | `VectorMemoryTool` — writable cross-run SQLite memory table (`remember` / `recall`)                                   |
| `FileHanlder` / `PythonCodeExecute`                              | `WriteFileTool` / `SearchFileTool` / `RunPythonTool` (traversal-safe under `worklog_folder`)                          |
| `RagAssistant.stream` (parallel `DocumentRanking` batches)       | `SqliteVectorTool` ranking path (`ranking: true`)                                                                     |
| `SqliteVectorStore.async_query` (sqlite-vec)                     | `SqliteVectorTool` — the primary capability (embedded, single `.db` file)                                             |
| `Task` + DI-kwargs pattern                                       | `Router`, `Reflector` agents                                                                                          |
| `AnswerEvaluator`, `FinalThoughtSummarizer`                      | `double_check` policy + final recap from the worklog                                                                  |
| `PythonCodeExecute`                                              | `RunPythonTool` (optional `require_approval`, default false)                                                          |
| `Ollama` (`/api/generate`) / `OpenRouter` (429 backoff)          | The per-agent `models` chain via the platform factory (local-first, cloud fallback)                                   |
| `ChatBackend.create_chat_backend`                                | Unchanged streaming integration point                                                                                 |

---

## 15. Verification

1. **Unit**: config loader + delegate inheritance, four-tier **fractional** budgeting (trim +
   cascade-on-zero over each model's `max_tokens`), `cognitive_index` pointer append + adaptive compaction,
   model-ladder switch (single retry budget covering quality + infra) + success-reset, `Router`
   description-routing selection parser, `SqliteVectorTool`, segmented `Worklog` append / read (`block_id`
   integrity) behind one writer, `RunLogger` JSONL + FTS round-trip.
2. **Integration smoke**: load `example.json` with a stub model — assert the tree builds, the parent
   routes to a delegate by `description`, the delegate calls its SQLite vector tool and appends blocks under
   its own `agent_id`, `cognitive_index` grows yet stays ≤ its budget, and the `worklog/` segments +
   `cognitive_index.jsonl` + `knowledge_graph.jsonl` (+ per-agent `context_window.log` / `response_window.log`) exist and FTS
   search returns the run.
3. **Manual**: launch `progressive_agent_slm_demo.py` via uvicorn, ask a multi-step BVMS question,
   confirm streamed think / route / delegate / answer, per-block worklog flushing + index-and-retrieve,
   and on-disk logs searchable via the `LogSearch` CLI.
4. **Budget**: assert no request exceeds the selected model's `max_tokens`, and that a delegate omitting
   `models` inherits the parent's chain.

---

## 16. Open Questions

| #   | Question                                                                                                      | Recommendation / Resolution                                                                                                                                                                                                                                                                                                                              | Decision   |
| --- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| 1   | Recursion — is every delegate a full `ProgressiveAgentSLM`?                                                   | Yes; core to the design. Recursion depth is bounded by the finite delegate tree; per-agent work is bounded by `max_retries_until_switching_models` + ladder exhaustion.                                                                                                                                                                                  | ✅ Decided |
| 2   | Memory model — is `cognitive` compressed knowledge or an index?                                               | An **index** (pointer map into the append-only **segmented** worklog, addressing `{segment, iteration, line, offset}`); the **worklog** subsystem replaces the old `runs/` artifacts.                                                                                                                                                                    | ✅ Decided |
| 3   | Model switching — what counts as a "failed attempt"?                                                          | A single per-model budget `max_retries_until_switching_models` (default 5) counts **both** a quality failure (from the quick self-eval) **and** an infra failure (timeout / HTTP); when it is spent, drop to the next model. Success resets the ladder to the top.                                                                                       | ✅ Decided |
| 4   | Ladder exhaustion — loop, stop, or ladder-as-escalation?                                                      | **Ladder-as-escalation** — walk top-down once; the run stops when the last model exhausts its retry budget (no separate global iteration cap).                                                                                                                                                                                                           | ✅ Decided |
| 5   | Per-step (per-policy) model choice?                                                                           | **No** — `cognitive_behavior` stays declarative (system-prompt + todo); model choice is global via the ladder.                                                                                                                                                                                                                                           | ✅ Decided |
| 6   | Routing signal — how are delegates vs. tools selected?                                                        | **Delegates** are chosen by `description` only (agent-level `when` removed); **tools** keep a `when` that a cheap pre-pass uses to prune the menu before the SLM picks.                                                                                                                                                                                  | ✅ Decided |
| 7   | Worklog storage format — text `.log` with line ranges, structured JSON, or a monolithic array?                | **Append-only JSON Lines**, **segmented** into `worklog/seg-*.jsonl` (one self-contained block per line, keyed by `block_id`). Line ranges were fragile under compaction and one monolithic file grew unbounded; segmented JSONL keeps append-only, adds typed metadata, works with FTS5, and enables O(1) jump by `{segment, iteration, line, offset}`. | ✅ Decided |
| 8   | Token measurement for budgeting — real per-model tokenizer, or char≈token approximation?                      | **`char/4` for both the budget estimate AND the compaction threshold** (one heuristic, so measure and trigger never disagree — matches Hermes's `estimate_request_tokens_rough`); pluggable exact tokenizer in P2.                                                                                                                                       | ✅ Decided |
| 9   | `cognitive_index` summaries — cheap keyword extraction or LLM per block?                                      | Keyword / entity extraction by default (`KeywordExtractor`); LLM summary only when needed.                                                                                                                                                                                                                                                               | _TBD_      |
| 10  | `VectorMemory` scope & backing store — cross-run? SQLite file or server?                                      | Cross-run persistent; a dedicated **local SQLite** memory table (`sqlite-vec`) reusing `Embedding` — a single `.db` file, no server.                                                                                                                                                                                                                     | ✅ Decided |
| 11  | `worklog_folder` lifecycle — one ephemeral `<worklog_folder>/<run_id>/` per question; `VectorMemory` durable? | Yes — `<worklog_folder>/<run_id>/` is per-run; durable cross-run knowledge lives in `VectorMemory`.                                                                                                                                                                                                                                                      | _TBD_      |
| 12  | Worklog file growth — one big file, or many?                                                                  | **Segmented** into `worklog/seg-*.jsonl` (one segment per iteration; optional `max_segment_lines` cap). The `cognitive_index` addresses blocks by `{segment, iteration, line, offset}` for O(1) jump by file / iteration / line (§8.1).                                                                                                                  | ✅ Decided |
| 13  | Per-block metadata — how is it produced, and where does it go?                                                | A background **metadata agent** distills each flushed block into `{entities, keywords, ≤25-word summary, workflow, relationships}` → `knowledge_graph.jsonl` (§8.2), reusing `KeywordExtractor` / `SimpleEntityExtractor` + a ladder model.                                                                                                              | ✅ Decided |
| 14  | Dynamic retrieval over old worklogs — files only, or a database?                                              | Optional **embedded** mirrors of `knowledge_graph.jsonl`: a file-based **graph DB** (Kuzu / Cypher, or a SQLite nodes/edges fallback) and/or a **SQLite vector DB** (`sqlite-vec`); `cognitive_index.search` resolves against them when enabled. Both are file-based and default **off** (§8.3).                                                         | ✅ Decided |
| 15  | Sub-process concurrency — run steps sequentially or in parallel?                                              | One knob, `parallel_supprocess` (default **1** = sequential; `>1` = bounded pool), inherited by delegates; it bounds delegate / tool / metadata / DB-upsert fan-out (§2).                                                                                                                                                                                | ✅ Decided |
| 16  | Vector store backend — hosted Supabase / pgvector, or embedded?                                               | **Embedded SQLite** (`sqlite-vec`): every knowledge / memory / mirror store is a single local `.db` file you can copy or read directly — no server. Tools take `{ db_file, table }`; the primary tool is `SqliteVector` on a new `SqliteVectorStore` (§6, §8.3).                                                                                         | ✅ Decided |
| 17  | Tool models — reuse the agent's ladder, or run their own?                                                     | Each tool may pin its **own `models`** ladder (a leaner local model tuned for tool-calling); a tool that omits `models` **inherits the agent's** top-level ladder (§6).                                                                                                                                                                                  | ✅ Decided |
| 18  | Prompt assembly — rebuild the whole prompt each iteration, or keep a stable prefix?                           | **Stable prefix + volatile suffix** (§3): run-constant tiers stay byte-stable so the KV / prompt cache is reused; compaction is the only sanctioned rebuild. _(Hermes lesson.)_                                                                                                                                                                          | ✅ Decided |
| 19  | Behavioral policies — prompt-only, or enforced?                                                               | **Both** — declarative `when → then` on the surface, deterministic turn-end guards behind the critical ones (`double_check`, `say_no`, anti-drift), because SLMs ignore prompt-only rules (§5). _(Hermes lesson.)_                                                                                                                                       | ✅ Decided |
| 20  | Total work vs. model failover — one budget or two?                                                            | **Two** — `max_retries_until_switching_models` = failover only; separate `max_iterations` = total work (parent 200 / delegate 50) with a refund for batched turns (§2, §4). _(Hermes lesson.)_                                                                                                                                                           | ✅ Decided |
| 21  | Compaction target — fixed 50%, or adaptive?                                                                   | **Adaptive** — shrink only enough to fit, protect head + tail, and **update** the prior summary (iterative, goal-tracking) rather than replace it (§3, §8). _(Hermes lesson.)_                                                                                                                                                                           | ✅ Decided |
| 22  | Delegate boundary — pass agent objects, or a typed contract?                                                  | **Typed, immutable contract** — frozen request (goal / context / role / allowed*toolsets, byte-capped) + frozen result + explicit state machine + restricted toolset (§7). *(Hermes lesson.)\_                                                                                                                                                           | ✅ Decided |
| 23  | Memory model — flat worklog, or an explicit layered hierarchy?                                                | **Four layers L1 → L4** (§8): raw → facts → situational → behavior, each derived from the one below and progressively closer to the prompt; the layers compose with the §3 context tiers (L4 = prefix, L3 = situational tier, L2 = on-demand search, L1 = pointer seek).                                                                                 | ✅ Decided |
| 24  | L2 fact store — optional mirror, or a first-class default store?                                              | **First-class, default-on** `knowledge/facts.db` (sqlite-vec + FTS), fed by the metadata agent and queried by `KnowledgeSearchTool`; cross-run graph / vector mirrors stay optional (§8.3). Supersedes the earlier "mirrors default off" for the per-run fact store.                                                                                     | ✅ Decided |
| 25  | L3 situational digest — regenerate every iteration, or on change?                                             | **On material L2 change** (threshold-triggered, cheap model) — keeps the always-in-prompt digest current without a per-iteration summary cost (§8.2).                                                                                                                                                                                                    | ✅ Decided |
| 26  | L2 lifetime — per-run only, or cross-run?                                                                     | **Per-run by default**, rebuilt each run; durable facts can be promoted into the cross-run `VectorMemoryTool`, and earlier runs reached via the optional §8.3 mirrors. Revisit if per-run rebuild proves wasteful.                                                                                                                                       | _TBD_      |

---

## 17. Logging Artifacts & Record Schemas

The `worklog` subsystem per run (see §8), organized as the four memory layers **L1 → L4**, replacing
the old `runs/` artifacts:

- **`worklog/seg-*.jsonl`** _(L1)_ — shared, **append-only, segmented** single source of truth. Every
  finished block (any model, main or delegate) is one JSON record on its own line, keyed by a stable
  `block_id`; blocks are sharded into per-iteration segments (rolled at `max_segment_lines`). Never rewritten.
- **`knowledge_graph.jsonl`** _(L2)_ — shared **metadata / knowledge graph**: one record per block from
  the metadata agent (§8.2) — entities, keywords, a ≤25-word summary, workflow, and relationships.
- **`knowledge/facts.db`** _(L2, default-on)_ — the **fact store** (sqlite-vec + FTS): the queryable form
  of the distilled facts, upserted by the metadata agent and searched by `KnowledgeSearchTool` (§6).
- **`cognitive_index.jsonl`** _(L3 index)_ — shared **pointer map**: one record per block (schema below)
  that also records the block's physical location `{segment, iteration, line, offset}`, so the agent can
  jump to it by file / iteration / line and pull only the relevant blocks back into a working window.
- **`situational.md`** _(L3 digest)_ — the running "what I know so far vs. the goal" summary distilled
  from L2 by the situational summarizer (§8.2); **injected into the situational tier of every prompt**.
- **`context_window.log`** _(L1)_ — per-agent working set (plain text); compacted adaptively over its
  `current_working_attention` budget.
- **`response_window.log`** _(L1)_ — per-agent latest answer (plain text); flushed to the segments + index +
  metadata agent, then cleared each iteration.
- **`<worklog_folder>/index.db`** _(optional)_ — SQLite FTS5 over `worklog/seg-*.jsonl` +
  `cognitive_index.jsonl` + `knowledge_graph.jsonl` for `LogSearch`.

**Segment block record** (verbatim block + metadata):

```json
{
  "block_id": "run7-bvms-code-knowledge-iter3-002",
  "ts": "2026-08-02T12:34:56Z",
  "agent_id": "bvms-code-knowledge",
  "iteration": 3,
  "phase": "delegate",
  "actor": "tool:SqliteVector",
  "content": "…the full verbatim block text…",
  "tokens": 512
}
```

**`cognitive_index.jsonl` pointer record** (a **pointer** with a physical location, not the full block):

```json
{
  "block_id": "run7-bvms-code-knowledge-iter3-002",
  "segment": "worklog/seg-003.jsonl",
  "iteration": 3,
  "line": 2,
  "offset": 5342,
  "agent_id": "bvms-code-knowledge",
  "phase": "delegate",
  "actor": "tool:SqliteVector",
  "summary": "≈10–20-token gist of the block",
  "keywords": ["voyage", "approval", "saga"],
  "tokens": 512
}
```

**`knowledge_graph.jsonl` metadata record** (from the metadata agent, §8.2):

```json
{
  "block_id": "run7-bvms-code-knowledge-iter3-002",
  "segment": "worklog/seg-003.jsonl",
  "iteration": 3,
  "entities": ["VoyageService", "FuelOptimizationService", "Voyage"],
  "keywords": ["voyage", "approval", "saga"],
  "summary": "VoyageService coordinates approval across services with a saga; fuel optimization runs before commit.",
  "workflow": "Create Voyage → validate → optimize fuel → approve → emit VoyageApproved",
  "relationships": [
    {
      "from": "VoyageService",
      "type": "calls",
      "to": "FuelOptimizationService"
    },
    { "from": "VoyageService", "type": "writes", "to": "Voyage" }
  ]
}
```

`phase` ∈ `route | act | observe | reflect | delegate | answer`; `actor` ∈
`router | reflector | tool:NAME | delegate:<agent_id>`. The segments are the verbatim source of truth;
`cognitive_index.jsonl` is the retrieval map over them (jump by `{segment, iteration, line, offset}`);
`knowledge_graph.jsonl` is the derived meaning / structure layer; per-agent `context_window.log` holds
only the blocks pulled back in; `response_window.log` holds the current answer. Compaction only ever
touches the derived views — the segments are immutable, so any detail is one `{segment, offset}` seek
away.

---

_Last updated: 2026-08-08_
