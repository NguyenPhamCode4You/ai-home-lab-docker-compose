# ProgressiveAgentSLM

> **A single, recursive agent class tuned for local / small language models (SLMs).**
> It reasons like a senior expert through **disciplined and cultivated context of experience — not a
> bigger LLM**. This is the project's new home.

## What it is

`ProgressiveAgentSLM` is a recursive agent harness for **local/SLM-first, domain-expert reasoning**. One
instance owns a context budget, a role-tagged model ladder, hook-driven behavior policies, tools,
cultivated memory stores, and delegates (which are themselves `ProgressiveAgentSLM` instances). It
**progressively cultivates knowledge**: every iteration's raw reasoning is appended to an append-only
raw log (L1) and distilled into derived `memory_data_stores` (L2/L3) — so a _small_ local model stays
expert through disciplined memory handling, not by being big.

See [`planning/design-principle.md`](planning/design-principle.md) for the _why_ and
[`planning/planning.md`](planning/planning.md) for the full design.

## Project layout

```
ProgressiveAgentSLM/
  progressive_agent_slm_demo.py   # entry: load example-revised.json → serve on 8001
  src/
    agents/models/                # Ollama, OpenRouter (async stream() interface)
    framework/                    # the recursive agent + all primitives
      ProgressiveAgentSLM.py      #   the single recursive agent class
      AgentConfig.py              #   parsed §2 config + delegate inheritance
      ContextWindow.py            #   3-window percentage budget (§3)
      ModelChain.py               #   role-tagged models_ladder + failover (§4)
      CircularRounds.py           #   total-work budget (beat Hermes iteration_budget.py)
      BehaviorPolicies.py         #   when→then policies fired on run_after hooks (§5)
      ToolRegistry.py             #   Tool base + dispatch
      ParallelExecutor.py         #   bounded fan-out (parallel_subprocesses)
      bounded_io.py               #   byte + deadline bounded reads (Hermes port)
      redact.py                   #   egress secret redaction (Hermes port)
      agents/                     #   Router, Reflector, Guards
      tools/                      #   safety.py, ReadFileTool, TodoTool, Sqlite/Jsonl query
      delegates/contracts.py      #   typed immutable delegate boundary
      guards/                     #   tool_loop, verify_on_stop
      memory/                     #   RawLog, MemoryStore(s), Distiller, LogSearch, RunLogger
      modes/                      #   AssistantMode, ResearchMode, (ReflectionMode…)
      config/load.py              #   JSONC loader → recursive tree
      example-revised.json        #   the canonical bvms-assistant config
  tests/framework/                #   pytest suite (green from day one)
  planning/                       #   the design docs + WIP tracker
```

## Quick start

```bash
pip install -e ".[dev]"
python progressive_agent_slm_demo.py   # serves on :8001
pytest -q                              # test suite
```

The demo loads `src/framework/example-revised.json` (a JSONC config), builds the full recursive
`bvms-assistant` tree (with its `bvms-code-analyzer` delegate), and serves it through `create_chat_backend`.

## WIP tracker

The execution plan is [`planning/wip_checklist.md`](planning/wip_checklist.md) — 100 todos across
Phases 0–4, each with "read / do / validate". The design is in [`planning/planning.md`](planning/planning.md);
the Hermes porting map is [`planning/steal-list-hermes.md`](planning/steal-list-hermes.md).

> **Status (2026-08-12):** scaffolding complete — the project folder, package layout, planning home,
> Hermes ports (bounded I/O, CircularRounds, safety, redact, guards, contracts), the config loader
> (JSONC → tree), and a green-from-day-one test suite. Phases 0–4 core algorithms are the next checkpoint.
