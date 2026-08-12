# ProgressiveAgentSLM — WIP Implementation Checklists

> Five checklists, one per phase in [planning.md](planning.md) §12 (Phases 0–4), **20 todos each**
> (100 total). Every todo is written so you — or another agent — can execute it cold: it names
> **_Read_** (which plan section / source file to open first), **_Do_** (the concrete change), and
> **_Validate_** (how to prove it is correctly implemented). Work top-to-bottom; a phase gates the
> next, and within a phase the items are roughly ordered by dependency.
>
> Use [planning.md](planning.md) for the **why** (design rationale) and this file for the **how**
> (execution + proof). All target file paths follow the §11 package layout under `src/framework/`.
> "§N" always refers to a section in [planning.md](planning.md).
>
> **2026-08-12 — this tracker now lives inside the `ProgressiveAgentSLM/planning/` folder (the project's
> new home).** The previous copy at `ai-c4y/planning/wip_checklist.md` is superseded. See the
> [scaffolding note](wip_checklist.md#scaffolding-status-2026-08-12) below for what the first
> implementation pass already put on disk.

**Status legend:** `[ ]` todo · `[~]` in progress / exists-needs-rework · `[x]` done & validated.

**Global validation gates (must stay green after every phase):**

- `pytest -q` passes for everything built so far.
- No request ever exceeds the selected model's `max_tokens` (windows are percentages of it that sum to 100).
- `iteration_logging/iteration_*.jsonl` is **only ever appended to** (never rewritten); every
  `cognitive_index` pointer still resolves to a valid `block_id`.

---

## Scaffolding status (2026-08-12)

**First implementation pass complete — the project folder exists.** What's on disk now:

### Project home

- `ProgressiveAgentSLM/` — new project root (in `github/ai-home-lab-docker-compose/`).
- `ProgressiveAgentSLM/planning/` — the entire planning folder brought inside (new home + WIP tracker):
  `planning.md`, `wip_checklist.md` (this file), `design-principle.md`, `example-revised.json`,
  `steal-list-hermes.md`, `analysis-against-hermes.md`, `review-revise-design.md`,
  `design-review-summary.md`, `README.md`.

### Package layout (§11) — scaffolded

- `src/framework/` — all subpackages present with `__init__.py` + the demo entry point.
- `src/agents/models/` — `Ollama.py`, `OpenRouter.py` (ported async `stream()` clients).

### Implemented primitives (importable, tested)

- `src/framework/bounded_io.py` — byte+deadline bounded read (Hermes port).
- `src/framework/CircularRounds.py` — total-work budget with refund (Hermes port).
- `src/framework/tools/safety.py` — traversal + deny-list (Hermes port).
- `src/framework/redact.py` — egress secret redaction (Hermes port).
- `src/framework/guards/tool_loop.py` + `guards/verify_on_stop.py` (Hermes ports).
- `src/framework/delegates/contracts.py` — typed immutable delegate boundary (Hermes port).
- `src/framework/ContextWindow.py` — **rebuilt** to the three-window percentage budget.
- `src/framework/ModelChain.py` — role-tagged ladder + failover + success-reset.
- `src/framework/BehaviorPolicies.py`, `ParallelExecutor.py`.
- `src/framework/ToolRegistry.py`, `tokens.py` (char/4).
- `src/framework/agents/Router.py`, `agents/Reflector.py`.
- `src/framework/memory/` — `RawLog`, `MemoryStore`, `MemoryStores`, `Distiller`, `LogSearch`,
  `RunLogger` (stubs, importable).
- `src/framework/modes/` — `AssistantMode`, `ResearchMode` (stubs).
- `src/framework/config/load.py` — **JSONC loader → recursive tree**.
- `src/framework/ProgressiveAgentSLM.py` — **rebuilt** as the recursive class (stubbed loop).
- `src/framework/AgentConfig.py` — **rebuilt** to the full §2 fields + inheritance.
- `src/framework/example-revised.json` — canonical config (JSONC).

### Tool stubs

- `src/framework/tools/` — `ReadFileTool` (safety-hardened), `TodoTool`, `SqliteVectorQueryTool`,
  `JsonlQueryTool`, and a `build_tool` factory. Remaining tools (Search/Write/Diagram/Python/
  Internet/CodeAnalysis) land in Phase 2.

### Test suite (green from day one)

- `tests/framework/conftest.py`, `test_context_window.py`, `test_model_chain.py`,
  `test_agent_config.py`, `test_load.py`.

### Metadata

- `pyproject.toml`, `requirements.txt`, `README.md`, `.gitignore`.

---

## Status key for the phase checklists below

- `[x]` = implemented + validated (has a passing test / proven behavior).
- `[~]` = exists (scaffold / port) but not fully validated or needs rework.
- `[ ]` = not started.

**Items marked `[~]` below reflect the scaffolding/ports above; most Phase 0–4 items are still `[ ]`.**
Run `pytest -q` from `ProgressiveAgentSLM/` to confirm the green baseline before starting Phase 0 item 3.

---

## Phase 0 — Foundation primitives 🟡

_Goal: the budget, model-ladder, and append-only logging primitives everything else stands on._

> **2026-08-12 — the scaffolding pass already delivered several Phase 0 primitives on disk** (see the
> status note above). Items below marked `[~]` map to existing code and need only validation / wiring;
> `[ ]` items remain unbuilt.

- [~] **1. Orient on the model.**
  - _Read:_ §1–§3 (three-window budget), §4 (ladder), §8 + §17 (append-only log), §11 (layout), §12 Phase 0.
  - _Do:_ Sketch the data flow `iteration_logging → memory_data_stores → context_window → response_window`; list new vs. rework.
  - _Validate:_ You can state, in one sentence each, what each file holds and who writes it. _(Done in the status note.)_
- [~] **2. Inventory existing code.**
  - _Read:_ `src/framework/ModelChain.py`, `src/framework/ContextWindow.py`, `src/framework/memory/RawLog.py`, `src/framework/tokens.py`.
  - _Do:_ Note the gap between the old flat/Supabase code (in the previous home) and the new recursive design.
  - _Validate:_ A short "keep / rework / replace" list committed as a comment block or scratch note.
- [~] **3. Token-count utility.**
  - _Read:_ §3 (auto-infer), §16 #8 (char/4 decision), `src/framework/tokens.py`.
  - _Do:_ `count_tokens(text)` = `(len(text)+3)//4` with a pluggable tokenizer seam (`set_tokenizer`).
  - _Validate:_ `count_tokens("abc"*100) == 75`; unit test asserts monotonicity. _(Implemented; add the unit test in Phase 4.)_
- [~] **4. `ContextWindow` (three-window percentage).**
  - _Read:_ §2 (`context_window_breakdown_percentages`), §3 (window table + defaults).
  - _Do:_ Class holding `cognition_window` / `attention_window` / `response_window` (sum = 100), `resolve(max_tokens)`, `trim`.
  - _Validate:_ Construct from the §13a parent (32.5 / 52.5 / 15.0); attributes read back exactly. _(Implemented + tested.)_
- [ ] **5. Cascade-on-zero donation.**
  - _Read:_ §3 (zero-window rule).
  - _Do:_ When a window percentage is `0`, donate it to the next window.
  - _Validate:_ Set `cognition_window=0`; assert its budget rolls into `attention_window`.
- [~] **6. Resolve window budgets from percentages.**
  - _Read:_ §3 (percentages × `max_tokens`), §4 (`max_tokens: "auto"`).
  - _Do:_ `ContextWindow.resolve(max_tokens)` → each window's token budget = `(pct/100) × max_tokens`.
  - _Validate:_ For gpt-oss (62,000): 32.5% → 20,150; 52.5% → 32,550; 15% → 9,300. _(Implemented + tested.)_
- [~] **7. Per-window trim.**
  - _Read:_ §3 (budget/compaction column), §12 Phase 2 budget-enforcement note.
  - _Do:_ `trim(tier, text)` truncates a window's text to its budget using `count_tokens`.
  - _Validate:_ Feed over-budget text; assert `count_tokens(result) ≤ budget`. _(Implemented; add unit test.)_
- [ ] **8. Compaction signals.**
  - _Read:_ §3 core-loop invariant, §8 (progressive reflection).
  - _Do:_ Expose `size()` and `needs_compaction()` on `ContextWindow` (actual compaction lives in `Reflector`).
  - _Validate:_ `needs_compaction()` flips true once `attention + always_on` exceed budgets.
- [ ] **9. `ContextWindow` unit tests (complete).**
  - _Read:_ §15.1 (unit list).
  - _Do:_ Extend `tests/framework/test_context_window.py` with cascade-on-zero, compaction signal.
  - _Validate:_ `pytest tests/framework/test_context_window.py` green.
- [~] **10. `ModelChain` skeleton + platform factory.**
  - _Read:_ §4 (models table), §11 (`ModelChain.py`), `src/agents/models/Ollama.py` / `OpenRouter.py`.
  - _Do:_ Parse `models_ladder[]`; factory `ollama→Ollama`, `lmstudio→Ollama(url)`, `open_router→OpenRouter`.
  - _Validate:_ Build the §13a ladder; `chain.entries[0]` is the embedding entry. _(Implemented; add tests.)_
- [~] **11. Reachability selection + `"auto"`.**
  - _Read:_ §4 ("Selection & the ladder"), §3 (fractions apply to any model).
  - _Do:_ Select the first **reachable** `is_general_purpose`; `"auto"`/omitted `max_tokens` sizes to the platform default.
  - _Validate:_ With the top model reachable it wins; mark it unreachable and the next is chosen. _(Implemented selection; reachability health-check pending.)_
- [~] **12. Retry budget + switch.**
  - _Read:_ §2 (`max_retries_until_switching_models`, default **5**), §4 (retry budget), §16 #3.
  - _Do:_ Track retries per model (quality self-eval + infra combined); on reaching the budget, advance the ladder pointer and reset the counter.
  - _Validate:_ Feed 5 "not good enough" verdicts; assert the active model advances. _(Implemented + tested.)_
- [~] **13. Infra failures share the budget.**
  - _Read:_ §2, §4 (one budget for quality + infra), §16 #3.
  - _Do:_ Count timeout/HTTP/unreachable against the **same** counter as quality failures.
  - _Validate:_ Mix 3 timeouts + 2 bad verdicts (= 5); assert the model advances after the 5th. _(Implemented + tested.)_
- [~] **14. Success resets the ladder.**
  - _Read:_ §4 ("Success resets the ladder").
  - _Do:_ After a successful iteration, reset the ladder pointer to the **top** model.
  - _Validate:_ Advance to model 1, then a success; next selection starts again at model 0. _(Implemented + tested.)_
- [ ] **15. `ModelChain` unit tests (complete).**
  - _Read:_ §15.1.
  - _Do:_ Extend `tests/framework/test_model_chain.py`: reachability selection, flag-routed fallback.
  - _Validate:_ `pytest tests/framework/test_model_chain.py` green.
- [~] **16. `RawLog` (append-only).**
  - _Read:_ §8 (`iteration_logging/iteration_*.jsonl`), §17 (block records keyed by `block_id`).
  - _Do:_ `append(block) -> block_id` (one JSON line per block) + a `block_id → byte-offset` map for O(1) `fetch`; never rewrite.
  - _Validate:_ Append 3 blocks; each returned `block_id` fetches back the exact block record. _(Implemented; add unit test.)_
- [ ] **17. `CognitiveIndex` (pointer map).**
  - _Read:_ §8 (cognitive_index.jsonl), §17 (record schema).
  - _Do:_ Create `logging/CognitiveIndex.py`: `append(pointer)`, `search(query)`, `compact(0.5)`; summaries via `KeywordExtractor` / `SimpleEntityExtractor`.
  - _Validate:_ Each appended record matches the §17 schema; `search` returns the block whose keywords match.
- [ ] **18. Per-agent windows + single writer.**
  - _Read:_ §8 (context_window / response_window, "one serialized writer").
  - _Do:_ Create `ContextWindowLog.py`, `ResponseWindow.py`, and coordinate all appends behind **one** serialized writer.
  - _Validate:_ Two concurrent `append` calls never interleave (blocks stay whole in `RawLog`).
- [~] **19. `RunLogger` owns `<base_folder_path>/`.**
  - _Read:_ §8 (folder tree), §17.
  - _Do:_ `memory/RunLogger.py` creates `<base_folder_path>/` and emits terminal + per-block events through the single writer.
  - _Validate:_ After a fake run, `<base_folder_path>/iteration_logging/iteration_*.jsonl` exists. _(Implemented; add test.)_
- [ ] **20. Progressive reflection — integrity.**
  - _Read:_ §3 (compaction), §8 ("Progressive reflection").
  - _Do:_ Implement `Reflector` adaptive compaction (only enough to fit; protect head+tail; update prior summary); `RawLog` untouched.
  - _Validate:_ Append N blocks → compact → assert the raw log is byte-identical and every surviving pointer still resolves.

---

## Phase 1 — Recursive core agent (runnable vertical slice) 🟡

_Goal: a single `ProgressiveAgentSLM` that retrieves, routes, calls a tool, delegates once, and streams an answer through `create_chat_backend`._

- [~] **1. Orient on the object + loop.**
  - _Read:_ §2 (object table), §5 (behavior_policies), §6 (tools), §7 (delegates), §10 (control flow), §12 Phase 1, §14 (reuse map).
  - _Do:_ List the per-step loop stages (retrieve → assemble → select model → route/act → answer → flush → self-eval).
  - _Validate:_ You can name, for each stage, the primitive from Phase 0 it uses. _(The class exists; the loop body is stubbed.)_
- [~] **2. Read the code to rework.**
  - _Read:_ `src/framework/ProgressiveAgentSLM.py` (recursive skeleton), `AgentConfig.py`, `agents/Router.py`, `agents/Reflector.py`, `ToolRegistry.py`.
  - _Do:_ Mark exactly what to keep vs. rewrite for recursion.
  - _Validate:_ Notes reference concrete method names you will reuse.
- [~] **3. `AgentConfig` fields.**
  - _Read:_ §2 (all fields incl. `system_prompt`, `base_folder_path`, `max_retries_until_switching_models`).
  - _Do:_ Parse every §2 field with the documented default (retry budget **5**).
  - _Validate:_ Loading the §13a parent dict yields all fields; missing optionals fall back to defaults. _(Implemented; add tests.)_
- [~] **4. Delegate inheritance.**
  - _Read:_ §2 inheritance note, §7, §13a.
  - _Do:_ Inherit `models_ladder` + `max_retries_until_switching_models` + `working_directories` + `parallel_subprocesses` + round cap from parent; keep windows / `system_prompt` / `behavior_policies` / `tools` per-agent.
  - _Validate:_ A delegate omitting `models_ladder` reports the parent's ladder but its **own** windows. _(Implemented + tested.)_
- [ ] **5. Config unit test (complete).**
  - _Read:_ §15.1.
  - _Do:_ Extend `tests/framework/test_agent_config.py`: working_directories + parallel_subprocesses inheritance.
  - _Validate:_ `pytest` green.
- [~] **6. `ToolRegistry` + base.**
  - _Read:_ §6 (each tool carries `when`), §11 (`ToolRegistry.py`).
  - _Do:_ `Tool` base has `name`, `description`, `when`, optional `models_ladder`, async `run`/`stream`; registry dispatches by `name`.
  - _Validate:_ Registering a stub tool makes it discoverable and its `when` retrievable for pruning. _(Implemented; add test.)_
- [ ] **7. `SqliteVectorQueryTool` (primary) — real sqlite-vec.**
  - _Read:_ §6 (`SqliteVectorQueryTool` row), §14 (`SqliteVectorStore.async_query`).
  - _Do:_ Wire `src/framework/tools/SqliteVectorQueryTool.py` to a real `SqliteVectorStore` (`sqlite-vec`) — `async_query` over a local `.db` file + `table`.
  - _Validate:_ Against a stub store, calling with `{path, table}` invokes `async_query` with that table.
- [~] **8. `ReadFileTool` (traversal-safe + deny-list).**
  - _Read:_ §6 (`ReadFileTool` row), §10 (tool safety), `src/framework/tools/safety.py`.
  - _Do:_ Resolve paths under `base_folder_path` + `working_directories`; reject `../` / absolute escapes / deny-list hits.
  - _Validate:_ Read inside an allowed root works; `../` and deny-listed paths raise. _(Implemented; add test.)_
- [~] **9. `TodoTool`.**
  - _Read:_ §6 (`TodoTool` row), §5 (todo checklist).
  - _Do:_ Model **rewrites the whole list** `[{id, content, status}]` into `<base_folder_path>/todo.md`.
  - _Validate:_ Writing a list then reading returns it verbatim; malformed status rejected. _(Implemented; add test.)_
- [~] **10. `Router` (route by description).**
  - _Read:_ §7 (route by description), §14 (`_parse_agent_routing`).
  - _Do:_ Choose delegate(s) by `description` via the generalized `_parse_agent_routing` (`delegate:<id>`); prune the tool menu by each tool's `when`.
  - _Validate:_ Given a code question, the code delegate is selected by its `description`. _(Implemented; add test.)_
- [~] **11. `Reflector` (adaptive compaction).**
  - _Read:_ §8 (reflection), §14 (`KnowledgeCompression`, `IterationSummarizer`), `agents/Reflector.py`.
  - _Do:_ Compact the working set **adaptively** (only enough to fit; protect head+tail; update prior summary) reusing the compression primitives.
  - _Validate:_ Over-budget input returns a result ≤ budget; `RawLog` untouched; pointers still resolve.
- [~] **12. `ProgressiveAgentSLM` skeleton.**
  - _Read:_ §2, §11 (class responsibilities).
  - _Do:_ Constructor owns `ContextWindow`, `ModelChain`, tools, `delegates`, and the run's logger. _(Implemented.)_
  - _Validate:_ Instantiating the §13a parent builds the object graph (1 delegate nested) without error. _(Implemented — `load_agent` test.)_
- [ ] **13. Retrieve step (index-and-retrieve).**
  - _Read:_ §3 core loop, §8 ("read path").
  - _Do:_ Implement per-step retrieval: `memory_data_stores` (via `SqliteVectorQueryTool`) + raw log (via `JsonlQueryTool`) → working set.
  - _Validate:_ With seeded blocks, only relevant blocks enter the working set.
- [ ] **14. Prompt assembly (stable prefix + volatile suffix).**
  - _Read:_ §3 (prompt-assembly block), §5 (behavior_policies render), §6/§7 (description-routed delegates + when-pruned tools).
  - _Do:_ Build the three-window prompt: stable prefix (`system_prompt` + policies + delegate descriptions + pruned tool menu + always-on stores) + volatile suffix (question + retrieved context + reasoning).
  - _Validate:_ Rendered prompt contains the policies and only the pruned tool menu; the prefix is **byte-identical** across iterations; each window ≤ its budget.
- [ ] **15. Model call + streaming answer.**
  - _Read:_ §4 (selection), §14 (`create_chat_backend`).
  - _Do:_ Call the `ModelChain`-selected model; stream chunks as an async generator of `str`; cap output at the `response_window` budget.
  - _Validate:_ A stub model yields chunks that stream out; output never exceeds the answer budget.
- [ ] **16. Block flush.**
  - _Read:_ §8 ("write path, per block").
  - _Do:_ On completion, flush `response_window` → `RawLog` (get `block_id`) + `CognitiveIndex` (pointer), then **clear** `response_window`.
  - _Validate:_ After a step, the answer is in the raw log, indexed, and `response_window` is empty.
- [ ] **17. Quick self-eval → switch signal.**
  - _Read:_ §4 (retry budget), §14 (`AnswerEvaluator`), §16 #3.
  - _Do:_ After each iteration, run a quick self-eval; a "not good enough" verdict increments the `ModelChain` retry counter.
  - _Validate:_ Repeated bad verdicts trigger a model switch via Phase 0 item 12.
- [ ] **18. Recursion into delegates.**
  - _Read:_ §7 (hands-down / delivers), §2 inheritance.
  - _Do:_ Run a chosen delegate's own full loop; it writes finished blocks to the **shared** `RawLog` under its `agent_id` but returns only its **final** answer to the parent.
  - _Validate:_ Parent receives one final block; the raw log shows the delegate's full work under its `agent_id`.
- [ ] **19. Stop conditions.**
  - _Read:_ §4 (stopping / ladder exhaustion), §7 (depth).
  - _Do:_ Enforce ladder-exhaustion (per-model retry budget spent) + a recursion-depth cap + the `CircularRounds` cap.
  - _Validate:_ A never-satisfied stub stops once the last model's retry budget is spent; deep nesting stops at the recursion cap.
- [ ] **20. Wire the demo (vertical slice).**
  - _Read:_ §11 (`progressive_agent_slm_demo.py`), §13b, §14 (`create_chat_backend`).
  - _Do:_ The demo `load_agent("src/framework/example-revised.json")` → `create_chat_backend` → `uvicorn` on **8001**.
  - _Validate:_ Boot it, ask one multi-step question; observe streamed think/route/delegate/answer and a populated `<base_folder_path>/`.

---

## Phase 2 — Full tools, behavior_policies, model routing ⬜

_Goal: the complete tool catalog, declarative behavior_policies, ranking, live budget enforcement, and full-text log search._

- [~] **1. Orient.**
  - _Read:_ §5 (behavior_policies), §6 (full tool catalog), §3 (budgets), §8 (read/compaction), §12 Phase 2.
  - _Do:_ List the remaining tools + the policy engine + ranking + budget + search deliverables.
  - _Validate:_ Each maps to a target file in §11.
- [ ] **2. `SearchFileTool`.**
  - _Read:_ §6 row, §14 (`FileHanlder`).
  - _Do:_ Search by name or content (+ optional `glob`), ripgrep-style; return `path + line + snippet`; resolve under `base_folder_path` + `working_directories`.
  - _Validate:_ Seeded tree returns correct name/content hits; snippet + line number accurate.
- [ ] **3. Validate `SearchFileTool` traversal safety.**
  - _Read:_ §10 (tool safety), `tools/safety.py`.
  - _Do:_ Add traversal/absolute-escape + deny-list rejection.
  - _Validate:_ Searching outside allowed roots raises (OWASP A01/A03).
- [ ] **4. `WriteFileTool`.**
  - _Read:_ §6 row, §10 (safety), `tools/safety.py`.
  - _Do:_ Overwrite-or-append write, resolve under allowed roots, traversal + deny-list rejection, optional `require_approval` (default false).
  - _Validate:_ Overwrite vs. append both work inside allowed roots; escape + deny-list rejected; `require_approval: true` gates the write.
- [ ] **5. `VectorMemoryTool` (sqlite-vec `remember`/`recall`).**
  - _Read:_ §6 row, §14 (`SqliteVectorStore` + `Embedding`), §16 #9.
  - _Do:_ `recall(query, k)` + `remember(text, tags?)` over a local sqlite-vec table; cross-run.
  - _Validate:_ `remember` then `recall` returns the item; a second run can recall it.
- [ ] **6. `SkillTool` (progressive disclosure).**
  - _Read:_ §6 row, §10 (trusted-local only), §16 #10.
  - _Do:_ Parse `{id, description, when}` frontmatter from `skills_dir`; expose only those until `when` matches, then load the body.
  - _Validate:_ Body is hidden until matched; external/out-of-dir skill paths rejected.
- [ ] **7. `GenerateDiagramTool`.**
  - _Read:_ §6 row, §5 (`visual_representation`).
  - _Do:_ Emit Mermaid.
  - _Validate:_ Output parses as a valid ```mermaid block.
- [ ] **8. `RunPythonTool`.**
  - _Read:_ §6 row, §10 (autonomous-exec warning), §14 (`PythonCodeExecute`).
  - _Do:_ Wrap `PythonCodeExecute`; optional `require_approval` (default false); capture stdout/stderr.
  - _Validate:_ A snippet returns its stdout; `require_approval: true` gates execution.
- [ ] **9. `SearchInternetTool` / `CodeAnalysisTool`.**
  - _Read:_ §6 (specialized delegates), §9 (knowledge sources).
  - _Do:_ Web search + static code analysis for specialized delegates (e.g. `bvms-code-analyzer`).
  - _Validate:_ Each returns useful context for its delegate.
- [ ] **10. Register + prune all tools.**
  - _Read:_ §6 (menu pruning), §7.
  - _Do:_ Register every tool in `ToolRegistry`; confirm each exposes a `when` used by the `Router` pruner.
  - _Validate:_ For a given step, only `when`-matching tools appear in the assembled menu.
- [~] **11. `BehaviorPolicies` engine.**
  - _Read:_ §5 (render each iteration + todo), §11 (`BehaviorPolicies.py`).
  - _Do:_ Render `behavior_policies` `when → then` rules into the system prompt every iteration; fire them at their `run_after` hooks.
  - _Validate:_ The prompt contains each rule as "When …, then …". _(Implemented; add tests.)_
- [ ] **12. Baseline policies.**
  - _Read:_ §5 (recommended set).
  - _Do:_ Ship `deep_planning`, `analyzing_retrieval_results`, `double_checking`, `visual_representation`, `refusing_to_invent`, `self_reflection`.
  - _Validate:_ Config with these renders all six; ids unique.
- [ ] **13. Enforcement guards.**
  - _Read:_ §5, §10, `guards/`.
  - _Do:_ Wire `double_checking` → verify-on-stop, `refusing_to_invent` → grounding gate (`NoFindingsGuard`), anti-drift → tool-loop guard (`guards/tool_loop.py`).
  - _Validate:_ Empty-KB question yields an honest "not available"; a gap triggers one more bounded iteration; a repeated identical tool call is detected.
- [ ] **14. `SqliteVectorQueryTool` ranking path.**
  - _Read:_ §6 (`ranking`), §14 (`RagAssistant.stream` parallel `DocumentRanking`).
  - _Do:_ When `ranking: true`, re-rank retrieved chunks with parallel `DocumentRanking` batches.
  - _Validate:_ Ranking on vs. off changes chunk order; latency stays bounded (batched, not serial).
- [ ] **15. Live budget enforcement.**
  - _Read:_ §3 (budgets), §12 Phase 2 budget note.
  - _Do:_ In the live loop, measure tokens (`tokens.py`), trim each window, apply cascade-on-zero, cap always-on stores.
  - _Validate:_ Assert every assembled request ≤ selected model `max_tokens` across a multi-iteration run.
- [ ] **16. Compaction under load.**
  - _Read:_ §8 (progressive reflection).
  - _Do:_ Trigger real adaptive compaction mid-run when `attention + always_on` exceed budgets.
  - _Validate:_ Working windows shrink; answers still cite detail recovered from the raw log / stores.
- [ ] **17. `LogSearch` (FTS5).**
  - _Read:_ §8 (`<base_folder_path>/log_index.db`), §17, §11 (`memory/LogSearch.py`).
  - _Do:_ Real SQLite FTS5 (trigram + CJK) over `iteration_logging/*.jsonl`; incremental bounded merge, query caps, resumable rebuild.
  - _Validate:_ CLI query returns the run and correct blocks for a known term.
- [ ] **18. Native + prompted tool-calling.**
  - _Read:_ §10 (tool-call protocol).
  - _Do:_ Support native Ollama `/api/chat` tool-calling when available, with a prompted-JSON + robust-parser fallback.
  - _Validate:_ Same tool fires via both paths on a capable and a non-capable stub model.
- [ ] **19. Cross-tool integration.**
  - _Read:_ §6, §7.
  - _Do:_ Run a scenario exercising SqliteVector → Write → Todo → Diagram in one iteration.
  - _Validate:_ Each tool's block lands in the raw log under the right `actor` (§17).
- [ ] **20. Phase-2 end-to-end.**
  - _Read:_ §15.3.
  - _Do:_ Run the demo with all tools + policies enabled on a multi-step BVMS question.
  - _Validate:_ Every tool callable, a Mermaid diagram emitted, ranking applied, budgets never exceeded, `LogSearch` CLI finds the run.

---

## Phase 3 — Config loader (JSON + Python) ⬜

_Goal: build the whole agent tree from `example-revised.json` (or a Python dict) with schema validation and delegate inheritance — no code change to add/remove agents._

- [~] **1. Orient.**
  - _Read:_ §2 (object), §11 (`config/`), §13 (JSON + Python), §13a (inheritance note).
  - _Do:_ List the loader responsibilities: parse → validate → inherit → build tree.
  - _Validate:_ You can point to the single place inheritance lives (`load.py`). _(Implemented.)_
- [~] **2. Reconcile the canonical config.**
  - _Read:_ `src/framework/example-revised.json`, §13a.
  - _Do:_ Keep the live copy field-for-field aligned with §13a.
  - _Validate:_ The JSONC file parses (JSONC-stripped) into the expected dict. _(Implemented.)_
- [ ] **3. Schema — core fields.**
  - _Read:_ §2 (types + required), §11 (`schema.json`).
  - _Do:_ Write `config/schema.json`: required `id`, `description`, ≥1 `model`; type each field.
  - _Validate:_ Schema lints as valid JSON Schema.
- [ ] **4. Schema — recursion.**
  - _Read:_ §7 (delegate = full agent).
  - _Do:_ Add a recursive `$ref` so each `delegates[]` entry is itself an agent.
  - _Validate:_ The §13a tree validates through the recursive ref.
- [ ] **5. Schema — enums & unions.**
  - _Read:_ §4 (`platform`, `max_tokens`), §6 (tool `type`), §5 (policy shape).
  - _Do:_ Enforce `platform ∈ {ollama, lmstudio, open_router}`, tool `type` enum, `max_tokens: number | "auto"`, todo `status` enum.
  - _Validate:_ Valid values pass; a bad platform fails.
- [ ] **6. Validate canonical config.**
  - _Read:_ §13a.
  - _Do:_ Run the schema against `example-revised.json`.
  - _Validate:_ Passes with zero errors.
- [ ] **7. Validate rejection.**
  - _Read:_ §2 (required), §4.
  - _Do:_ Feed a config missing `models` and one with a bad `platform`.
  - _Validate:_ Both fail with a message naming the offending field.
- [~] **8. `load.py` — parse.**
  - _Read:_ §11 (`load.py`), §13b (Option A).
  - _Do:_ `load_agent(path|dict)` → validate → build `AgentConfig` tree recursively.
  - _Validate:_ Loading `example-revised.json` returns the tree (parent + 1 delegate). _(Implemented + tested.)_
- [~] **9. `load.py` — inheritance.**
  - _Read:_ §2 inheritance note, §13a.
  - _Do:_ Apply parent→delegate inheritance; keep per-agent fields isolated.
  - _Validate:_ Delegates report the parent ladder + retry budget but their own windows. _(Implemented + tested.)_
- [~] **10. `load.py` — build objects.**
  - _Read:_ §11, Phase 1 (`ProgressiveAgentSLM`, `ToolRegistry`).
  - _Do:_ Instantiate `ProgressiveAgentSLM` from each `AgentConfig`, wiring tools via `ToolRegistry` and nesting delegates.
  - _Validate:_ The returned parent has its live delegate instances with tools attached. _(Implemented.)_
- [ ] **11. `load.py` — Python-dict parity.**
  - _Read:_ §13b (Option B).
  - _Do:_ Ensure a Python dict/kwargs path produces the same tree as the JSON path.
  - _Validate:_ JSON-loaded and dict-built trees compare equal (ids, budgets, tools, inheritance).
- [ ] **12. Friendly errors.**
  - _Read:_ §16 (author usability).
  - _Do:_ On validation failure, report the failing `agent_id` + field + reason.
  - _Validate:_ A broken delegate names itself in the error.
- [ ] **13. Fraction-sum guard (complete).**
  - _Read:_ §3 (windows sum = 100), §13a.
  - _Do:_ Load-time check that each agent's windows sum to **100** and the always-on-store sum fits the cognition window.
  - _Validate:_ Canonical config passes; a bad sum fails the guard. _(ContextWindow enforces sum = 100; the always-on sum guard is in ContextWindow too — add loader wiring.)_
- [~] **14. Round-trip test (JSON).**
  - _Read:_ §15.2.
  - _Do:_ `tests/framework/test_load.py`: load `example-revised.json`, assert tree shape + inheritance + tool wiring.
  - _Validate:_ `pytest` green. _(Implemented.)_
- [ ] **15. Round-trip test (Python).**
  - _Read:_ §13b.
  - _Do:_ Build Option B in code; assert equivalence to the JSON tree.
  - _Validate:_ Equality assertion passes.
- [ ] **16. `ApiServer` + health endpoint.**
  - _Read:_ §7b (health), §11 (`modes/AssistantMode.py`).
  - _Do:_ `GET /api/v1/health`: models (concurrency vs. max), stores (row counts / last-distilled), windows (usage), delegates (states / depth).
  - _Validate:_ The health payload reports real numbers for a live run.
- [~] **17. Wire loader into the demo.**
  - _Read:_ §13b (Option A).
  - _Do:_ Switch `progressive_agent_slm_demo.py` to `load_agent("src/framework/example-revised.json")`. _(Implemented.)_
  - _Validate:_ Demo boots on 8001 from the JSON alone.
- [ ] **18. Authoring README.**
  - _Read:_ §2, §5, §6, §7 (author-facing behavior).
  - _Do:_ Document every field, defaults, inheritance, description-based routing, and each tool shape.
  - _Validate:_ A newcomer can add a third delegate by editing only JSON.
- [ ] **19. Defaults-only example.**
  - _Read:_ §2 (defaults), §12 Phase 3.
  - _Do:_ Add a minimal single-agent config to exercise the default path.
  - _Validate:_ It loads and runs using all defaults (retry budget 5, windows 32.5/52.5/15).
- [ ] **20. Phase-3 acceptance.**
  - _Read:_ §15.2.
  - _Do:_ From a fresh checkout, load `example-revised.json`, boot the demo, ask a question; then add a delegate via JSON only.
  - _Validate:_ Answer streams; the new delegate is routable **without any code change**.

---

## Phase 4 — Hardening ⬜

_Goal: a green test suite, an integration smoke test, robust retries/timeouts, safety hooks, and the plan's open questions resolved._

- [ ] **1. Orient.**
  - _Read:_ §15 (Verification), §12 Phase 4, §10 (safety), §16 (open questions).
  - _Do:_ Turn each §15 bullet into a named test file.
  - _Validate:_ A test matrix maps every §15 claim to a test.
- [ ] **2. Stub model harness.**
  - _Read:_ §12 Phase 4, §14 (`Ollama`/`OpenRouter` interface).
  - _Do:_ Build a stub implementing `.stream` (async generator) with scriptable outputs + failure injection (quality + infra).
  - _Validate:_ Stub can emit chunks, a "bad" verdict, and a timeout on demand.
- [ ] **3. Config/inheritance tests (complete).**
  - _Read:_ §2 inheritance, §15.1.
  - _Do:_ Assert delegate omitting `models`/retry budget inherits them, shares `base_folder_path`, keeps own windows.
  - _Validate:_ `pytest` green.
- [ ] **4. Budgeting tests (complete).**
  - _Read:_ §3, §15.1.
  - _Do:_ Cover trim, cascade-on-zero donation, always-on sum guard, byte-identical prefix across iterations.
  - _Validate:_ Each rule asserted independently.
- [ ] **5. Raw-log immutability tests.**
  - _Read:_ §3, §8, §17.
  - _Do:_ Append N blocks → compact → assert `block_id` integrity and raw-log immutability.
  - _Validate:_ Byte-compare the raw log before/after == equal.
- [ ] **6. Model-ladder tests (complete).**
  - _Read:_ §4, §16 #3–#4, §15.1.
  - _Do:_ Assert the model switches after **5** combined retries (quality + infra on one counter), success-reset to top, ladder-exhaustion abort, flag-routed fallback.
  - _Validate:_ Quality and infra failures share the one counter.
- [ ] **7. Router pruning tests.**
  - _Read:_ §7, §15.1.
  - _Do:_ Assert delegates are selected by `description`; `delegate:<id>` parses; only `when`-matching tools enter the menu.
  - _Validate:_ Code vs. domain question route to the right delegate.
- [ ] **8. Tool tests.**
  - _Read:_ §6, §14, §15.1.
  - _Do:_ Assert `SqliteVectorQueryTool` calls `async_query` with `{path, table}`; file tools reject traversal + deny-list; `TodoTool` round-trips.
  - _Validate:_ Mocked store records the exact call.
- [ ] **9. Single-writer tests.**
  - _Read:_ §8, §15.1.
  - _Do:_ Assert append/read behind one writer; parallel delegate blocks don't interleave; `response_window` flush→clear.
  - _Validate:_ Concurrency test shows whole, ordered blocks.
- [ ] **10. Logging + FTS round-trip.**
  - _Read:_ §8, §17, §15.1.
  - _Do:_ Assert JSONL block events written and `LogSearch` finds them.
  - _Validate:_ Search returns the seeded run + blocks.
- [ ] **11. `bounded_io` / `run_clock` tests.**
  - _Read:_ §4, §10, §15.1.
  - _Do:_ Assert a stalled read times out (deadline → one infra failure); a whole-run clock cap stops the run.
  - _Validate:_ Deadline hit increments the model-chain failure counter.
- [ ] **12. Integration smoke.**
  - _Read:_ §15.2.
  - _Do:_ Load `example-revised.json` with the stub model; assert tree builds, parent routes by description, delegate calls its tools, stores stay ≤ budgets, logs + `.db` exist, FTS finds the run.
  - _Validate:_ One test drives the whole slice end-to-end.
- [ ] **13. Budget property test.**
  - _Read:_ §3, §4, §15.4.
  - _Do:_ Over randomized budgets, assert no assembled request exceeds the selected model `max_tokens`.
  - _Validate:_ Property holds across many samples.
- [ ] **14. Timeouts / retries / fall-through.**
  - _Read:_ §4, §14 (`OpenRouter` 429 backoff), §12 Phase 4.
  - _Do:_ Reuse 429/backoff; on infra error consume the shared retry budget and fall through to the next model when it is spent.
  - _Validate:_ Injected 429 retries then advances once the shared retry budget is exhausted.
- [ ] **15. Approval hook.**
  - _Read:_ §10 (safety), §6 (`RunPythonTool`/`WriteFileTool`).
  - _Do:_ Add a `require_approval` hook (default false / no-op); wire it to `RunPythonTool` + `WriteFileTool`.
  - _Validate:_ `require_approval: true` blocks until confirmed; default (false) allows.
- [ ] **16. Skill-safety review.**
  - _Read:_ §6 (`SkillTool`), §10 (trusted-local), §16 #10.
  - _Do:_ Confirm skills load **trusted-local files only**; document the prompt-injection surface.
  - _Validate:_ External skill path rejected; note added to the authoring README.
- [ ] **17. Single-writer stress.**
  - _Read:_ §8 ("one serialized writer").
  - _Do:_ Concurrently flush blocks from parent + both delegates.
  - _Validate:_ Raw-log line ranges stay consistent and every pointer resolves.
- [ ] **18. Resolve open questions.**
  - _Read:_ §16.
  - _Do:_ Flip any remaining `_TBD_` rows to a resolution.
  - _Validate:_ [planning.md](planning.md) §12 has no remaining `_TBD_`.
- [ ] **19. CI wiring.**
  - _Read:_ §15, `pyproject.toml`.
  - _Do:_ Add a `pytest` task/target and (optionally) coverage over `src/framework/`.
  - _Validate:_ One command runs the whole suite green.
- [ ] **20. Phase-4 acceptance.**
  - _Read:_ §15.3, §12 (statuses).
  - _Do:_ Run the full suite + the manual §15.3 launch; then update §12 phase statuses to ✅ and bump the footer date.
  - _Validate:_ Green suite **and** a live multi-step BVMS answer with searchable logs; plan statuses reflect reality.

---

_Companion to [planning.md](planning.md). Last updated: 2026-08-12 (project home: `ProgressiveAgentSLM/planning/`)._
