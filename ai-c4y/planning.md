# Capability Agent Framework — Planning & Progress Tracker

> Build a **full, customizable agentic-workflow framework optimized for local & small language
> models (SLMs)** — yet highly extensible so any step can be swapped, plug-and-play, for a more
> capable **cloud** model when needed (current cloud provider: **OpenRouter**).
>
> Users declare a **ProgressiveAgentSLM**: it takes a goal, plans a sub-task DAG, delegates each node to
> small local LLMs / sub-agents / tools (following the existing `AssistantOrchestra` delegation
> style), reflects after every step to keep context small, and records each delegate's **compact**
> answer into a single shared **worklog** that reflection keeps revised and current.
>
> It reuses existing primitives (`Task`, model clients, `SupabaseVectorStore`, `PythonCodeExecute`,
> `KnowledgeCompression`, `IterationSummarizer`, `AnswerEvaluator`, `FinalThoughtSummarizer`) and
> drops into `create_chat_backend` unchanged.

**Status legend:** ⬜ Not started · 🟡 In progress · ✅ Done · ⛔ Blocked

---

## 1. Vision & Design Philosophy

- **Local & SLM-first.** Default every role to a small/local Ollama model so the whole workflow runs on home-lab hardware. Small models do the cheap, frequent work (routing, planning, reflection, tool calls); quality comes from decomposition + reflection rather than one giant model.
- **Plug-and-play cloud escalation.** Any role/step can be swapped for a more capable cloud model (OpenRouter) by changing one config value — no code change. `ModelRegistry` makes model choice a per-role setting with a local→cloud fallback chain.
- **Reuse, don't rebuild.** Follow the existing philosophy: async streaming generators that `yield` chunks, DI via constructor kwargs, `Task`-subclass agents driven by `instruction_template`, prompt-based JSON protocols with robust regex fallbacks, and JSON-file state like the `cia_phase*` workflows. New code lives under `src/framework/`; existing files are touched minimally.
- **Delegation like `AssistantOrchestra`.** Keep the proven route → execute → accumulate → evaluate → iterate/compact → final-recap loop, generalized from "agents only" to "agents + tools + knowledge", and persist the accumulator to a shared worklog file.
- **Everything observable.** Every step streams live (`<think>` blocks) and is written to disk (worklog + event log + transcript) for full-text search later.

---

## 2. Goals → Components

| Goal (user)                                                                                               | Realized by                                                                  |
| --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Framework to design/customize a strong capability agent                                                   | `AgentConfig` + `ProgressiveAgentSLM` + `WorkflowBuilder` / `WorkflowSpec`   |
| **Goal**: focus on achieving the user-set goal                                                            | `Planner` + evaluate/re-plan loop (reuse `AnswerEvaluator`)                  |
| **Knowledge**: text files + Supabase vector DB                                                            | `KnowledgeProvider` → `FileKnowledge`, `SupabaseKnowledge`                   |
| **Tools**: terminal, write code, execute function, read file                                              | `ToolRegistry` + `tools/` (Terminal, RunPython, WriteFile, Function, Read)   |
| **Reflection**: summarize during work, avoid overflow, save to KB                                         | `Reflector` (reuse `KnowledgeCompression` + `IterationSummarizer`) + persist |
| **Delegate**: break task into steps/sub-agents, collect results                                           | Plan DAG + bounded ReAct per node + sub-agent dispatch                       |
| **Worklog**: one shared file every delegate writes a compact answer into, revised by reflection each step | `Worklog` + `Reflector` (persisted evolution of `all_agent_responses`)       |
| Local/SLM-first with plug-and-play cloud escalation (OpenRouter)                                          | `ModelRegistry` (per-role model + local→cloud fallback)                      |
| Per-step logging to terminal + files for full-text search                                                 | `RunLogger` (JSONL + Markdown) + `LogSearch` (SQLite FTS5)                   |
| Workflow configurable via JSON **and** Python                                                             | `WorkflowSpec` (declarative DAG + `schema.json`) + `WorkflowBuilder`         |

---

## 3. Design Decisions

| Topic              | Decision                                                                                                                                                                                                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Control-flow style | **Hybrid** — plan a sub-task DAG upfront, execute each node with bounded ReAct + reflection, re-plan only on step failure or unsatisfied evaluator.                                                                                                                                   |
| Delegation         | **Follow `AssistantOrchestra`** — `agents` registry (`name → {agent, description, context_awareness}`), JSON routing, sequential execution accumulating into the worklog; generalized to also delegate to **tools** and **knowledge**.                                                |
| Models (defaults)  | **Local/SLM-first**: `gemma4:e4b` chat · `gpt-oss:20b` reflection · `qwen3.6:27b` reasoning/coding/tool-use. Any role swappable to **OpenRouter** cloud.                                                                                                                              |
| Worklog            | **One shared main file per run.** Every agent/sub-agent/tool writes a **compact** answer; `Reflector` revises/compacts it **every step** to prevent overflow and keep the KB current.                                                                                                 |
| Tool safety        | **Trust-local / ungated** (home-lab). Include an optional **no-op approval hook (default allow)** on `TerminalTool`/`RunPythonTool` so gating can be enabled later without refactoring. ⚠️ Autonomous terminal + code execution can be destructive; revisit before any non-local use. |
| Tool-call protocol | **Both** — native Ollama `/api/chat` tool-calling when supported; **prompted-JSON + robust parser** fallback for small models.                                                                                                                                                        |
| Logging & search   | **JSONL events + per-run Markdown transcript + SQLite FTS5 index** for full-text search.                                                                                                                                                                                              |
| Sequencing         | **Phased** — MVP core agent first, then full tools/reflection, then workflow config, then hardening.                                                                                                                                                                                  |
| Workflow config    | **Declarative DAG JSON** (agents, tools, knowledge, steps, deps) **+ Python builder escape hatch** for conditionals/loops.                                                                                                                                                            |
| Isolation          | All new code under `src/framework/`. Existing files minimally touched (async `SupabaseVectorStore`, Ollama `/api/chat`).                                                                                                                                                              |

---

## 4. Model Roles & Defaults

`ModelRegistry` maps a **role** → an ordered **fallback chain** (first available wins; on timeout/HTTP error it falls through — local first, cloud as backstop). Defaults:

| Role         | Default (local) | Used by                                                     | Cloud escalation (OpenRouter) |
| ------------ | --------------- | ----------------------------------------------------------- | ----------------------------- |
| `chat`       | `gemma4:e4b`    | forwarder/router, light chat, final recap                   | any chat model                |
| `reflection` | `gpt-oss:20b`   | `Reflector`, `KnowledgeCompression`, `IterationSummarizer`  | any knowledge model           |
| `reasoning`  | `qwen3.6:27b`   | `Planner`, `StepExecutor`, coding, **tool use**, evaluation | a stronger reasoning model    |

```python
# Conceptual default registry (Phase 0)
MODEL_REGISTRY = {
    "chat":       [Ollama(model="gemma4:e4b")],
    "reflection": [Ollama(model="gpt-oss:20b")],
    "reasoning":  [Ollama(model="qwen3.6:27b")],
    # Per-role cloud escalation is opt-in, e.g.:
    # "reasoning": [Ollama(model="qwen3.6:27b"), OpenRouter(model="anthropic/claude-3.5-sonnet")],
}
```

Any role can be overridden per-agent in config (JSON or Python) — that is the plug-and-play cloud-escalation mechanism.

---

## 5. Delegation Model — follows `AssistantOrchestra`

The core loop generalizes `AssistantOrchestra.stream` from "route to agents" to "route to **agents, tools, and knowledge**", preserving its structure and streaming behavior:

1. **Register delegates.** `agents` registry keyed by name → `{agent, description, context_awareness}` (today's shape via `add_agent`). Tools and knowledge register the same way (`tool:NAME`, `knowledge:NAME`).
2. **Plan / route.** A forwarder/planner streams reasoning inside `<think>` and ends with a JSON block (`[{"agent": "...", "question": "..."}]`), parsed by the proven `_parse_agent_routing` pattern.
3. **Execute each delegate sequentially.** A `context_awareness: true` delegate receives the **worklog** as context (today this is the raw `all_agent_responses`).
4. **Accumulate into the worklog.** Each delegate's compact output is appended; reflection compacts it.
5. **Evaluate.** `AnswerEvaluator` decides `satisfied` / `follow_up`; loop up to `max_iterations`, compacting via `IterationSummarizer` past `compact_threshold`.
6. **Final recap.** `FinalThoughtSummarizer` recaps when more than one delegate contributed.

> Key change vs today: the in-memory `all_agent_responses` becomes a **persisted, reflection-curated worklog file** (§6), and delegates can be tools/knowledge, not just agents.

---

## 6. The Worklog — shared compact memory

A single **main worklog file per run** (`runs/<run_id>/worklog.md`) is the agent's curated working memory and the heart of delegation + reflection.

- **Every delegate writes a compact answer.** After an agent / sub-agent / tool finishes its responsibility, it appends a **concise** summary of _its_ result (not a raw dump) under its own section — the deliverable for that step.
- **Reflection revises it every step.** After each step the `Reflector` (`gpt-oss:20b`) rewrites/compacts the worklog so it stays small, non-redundant, and current — preventing context overflow. This is the persisted evolution of `all_agent_responses` + `IterationSummarizer` compaction already in `AssistantOrchestra`.
- **It is the shared context.** Context-aware delegates read the worklog (not the full transcript), so each sub-agent gets a tight, relevant briefing.
- **It seeds the final answer & KB.** The final recap is built from the worklog; durable facts can be persisted back to the knowledge base (`KnowledgeProvider.persist`).

```
runs/<run_id>/
  worklog.md       # ← the single shared, compact, reflection-revised main file (this section)
  events.jsonl     # append-only raw event stream (every think/act/observe/delegate)
  transcript.md    # full human-readable rendering (verbatim)
# runs/index.db    # SQLite FTS5 index over all runs' events (full-text search)
```

---

## 7. Target Package Layout

```
src/framework/
  __init__.py
  AgentConfig.py                 # dataclass: goal, knowledge[], tools[], sub_agents, reflection cfg, model roles, limits
  ProgressiveAgentSLM.py         # core hybrid loop: plan → exec → reflect(worklog) → evaluate → re-plan → final
  ModelRegistry.py               # role → model + fallback chain; defaults gemma4:e4b / gpt-oss:20b / qwen3.6:27b (local → OpenRouter)
  StepExecutor.py                # per-node bounded ReAct: think → action → observe → repeat
  ToolRegistry.py                # Tool protocol + dispatch (native + prompted tool-calls)
  Worklog.py                     # shared compact worklog file: append(section, compact), read(), revise via Reflector
  agents/
    Planner.py                   # Task subclass → emits sub-task DAG as JSON (reasoning role)
    Forwarder.py                 # routing/delegation a la QuestionForwarder (chat role) — agents + tools + knowledge
    Reflector.py                 # wraps KnowledgeCompression + IterationSummarizer; revises worklog + KB write-back (reflection role)
  tools/
    ReadFileTool.py
    WriteFileTool.py
    RunPythonTool.py             # wraps tools/PythonCodeExecute
    WriteCodeTool.py
    TerminalTool.py              # new shell exec; optional approval hook (default allow)
    ExecuteFunctionTool.py       # call a registered Python callable
    VectorSearchTool.py          # wraps SupabaseVectorStore
    FileKnowledgeTool.py
  knowledge/
    KnowledgeProvider.py         # base: async search(query, k) -> chunks; async persist(fact, meta)
    FileKnowledge.py             # FileHanlder split + keyword/embedding search
    SupabaseKnowledge.py         # SupabaseVectorStore + parallel DocumentRanking (from RagAssistant)
  logging/
    RunLogger.py                 # terminal + runs/<run_id>/{events.jsonl, transcript.md}; owns the Worklog
    LogSearch.py                 # SQLite FTS5 index (runs/index.db) + search() + CLI
  workflow/
    WorkflowSpec.py              # JSON loader: load_workflow(path|dict) -> AgentConfig/Workflow + validation
    WorkflowBuilder.py           # Python fluent API + escape hatch (mirrors AssistantOrchestra.add_agent)
    schema.json                  # JSON schema for validation
    examples/                    # example workflow JSON files

progressive_agent_slm_demo.py    # entry point: compose ProgressiveAgentSLM + create_chat_backend + uvicorn (port 8001)
```

---

## 8. Phases & Tasks

### Phase 0 — Foundation primitives ⬜

Unblocks meaningful small-model use (cheap roles local, cloud as backstop).

- [ ] `ModelRegistry.py`: role→model map (planner/executor/reflector/ranking/generation) with fallback chain; local→cloud failover on timeout/HTTP error. _(IMPROVEMENTS.md §4a)_
- [ ] Make `SupabaseVectorStore` async: swap `requests` → `httpx.AsyncClient`. _(IMPROVEMENTS.md §2)_
- [ ] `RunLogger.py` skeleton: terminal echo + `runs/<run_id>/events.jsonl` + `runs/<run_id>/transcript.md`.
- [ ] `Worklog.py` skeleton: create/append compact sections + read; owned by `RunLogger`.

### Phase 1 — MVP core agent (runnable vertical slice) ⬜

Goal: end-to-end stream that plans, delegates to one existing RAG sub-agent, reflects, logs.

- [ ] `AgentConfig.py` dataclass (goal, knowledge[], tools[], sub*agents, reflection cfg, model roles, limits: `max_steps`, `max_react_iters`, `compact_threshold`). *(deps: ModelRegistry)\_
- [ ] `agents/Forwarder.py` + `agents/Planner.py`: routing/delegation a la `QuestionForwarder` (chat role) + DAG planner (reasoning role) emitting nodes `{id, description, assignee(self|tool:NAME|agent:NAME|knowledge:NAME), depends_on[], done_when}`; robust JSON parser (pattern from `_parse_agent_routing`).
- [ ] `ProgressiveAgentSLM.py`: hybrid loop modeled on `AssistantOrchestra.stream` (route → execute → accumulate into worklog → reflect → evaluate → re-plan/stop → final). Reuse `AnswerEvaluator` + `FinalThoughtSummarizer`. _(deps: AgentConfig, Forwarder/Planner, Worklog)_
- [ ] `ToolRegistry.py` + minimal `tools/ReadFileTool.py`, `tools/VectorSearchTool.py` (Tool protocol: `name`, `description`, `parameters` JSON schema, `async run`). _(deps: async SupabaseVectorStore)_
- [ ] `agents/Reflector.py`: wrap `KnowledgeCompression` + `IterationSummarizer`; compact working memory past `compact_threshold` (reuse compaction trigger from `AssistantOrchestra.stream`).
- [ ] Wire `RunLogger` + `Worklog` through every phase; add `progressive_agent_slm_demo.py` using `create_chat_backend`. Register an existing `RagAssistant` as a sub-agent to prove delegation. _(deps: RunLogger, ProgressiveAgentSLM, ToolRegistry, Reflector)_

### Phase 2 — Full tools, reflection write-back, model routing ⬜

- [ ] Tools: `TerminalTool` (new shell; optional approval hook, default allow), `RunPythonTool`/`WriteCodeTool` (wrap `PythonCodeExecute`), `WriteFileTool`, `ExecuteFunctionTool`.
- [ ] `StepExecutor.py` tool-call protocol: native Ollama `/api/chat` tools when supported (extend `Ollama`), prompted-JSON fallback otherwise.
- [ ] `knowledge/`: `KnowledgeProvider` base + `FileKnowledge` (via `FileHanlder`) + `SupabaseKnowledge` (reuse parallel `DocumentRanking` batches from `RagAssistant.stream`); reflection KB write-back (`persist`) from the worklog.
- [ ] Parallel execution of independent DAG nodes (`asyncio.gather`). _(IMPROVEMENTS.md §3a)_
- [ ] Complexity-based model routing in `ModelRegistry` (escalate hard steps to OpenRouter cloud).
- [ ] `logging/LogSearch.py`: SQLite FTS5 index (`runs/index.db`) + search + CLI over all runs.

### Phase 3 — Workflow configuration (JSON + Python) ⬜

- [ ] `workflow/WorkflowSpec.py` + `schema.json`: declarative DAG loader `load_workflow(path|dict)` with validation + `examples/`.
- [ ] `workflow/WorkflowBuilder.py`: Python fluent API + escape hatch (mirrors `add_agent`).
- [ ] Port `rag_orchestra.py` to an equivalent JSON workflow as a worked example + regression check; add authoring README.

### Phase 4 — Hardening ⬜

- [ ] Unit tests: plan/eval parsers, tool dispatch, workflow loader/validator, Worklog append/revise, RunLogger JSONL+FTS round-trip.
- [ ] Integration smoke test with a stub model implementing `.stream`.
- [ ] Timeouts/retries (reuse 429/retry pattern from `OpenRouter`).
- [ ] Optional safety hook wired (default allow) on terminal/code tools.

---

## 9. Example: Configuring an Agentic Workflow (when finished)

The same workflow can be expressed in **JSON** (declarative) or **Python** (fluent + escape hatch). Both build an equivalent `ProgressiveAgentSLM` and drop into `create_chat_backend`.

### 9a. JSON (declarative DAG)

```json
{
  "name": "bvms-assistant",
  "goal": "Answer BVMS questions accurately using domain + code knowledge, with diagrams when useful.",
  "models": {
    "chat": "gemma4:e4b",
    "reflection": "gpt-oss:20b",
    "reasoning": "qwen3.6:27b"
  },
  "limits": {
    "max_steps": 6,
    "max_react_iters": 3,
    "compact_threshold_tokens": 24000
  },
  "knowledge": [
    {
      "name": "bvms-docs",
      "type": "supabase",
      "function_name": "match_n8n_documents_bvms_neo",
      "rank": true
    },
    { "name": "local-notes", "type": "files", "path": "docs/bvms" }
  ],
  "tools": [
    { "name": "read_file", "type": "ReadFileTool" },
    { "name": "run_python", "type": "RunPythonTool", "approval": false }
  ],
  "agents": {
    "BVMS-General": {
      "type": "RagAssistant",
      "context_awareness": true,
      "query_function_name": "match_n8n_documents_bvms_neo",
      "description": "Business workflow & domain knowledge about BVMS.",
      "model_role": "chat"
    },
    "BVMS-Code": {
      "type": "RagAssistant",
      "context_awareness": true,
      "query_function_name": "match_n8n_documents_bvms_code",
      "description": "Deep technical/code aspects of BVMS.",
      "model_role": "reasoning"
    }
  },
  "plan": [
    {
      "id": "domain",
      "assignee": "agent:BVMS-General",
      "description": "Gather business/domain context",
      "depends_on": []
    },
    {
      "id": "code",
      "assignee": "agent:BVMS-Code",
      "description": "Get technical/code detail",
      "depends_on": ["domain"]
    },
    {
      "id": "recap",
      "assignee": "self",
      "description": "Synthesize the final answer from the worklog",
      "depends_on": ["domain", "code"]
    }
  ],
  "reflection": {
    "enabled": true,
    "every_step": true,
    "persist_to_kb": "bvms-docs"
  },
  "escalation": { "reasoning": "anthropic/claude-3.5-sonnet" }
}
```

```python
# Run a JSON-configured workflow
from src.framework.workflow.WorkflowSpec import load_workflow
from src.ChatBackend import create_chat_backend
import uvicorn

assistant = load_workflow("src/framework/workflow/examples/bvms-assistant.json")
if __name__ == "__main__":
    uvicorn.run(create_chat_backend(assistant), host="0.0.0.0", port=8001, timeout_keep_alive=300)
```

### 9b. Python (fluent builder + escape hatch)

```python
from src.framework.workflow.WorkflowBuilder import WorkflowBuilder
from src.framework.ModelRegistry import ModelRegistry
from src.framework.tools import ReadFileTool, RunPythonTool
from src.framework.knowledge import SupabaseKnowledge
from src.agents.models.Ollama import Ollama
from src.agents.models.OpenRouter import OpenRouter
from rag_chat_bvms import bvms_rag_assistant
from rag_chat_bvms_code import bvms_code_rag_assistant

models = ModelRegistry(
    chat=[Ollama(model="gemma4:e4b")],
    reflection=[Ollama(model="gpt-oss:20b")],
    # plug-and-play cloud escalation: local first, OpenRouter as backstop
    reasoning=[Ollama(model="qwen3.6:27b"), OpenRouter(model="anthropic/claude-3.5-sonnet")],
)

assistant = (
    WorkflowBuilder(goal="Answer BVMS questions accurately using domain + code knowledge.")
        .with_models(models)
        .with_limits(max_steps=6, max_react_iters=3, compact_threshold_tokens=24000)
        .add_knowledge(SupabaseKnowledge("match_n8n_documents_bvms_neo", rank=True), name="bvms-docs")
        .add_tool(ReadFileTool())
        .add_tool(RunPythonTool(approval=False))
        # delegation registry — same shape as AssistantOrchestra.add_agent
        .add_agent("BVMS-General", "Business workflow & domain knowledge about BVMS.", bvms_rag_assistant, context_awareness=True)
        .add_agent("BVMS-Code", "Deep technical/code aspects of BVMS.", bvms_code_rag_assistant, context_awareness=True)
        .with_reflection(every_step=True, persist_to_kb="bvms-docs")
        .build()
)

# Escape hatch: drop to a raw async step for control flow JSON can't express
@assistant.step(after="code", id="custom-check")
async def verify(ctx):
    if "ERROR" in ctx.worklog.read():
        await ctx.delegate("agent:BVMS-Code", "Resolve the flagged error and update the worklog.")

if __name__ == "__main__":
    import uvicorn
    from src.ChatBackend import create_chat_backend
    uvicorn.run(create_chat_backend(assistant), host="0.0.0.0", port=8001, timeout_keep_alive=300)
```

> Both paths build the same `ProgressiveAgentSLM`; JSON covers the common declarative DAG, while the Python builder adds an escape hatch for conditionals/loops — mirroring how `rag_orchestra.py` wires `AssistantOrchestra` today.

---

## 10. Key Reuse Map (concrete)

| Existing asset                                                   | Reused for                                                                           |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `AssistantOrchestra.stream`                                      | `ProgressiveAgentSLM` route/execute/accumulate/evaluate/compact/recap loop           |
| `AssistantOrchestra._parse_agent_routing` / `_parse_eval_result` | Plan-DAG parser + evaluator parser                                                   |
| `AssistantOrchestra.add_agent` / `agents` registry               | Delegate registry (agents + tools + knowledge)                                       |
| `all_agent_responses` + `IterationSummarizer` compaction         | The persisted, reflection-revised **worklog**                                        |
| `RagAssistant.stream` (parallel `DocumentRanking` batches)       | `SupabaseKnowledge.search`                                                           |
| `Task` + DI-kwargs pattern                                       | `Planner`, `Forwarder`, `Reflector` agents                                           |
| `KnowledgeCompression`, `IterationSummarizer`                    | `Reflector` compaction + KB write-back                                               |
| `AnswerEvaluator`, `FinalThoughtSummarizer`                      | Goal evaluation + final recap                                                        |
| `PythonCodeExecute`                                              | `RunPythonTool`                                                                      |
| `SupabaseVectorStore`                                            | `SupabaseKnowledge` + reflection `persist`                                           |
| `Ollama` (`/api/generate`)                                       | `ModelRegistry` local defaults + OpenRouter cloud escalation; `/api/chat` tool-calls |
| `ChatBackend.create_chat_backend`                                | Unchanged streaming integration point                                                |
| `cia_phase*` manifest/checkpoint pattern                         | Resumable run state (Phase 2+)                                                       |

---

## 11. Verification

1. **Unit**: plan-DAG parser, eval parser, tool-registry dispatch, JSON workflow validator, `RunLogger` JSONL+FTS write/search round-trip.
2. **Integration smoke**: run `ProgressiveAgentSLM` on a canned goal with a stub model — assert a plan is produced, a sub-agent + a tool are called, each writes a **compact worklog entry**, reflection revises the worklog, and `worklog.md` + `events.jsonl` + `transcript.md` exist and FTS search returns the run.
3. **Manual**: launch `progressive_agent_slm_demo.py` via uvicorn, ask a multi-step BVMS question, confirm streamed think/plan/delegate/answer plus on-disk logs searchable via the `LogSearch` CLI.
4. **Regression**: the JSON port of `rag_orchestra` behaves comparably to the original.

---

## 12. Open Questions

| #   | Question                                                                               | Recommendation                                            | Decision |
| --- | -------------------------------------------------------------------------------------- | --------------------------------------------------------- | -------- |
| 1   | Run-state persistence depth — full `cia_phase*` manifest/checkpoint, or in-memory MVP? | In-memory for P1; add resumable manifest in P2.           | _TBD_    |
| 2   | Reflection write-back target — dedicated Supabase table, or local file KB?             | Local file KB first (no migration); Supabase table in P2. | _TBD_    |
| 3   | Sub-agent reuse vs recursion — can a sub-agent be another full `ProgressiveAgentSLM`?  | Allow recursion, cap depth via `max_steps`.               | _TBD_    |

---

## 13. Logging Artifacts & Event Schema

Four artifacts per run (see §6):

- **`worklog.md`** — curated, compact, reflection-revised shared memory (each delegate's deliverable).
- **`events.jsonl`** — append-only raw event stream (schema below).
- **`transcript.md`** — full verbatim human-readable rendering.
- **`runs/index.db`** — SQLite FTS5 index over all events for `LogSearch`.

Each JSONL event line:

```json
{
  "run_id": "uuid",
  "ts": "ISO-8601",
  "step_id": "node id or 'root'",
  "phase": "plan | act | observe | reflect | delegate | worklog | final",
  "actor": "planner | forwarder | executor | reflector | tool:NAME | agent:NAME",
  "input": "prompt / action args (truncated)",
  "output": "result chunk / summary (truncated)",
  "status": "ok | error | skipped",
  "tokens": 0
}
```

`worklog.md` is the compact curated memory; `transcript.md` is the verbatim rendering;
`runs/index.db` indexes all events via SQLite FTS5 for `LogSearch`.

---

_Last updated: 2026-06-08_
