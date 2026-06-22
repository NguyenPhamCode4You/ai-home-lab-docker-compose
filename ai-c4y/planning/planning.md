# ProgressiveAgentSLM — Planning & Progress Tracker

> **ProgressiveAgentSLM** is a single, **recursive** agent class optimized for **local / small
> language models (SLMs)**. One instance owns an identity, a four-tier **token budget**
> (`context_window`), a priority list of **models**, a set of **reasoning** policies (`when → then`),
> a set of **tools** (Supabase vector search first), and a set of **delegates** — which are
> themselves `ProgressiveAgentSLM` instances. The agent _progressively_ accumulates compressed
> understanding in its **cognitive** layer while keeping every tier within budget, and streams its
> work into a shared **worklog** in realtime so delegate teammates can read along and continue it.
>
> Any model slot can be escalated, plug-and-play, to a more capable **cloud** model (OpenRouter). The
> class reuses existing primitives (`Task`, model clients, `SupabaseVectorStore`, `DocumentRanking`,
> `PythonCodeExecute`, `KnowledgeCompression`, `IterationSummarizer`, `AnswerEvaluator`,
> `FinalThoughtSummarizer`) and drops into `create_chat_backend` unchanged.

**Status legend:** ⬜ Not started · 🟡 In progress · ✅ Done · ⛔ Blocked

---

## 1. Vision & Design Philosophy

- **One recursive class.** Everything is a `ProgressiveAgentSLM`. A "team" is simply an agent whose `delegates` are other agents — composition _is_ recursion; there is no separate orchestrator type. Each agent carries its own `agent_id` + `description` so any parent can decide when to hand it a sub-question.
- **Progressive cognition under a token budget.** The model's context window is explicitly partitioned into four tiers (§3). Rather than dumping everything into one prompt, the agent keeps a small **cognitive** memory that grows by absorbing each step's context + answer (compressed by reflection). On small models, quality comes from disciplined budgeting + accumulation — not a bigger model.
- **Local & SLM-first, cloud optional.** `models` is a priority list (highest → lowest). Local Ollama models do the frequent work; a cloud model (OpenRouter) can sit lower as an automatic fallback, or be promoted to the top for hard steps — a one-line change.
- **Behavior by policy, not by code.** `reasoning` is a list of `when → then` rules injected into the system prompt, so a non-programmer can shape how the agent thinks (deep-think, double-check, visualize, say-no) without touching Python.
- **Realtime, shared worklog.** Every token an agent prints is flushed immediately to the run's `worklog.md`. Delegates read the live worklog to see what teammates have already done and append their own contributions — true multi-agent collaboration on one artifact.
- **Reuse, don't rebuild.** Async streaming generators that `yield` chunks, DI via constructor kwargs, `Task`-subclass agents, prompt-based JSON with robust regex fallbacks, JSON-file config/state. New code lives under `src/framework/`; existing files are touched minimally.

---

## 2. The `ProgressiveAgentSLM` Object

A single class configured by one object (JSON or Python). Every field has a sensible default; only `agent_id`, `description`, and at least one `model` are required.

| Field                           | Type        | Meaning                                                                                                           |
| ------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------- |
| `agent_id`                      | str         | Stable identifier. Used by a parent to address this agent (`delegate:<agent_id>`) and as its **worklog** section. |
| `description`                   | str         | One-line capability summary. Read by a parent agent to decide **when** to delegate here.                          |
| `context_window`                | object      | The four-tier token budget (§3) — the heart of the design.                                                        |
| `max_iterations_untill_give_up` | int \| null | Max self-iterations before stopping. Default **5**. `null` → iterate until the user cancels.                      |
| `models`                        | list        | Priority-ordered model chain (§4). First that fits the budget and is reachable wins; the rest are fallbacks.      |
| `reasoning`                     | list        | `when → then` behavioral policies (§5) injected into the system prompt.                                           |
| `tools`                         | list        | Capabilities the agent may call, each with a `when` guidance string (§6). Supabase vector search is primary.      |
| `delegates`                     | list        | Nested `ProgressiveAgentSLM` configs (§7). The agent routes sub-questions to them by `agent_id` / `description`.  |

> **Inheritance:** a delegate that omits `models` / `max_iterations_untill_give_up` **inherits the parent's**. `context_window`, `reasoning`, and `tools` are per-agent (not inherited), so each delegate is independently budgeted and specialized.

---

## 3. `context_window` — the four-tier progressive token budget

The model's usable context is split into four named budgets, assembled into the prompt in the order below. The **cognitive** tier is what makes the agent _progressive_.

| Tier                            | Default | Holds                                                                                 | Cascade / growth rule                                                                                                                 |
| ------------------------------- | ------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_awareness_tokens` | 800     | The ongoing user-facing chat history the agent may see.                               | If **0**, its budget is **donated to the next tier (`cognitive`)** — the agent "stops listening to chat" and thinks harder.           |
| `cognitive_tokens`              | —       | The agent's accumulated self-reflection over the whole conversation + knowledge seen. | After every answer: `cognitive ← reflect(cognitive + context + answer)`, compressed back **down to this budget**. Progressive memory. |
| `context_tokens`                | —       | The current working set: retrieved knowledge, tool outputs, the sub-question at hand. | Refilled each step, trimmed to budget. Donates unused space to `answering` if 0.                                                      |
| `answering_tokens`              | —       | Max tokens this agent may emit as its answer for a step.                              | Hard cap on output length.                                                                                                            |

**Prompt assembly per step** (the system prompt is separate overhead):

```
[ system: description + reasoning(when→then) + tool/delegate guidance ]
[ cognitive memory             ≤ cognitive_tokens ]
[ conversation awareness       ≤ conversation_awareness_tokens ]
[ current context / KB / tools ≤ context_tokens ]
[ question ]
→ answer                       ≤ answering_tokens
```

**Cognitive accumulation (core loop invariant):**

```
cognitive(t+1) = Reflector.compress(
    old           = cognitive(t),
    plus_context  = context_used(t),
    plus_answer   = answer(t),
    target_tokens = cognitive_tokens,
)
```

After each iteration the agent folds what it just saw and said into a compact, budget-bounded memory — preventing overflow while preserving continuity. The total request size ≈ the sum of the four tiers (+ system overhead), which is used to **auto-infer** the model token requirement (§4).

---

## 4. Models — per-agent priority chain

`models` is an ordered list, highest priority first. Each entry:

| Key          | Required   | Meaning                                                                                                 |
| ------------ | ---------- | ------------------------------------------------------------------------------------------------------- |
| `platform`   | yes        | `ollama` (local) or `open_router` (cloud). Maps to the existing `Ollama` / `OpenRouter` clients.        |
| `name`       | yes        | Model name on that platform.                                                                            |
| `url`        | for ollama | Endpoint (defaults to `OLLAMA_URL`).                                                                    |
| `max_tokens` | no         | Context ceiling. A number caps it; `"auto"` (or omitted) sizes the request to the `context_window` sum. |

Selection: walk the list top-down; pick the first model whose `max_tokens` ≥ the required budget (auto-inferred from §3) **and** that is reachable. On timeout / HTTP error, fall through to the next. This is the per-agent generalization of a role-based registry — local-first with cloud as an automatic backstop, or cloud promoted by putting it first.

```json
"models": [
  { "platform": "ollama",      "name": "gpt-oss:20b",                 "url": "http://localhost:11434", "max_tokens": 62000 },
  { "platform": "open_router", "name": "anthropic/claude-3.5-sonnet", "max_tokens": "auto" }
]
```

---

## 5. Reasoning — `when → then` behavioral policies

`reasoning` is a list of rules that shape the agent's behavior. Each rule renders into the system prompt as "**When** _condition_, **then** _action_." This lets the workflow author steer a small model declaratively, without code.

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

Other tools (`ReadFileTool`, `GenerateDiagramTool`, `RunPythonTool` with optional `approval` defaulting to allow, files knowledge) follow the same `{ type, when, … }` shape. The Supabase wrapper is built on the now-async `SupabaseVectorStore.async_query`.

---

## 7. Delegates — recursive composition

`delegates` is a list of **nested `ProgressiveAgentSLM` configs**. There is no separate "sub-agent" type — a delegate is a full agent with its own `context_window`, `tools`, and optional `reasoning` / `models` / `delegates`. The parent:

1. **Routes** by reading each delegate's `description` to decide **which** delegate(s) a sub-question goes to (the proven `_parse_agent_routing` JSON pattern, generalized to `delegate:<agent_id>`).
2. **Hands the sub-question down**; the delegate runs its own full progressive loop and streams into the **same** run worklog under its own `agent_id` section.
3. **Collects** the delegate's result back into its own `context` tier, then reflects it into `cognitive`.

Depth is bounded by `max_iterations_untill_give_up` at each level plus an overall recursion cap. Two RAG-backed delegates (`bvms-general-knowledge`, `bvms-code-knowledge`), each owning a Supabase function, is the canonical example (§13).

---

## 8. The Worklog — realtime shared memory

One `runs/<run_id>/worklog.md` per run is the team's shared, **live** working memory.

- **Realtime flush.** Every chunk an agent or delegate streams is appended to the worklog **as it is printed** (line-buffered flush), not only at end-of-step. A teammate reading the worklog sees work in progress.
- **Delegate-team coordination.** Each agent writes under its own `## <agent_id>` section. Before starting, a delegate **reads** the current worklog to learn what is already established and continue rather than repeat.
- **Reflection curates it.** After each iteration the `Reflector` compresses the relevant slice into the parent's `cognitive` tier (§3). The verbatim stream stays in `transcript.md`; the worklog holds the working narrative; `cognitive` holds the compressed memory.
- **Seeds the final answer & KB.** The final recap is built from the worklog; durable facts may be persisted back to a knowledge source.

```
runs/<run_id>/
  worklog.md       # ← shared, realtime-flushed team narrative (per-agent sections)
  events.jsonl     # append-only structured event stream (§17)
  transcript.md    # full verbatim rendering
# runs/index.db    # SQLite FTS5 index over all runs' events (full-text search)
```

---

## 9. Goals → Components

| Goal (user)                                                                                | Realized by                                                                                        |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Single recursive class anyone can configure (one object)                                   | `ProgressiveAgentSLM` + `AgentConfig` + `config/load.py`                                           |
| **Goal**: stay focused on the user-set goal                                                | `reasoning` policies + double-check / re-iterate loop (reuse `AnswerEvaluator`)                    |
| **Knowledge**: text files + Supabase vector DB                                             | `SupabaseTool` (primary, pgvector) + `FileKnowledgeTool`                                           |
| **Tools**: Supabase vector DB first, read file, diagrams, run Python                       | `ToolRegistry` + `tools/` (`SupabaseTool`, `ReadFileTool`, `GenerateDiagramTool`, `RunPythonTool`) |
| **Reflection/cognition**: accumulate compressed memory within budget                       | `Reflector`: `cognitive ← compress(...)` (reuse `KnowledgeCompression` + `IterationSummarizer`)    |
| **Delegate**: break task into steps/sub-agents, collect results                            | Recursive `delegates` + `Router` (`delegate:<agent_id>`) dispatch                                  |
| **Worklog**: one realtime shared file every delegate streams into, distilled by reflection | `Worklog` (realtime, per-`agent_id` sections) + `Reflector`                                        |
| Local/SLM-first with plug-and-play cloud escalation (OpenRouter)                           | `ModelChain` (per-agent priority list + local→cloud fallback)                                      |
| Per-step logging to terminal + files for full-text search                                  | `RunLogger` (JSONL + Markdown) + `LogSearch` (SQLite FTS5)                                         |
| Workflow configurable via JSON **and** Python                                              | `config/load.py` (`example.json` + `schema.json`) + `ProgressiveAgentSLM(...)`                     |

---

## 10. Design Decisions

| Topic                | Decision                                                                                                                                                                                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent & control flow | **Recursive progressive loop** — each step assembles the four-tier prompt, applies reasoning policies, calls tools / routes to delegates, then folds context+answer into `cognitive`; iterate up to `max_iterations_untill_give_up`.                        |
| Delegation           | **Follow `AssistantOrchestra`** routing (`_parse_agent_routing`), generalized to `delegate:<agent_id>`; a parent routes by reading each delegate's `description`. Delegates inherit `models` + `max_iterations_untill_give_up`.                             |
| Models (defaults)    | **Per-agent priority list** (highest→lowest): first reachable model that fits the budget wins; **OpenRouter** cloud as automatic fallback or promoted to top. `max_tokens: "auto"` sizes to the budget.                                                     |
| Worklog              | **One realtime shared file per run.** Every token is flushed immediately; each agent writes under its own `agent_id` section so teammates read live progress; `Reflector` distills it into the `cognitive` tier.                                            |
| Tool safety          | **Trust-local / ungated** (home-lab). Include an optional **no-op approval hook (default allow)** on `RunPythonTool` so gating can be enabled later without refactoring. ⚠️ Autonomous code execution can be destructive; revisit before any non-local use. |
| Tool-call protocol   | **Both** — native Ollama `/api/chat` tool-calling when supported; **prompted-JSON + robust parser** fallback for small models.                                                                                                                              |
| Logging & search     | **JSONL events + per-run Markdown transcript + SQLite FTS5 index** for full-text search.                                                                                                                                                                    |
| Sequencing           | **Phased** — MVP core agent first, then full tools/reflection, then workflow config, then hardening.                                                                                                                                                        |
| Workflow config      | **JSON (`example.json`) + Python construction**, both via `config/load.py` with delegate inheritance + `schema.json` validation.                                                                                                                            |
| Isolation            | All new code under `src/framework/`. Existing files minimally touched (async `SupabaseVectorStore`, Ollama `/api/chat`).                                                                                                                                    |

---

## 11. Target Package Layout

```
src/framework/
  __init__.py
  ProgressiveAgentSLM.py         # the single recursive agent class: owns context_window, models, reasoning, tools, delegates; runs the progressive loop and recurses into delegates
  AgentConfig.py                 # parsed config: agent_id, description, context_window, max_iterations_untill_give_up, models[], reasoning[], tools[], delegates[] (+ inheritance from parent)
  ContextWindow.py               # four-tier token budget: conversation_awareness / cognitive / context / answering; cascade-on-zero + budget-bounded trimming; auto-infers required model tokens
  ModelChain.py                  # per-agent priority list → first model that fits the budget and is reachable; platform factory (ollama → Ollama, open_router → OpenRouter); max_tokens "auto" sizing
  ReasoningPolicy.py             # renders when → then rules into the system prompt
  ToolRegistry.py                # Tool base + dispatch; each tool carries a `when` guidance string
  agents/
    Reflector.py                 # reflection role: cognitive ← compress(cognitive + context + answer, target=cognitive_tokens); also curates the worklog
    Router.py                    # reads each delegate.description → picks delegate(s) for a sub-question (generalized _parse_agent_routing → delegate:<agent_id>)
  tools/
    SupabaseTool.py              # PRIMARY: pgvector RPC via SupabaseVectorStore.async_query; optional parallel DocumentRanking when ranking=true
    ReadFileTool.py
    GenerateDiagramTool.py       # emits Mermaid for the visualize_diagram policy
    RunPythonTool.py             # wraps tools/PythonCodeExecute; optional approval (default allow)
    FileKnowledgeTool.py         # files-type knowledge source
  logging/
    RunLogger.py                 # owns the run dir; terminal + events.jsonl + transcript.md
    Worklog.py                   # realtime, line-buffered worklog.md (per-agent sections); read()/append() for delegate coordination
    LogSearch.py                 # SQLite FTS5 index (runs/index.db) + search() + CLI
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
- [~] `ModelChain.py`: per-agent priority list → first reachable model that fits the budget; platform factory (`ollama`→`Ollama`, `open_router`→`OpenRouter`); `max_tokens: "auto"` sizing; fall-through on timeout/HTTP error (§4). _(reworks `ModelRegistry`)_
- [x] Make `SupabaseVectorStore` async: `async_query` + `async_get_documents_string` via `httpx.AsyncClient` (sync preserved). _(IMPROVEMENTS.md §2)_
- [~] `logging/RunLogger.py` + `logging/Worklog.py`: run dir + `events.jsonl` + `transcript.md`; **realtime line-buffered** `worklog.md` with per-agent sections + `read()` (§8). _(rework: token-level flush)_

### Phase 1 — Recursive core agent (runnable vertical slice) 🟡

- [~] `AgentConfig.py`: parse `agent_id`, `description`, `context_window`, `max_iterations_untill_give_up` (default 5, `null`→infinite), `models[]`, `reasoning[]`, `tools[]`, `delegates[]`; apply parent→delegate inheritance of `models` / `max_iterations_untill_give_up`.
- [~] `ProgressiveAgentSLM.py`: the single recursive class. Per step — assemble the four-tier prompt, select a model, apply reasoning policies, call tools / route to delegates, emit ≤ `answering_tokens`, then `cognitive ← Reflector.compress(...)` (§3). Recurse into `delegates`; stop at `max_iterations_untill_give_up`.
- [~] `agents/Router.py`: read each delegate's `description`, choose delegate(s) per sub-question via the generalized `_parse_agent_routing` (`delegate:<agent_id>`). _(reworks Forwarder)_
- [~] `agents/Reflector.py`: the cognitive-accumulation compressor (reuse `KnowledgeCompression` + `IterationSummarizer`).
- [~] `ToolRegistry.py` + `tools/SupabaseTool.py` (primary; `function_name` + `ranking`) + `tools/ReadFileTool.py`; each tool carries its `when` guidance.
- [~] Wire `RunLogger` + realtime `Worklog`; `progressive_agent_slm_demo.py` via `create_chat_backend` (port 8001).

### Phase 2 — Full tools, reasoning policies, model routing ⬜

- [ ] Remaining tools: `GenerateDiagramTool` (Mermaid for `visualize_diagram`), `RunPythonTool` (wrap `PythonCodeExecute`, optional approval), `FileKnowledgeTool`.
- [ ] `ReasoningPolicy.py`: render `when → then` rules into the system prompt; ship the baseline set (deep_think, double_check, visualize_diagram, say_no).
- [ ] Supabase ranking path: parallel `DocumentRanking` batches (reuse `RagAssistant.stream`) when `ranking: true`.
- [ ] Budget enforcement: measure tokens (tokenizer or char-approx), trim each tier to budget, implement cascade-on-zero donation.
- [ ] `logging/LogSearch.py`: SQLite FTS5 index (`runs/index.db`) + search + CLI over all runs.

### Phase 3 — Config loader (JSON + Python) ⬜

- [ ] `config/load.py` + `config/schema.json`: build a `ProgressiveAgentSLM` tree from `example.json` (or a Python dict) with validation + delegate inheritance.
- [ ] Round-trip the canonical `example.json` (§13) end-to-end as a worked example + regression check; authoring README.

### Phase 4 — Hardening ⬜

- [ ] Unit tests: config loader/inheritance, four-tier budgeting + cascade, cognitive compaction, router parser, Supabase tool, Worklog realtime append/read, RunLogger JSONL+FTS round-trip.
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

  "context_window": {
    "conversation_awareness_tokens": 800,
    "cognitive_tokens": 7200,
    "context_tokens": 24000,
    "answering_tokens": 9200
  },
  "max_iterations_untill_give_up": 5,

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
      "when": "The user references a specific local file needed to answer."
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

The two delegates omit `models` and `max_iterations_untill_give_up`, so they **inherit** them from the parent. Budgets sum to 41,200 / 43,500 / 59,500 tokens respectively — all within the local model's 62,000 ceiling.

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
    context_window=dict(conversation_awareness_tokens=800, cognitive_tokens=7200,
                        context_tokens=24000, answering_tokens=9200),
    max_iterations_untill_give_up=5,
    models=[
        dict(platform="ollama", name="gpt-oss:20b", url="http://localhost:11434", max_tokens=62000),
        dict(platform="open_router", name="anthropic/claude-3.5-sonnet", max_tokens="auto"),
    ],
    reasoning=[
        dict(id="deep_think",   when="The question is complex.",            then="Decompose and route to delegate(s)/tool(s)."),
        dict(id="double_check", when="All delegates/tools have returned.",   then="Verify; re-iterate if gaps remain."),
        dict(id="say_no",       when="No answer after exhausting sources.",  then="Say so honestly; never invent."),
    ],
    tools=[dict(type="ReadFileTool", when="A referenced local file is needed.")],
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

> A delegate that omits `models` / `max_iterations_untill_give_up` inherits the parent's. The agent
> streams every token into the run's realtime `worklog.md` (§8), so the two delegates can read each
> other's in-progress work under their own `agent_id` sections.

---

## 14. Key Reuse Map (concrete)

| Existing asset                                                   | Reused for                                                                              |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `AssistantOrchestra.stream`                                      | `ProgressiveAgentSLM` per-step loop (route → execute → accumulate → reflect → iterate)  |
| `AssistantOrchestra._parse_agent_routing` / `_parse_eval_result` | `Router` delegate selection (`delegate:<agent_id>`) + double-check evaluation parsing   |
| `AssistantOrchestra.add_agent` / `agents` registry               | The recursive `delegates` registry (each keyed by `agent_id` + `description`)           |
| `all_agent_responses` + `IterationSummarizer` compaction         | Seed for the **cognitive** tier + the realtime **worklog**                              |
| `KnowledgeCompression`, `IterationSummarizer`                    | `Reflector.compress` — the `cognitive ← compress(cognitive+context+answer)` accumulator |
| `RagAssistant.stream` (parallel `DocumentRanking` batches)       | `SupabaseTool` ranking path (`ranking: true`)                                           |
| `SupabaseVectorStore.async_query`                                | `SupabaseTool` — the primary capability                                                 |
| `Task` + DI-kwargs pattern                                       | `Router`, `Reflector` agents                                                            |
| `AnswerEvaluator`, `FinalThoughtSummarizer`                      | `double_check` policy + final recap from the worklog                                    |
| `PythonCodeExecute`                                              | `RunPythonTool` (optional approval, default allow)                                      |
| `Ollama` (`/api/generate`) / `OpenRouter` (429 backoff)          | The per-agent `models` chain via the platform factory (local-first, cloud fallback)     |
| `ChatBackend.create_chat_backend`                                | Unchanged streaming integration point                                                   |

---

## 15. Verification

1. **Unit**: config loader + delegate inheritance, four-tier budgeting (trim + cascade-on-zero + auto token inference), `cognitive ← compress(...)` accumulation, `Router` selection parser, `SupabaseTool`, realtime `Worklog` append/read, `RunLogger` JSONL+FTS round-trip.
2. **Integration smoke**: load `example.json` with a stub model — assert the tree builds, the parent routes to a delegate, the delegate calls its Supabase tool and writes under its own `agent_id` section, `cognitive` grows yet stays ≤ its budget, and `worklog.md` + `events.jsonl` + `transcript.md` exist and FTS search returns the run.
3. **Manual**: launch `progressive_agent_slm_demo.py` via uvicorn, ask a multi-step BVMS question, confirm streamed think/route/delegate/answer, realtime worklog flushing, and on-disk logs searchable via the `LogSearch` CLI.
4. **Budget**: assert no request exceeds the selected model's `max_tokens`, and that a delegate omitting `models` inherits the parent's chain.

---

## 16. Open Questions

| #   | Question                                                                                 | Recommendation                                                                 | Decision   |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------- |
| 1   | Recursion — is every delegate a full `ProgressiveAgentSLM`?                              | Yes; core to the design. Bound depth via `max_iterations_untill_give_up`.      | ✅ Decided |
| 2   | Token measurement for budgeting — real per-model tokenizer, or char≈token approximation? | Char-approx (reuse `CHARS_PER_TOKEN`) for P1; pluggable tokenizer in P2.       | _TBD_      |
| 3   | Cognitive compaction timing — after every step, or only when over budget?                | Every step, but skip the compress call when already under budget (cost saver). | _TBD_      |
| 4   | Cascade-on-zero — does a 0 tier donate to the next tier only, or pool across all tiers?  | Donate to the immediate next tier (awareness→cognitive, context→answering).    | _TBD_      |
| 5   | Reflection write-back for durable facts — Supabase table, or local file KB?              | Local file KB first (no migration); Supabase table later.                      | _TBD_      |

---

## 17. Logging Artifacts & Event Schema

Four artifacts per run (see §8):

- **`worklog.md`** — the **realtime**, line-buffered shared narrative; one `## <agent_id>` section per agent, flushed token-by-token so delegates can read teammates' in-progress work.
- **`events.jsonl`** — append-only structured event stream (schema below).
- **`transcript.md`** — full verbatim human-readable rendering.
- **`runs/index.db`** — SQLite FTS5 index over all events for `LogSearch`.

Each JSONL event line:

```json
{
  "run_id": "uuid",
  "ts": "ISO-8601",
  "agent_id": "agent_id of the emitter (or 'root')",
  "phase": "route | act | observe | reflect | delegate | worklog | final",
  "actor": "router | reflector | tool:NAME | delegate:<agent_id>",
  "tier": "conversation_awareness | cognitive | context | answering | n/a",
  "input": "prompt / action args (truncated)",
  "output": "result chunk / summary (truncated)",
  "status": "ok | error | skipped",
  "tokens": 0
}
```

`worklog.md` is the realtime working narrative; `cognitive` (in-memory, per agent) is its compressed
distillation; `transcript.md` is the verbatim rendering; `runs/index.db` indexes all events via
SQLite FTS5 for `LogSearch`.

---

_Last updated: 2026-06-09_
