# Phase 0 — Orientation Scratch Notes

> Items 1 + 2 deliverables. Updated as new primitives are confirmed.

---

## Item 1 — Data-flow + four-file ownership

| File                    | Scope     | Written by                    | One sentence                                                                                                                                                           |
| ----------------------- | --------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `raw_worklog.jsonl`     | shared    | one serialized writer per run | Every finished block from every agent/delegate appended forever as one JSON record per line (keyed by `block_id`) — the single source of truth everyone loops back to. |
| `cognitive_index.jsonl` | shared    | the same writer               | One ~10–20-token pointer record per block, joined to `raw_worklog.jsonl` by `block_id` — the searchable map used to pull only relevant blocks into a working window.   |
| `context_window.log`    | per-agent | the owning agent              | The agent's current working set of blocks retrieved from `raw_worklog` via the index; compacted to 50 % when it exceeds the `current_working_attention` budget.        |
| `response_window.log`   | per-agent | the owning agent              | The agent's latest answer only; flushed whole to `raw_worklog` + `cognitive_index`, then cleared for the next iteration.                                               |

Data-flow direction:

```
question
  → cognitive_index.search(question)
    → raw_worklog.fetch(block_ids)
      → context_window.log  (working set for this step)
        → response_window.log  (answer for this iteration)
          → raw_worklog.append(block)  +  cognitive_index.append(pointer)
            → response_window cleared
```

---

## Item 2 — Inventory: keep / rework / replace

| File                                   | Decision                                      | Reason                                                                                                                                                                                                                     |
| -------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/framework/ModelRegistry.py`       | **Replace → `ModelChain.py`**                 | Role-based registry; target is a per-agent ordered ladder with per-model retry budget + success-reset + platform factory. Nothing to reuse from the old design.                                                            |
| `src/framework/Worklog.py`             | **Rework → `logging/Worklog.py` coordinator** | Old design: one `worklog.md` rewritten by Reflector. New: coordinator for four append-only files behind one serialized writer.                                                                                             |
| `src/framework/logging/RunLogger.py`   | **Rework**                                    | Old: owns `runs/<run_id>/` with `events.jsonl + transcript.md + worklog.md`. New: owns `<worklog_folder>/<run_id>/` with the four-file worklog subsystem; terminal + per-block events routed through the `Worklog` writer. |
| `src/framework/ContextWindow.py`       | **New (does not exist)**                      | Four-tier fractional budget class.                                                                                                                                                                                         |
| `src/framework/tokens.py`              | **New (does not exist)**                      | Char-approx `count_tokens` with a pluggable tokenizer seam.                                                                                                                                                                |
| `src/framework/ProgressiveAgentSLM.py` | **Rework (Phase 1)**                          | Flat loop → recursive; uses `ModelChain` + `ContextWindow` + four-file worklog. `_CHARS_PER_TOKEN` moves to `tokens.py`.                                                                                                   |
| `src/framework/AgentConfig.py`         | **Rework (Phase 1)**                          | Must grow all §2 fields + parent→delegate inheritance.                                                                                                                                                                     |
