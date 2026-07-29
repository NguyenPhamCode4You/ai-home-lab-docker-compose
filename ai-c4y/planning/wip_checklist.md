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

**Status legend:** `[ ]` todo · `[~]` in progress / exists-needs-rework · `[x]` done & validated.

**Global validation gates (must stay green after every phase):**

- `pytest -q` passes for everything built so far.
- No request ever exceeds the selected model's `max_tokens` (tiers are fractions of it that sum to < 1).
- `raw_worklog.log` is **only ever appended to** (never rewritten); every `cognitive_index` pointer still resolves to a valid line range.

---

## Phase 0 — Foundation primitives 🟡

_Goal: the budget, model-ladder, and four-file `worklog` logging primitives everything else stands on._

- [ ] **1. Orient on the model.**
  - _Read:_ §1–§3 (four-tier budget), §4 (ladder), §8 + §17 (four-file `worklog`), §11 (layout), §12 Phase 0.
  - _Do:_ Sketch the data flow `raw_worklog → cognitive_index → context_window → response_window` on paper; list which primitives are **new** vs. **rework**.
  - _Validate:_ You can state, in one sentence each, what each of the four files holds and who writes it.
- [ ] **2. Inventory existing code.**
  - _Read:_ `src/framework/ModelRegistry.py`, `src/framework/Worklog.py`, `src/framework/logging/RunLogger.py`, `src/framework/ContextWindow.py` (if present).
  - _Do:_ Note the gap between today's `runs/` markdown design and the target four-file design.
  - _Validate:_ A short "keep / rework / replace" list committed as a comment block or scratch note.
- [ ] **3. Token-count utility.**
  - _Read:_ §3 (auto-infer), §16 #7 (char≈token decision), the existing `CHARS_PER_TOKEN` constant.
  - _Do:_ Create `src/framework/tokens.py` with `count_tokens(text) -> int` (char-approx now, pluggable tokenizer seam for P2).
  - _Validate:_ `count_tokens("abc"*100)` ≈ `len/CHARS_PER_TOKEN`; unit test asserts monotonicity.
- [ ] **4. `ContextWindow` skeleton.**
  - _Read:_ §2 (`context_window_breakdown` field), §3 (tier table + defaults).
  - _Do:_ Create `src/framework/ContextWindow.py` — a class holding the three tier fractions (`conversation_history_awareness` default **0.025**, `cognitive_reflection_behavior`, `current_working_attention`; the remainder is the answer).
  - _Validate:_ Construct from the §13a parent dict (0.025 / 0.325 / 0.525); attributes read back exactly.
- [ ] **5. Cascade-on-zero donation.**
  - _Read:_ §3 (the `conversation_history_awareness = 0` rule).
  - _Do:_ Implement: when a tier's fraction is `0`, donate it to the next tier ("stop listening to chat, think harder").
  - _Validate:_ Set `conversation_history_awareness=0`; assert its budget rolls into `cognitive_reflection_behavior`/`current_working_attention`.
- [ ] **6. Resolve tier budgets from fractions.**
  - _Read:_ §3 (fractions × `max_tokens`), §4 (`max_tokens: "auto"`).
  - _Do:_ `ContextWindow.resolve(max_tokens)` → each tier's token budget = its fraction × `max_tokens`; the leftover (1 − Σfractions) is the answer budget.
  - _Validate:_ For gpt-oss (62,000) the parent's 0.025 / 0.325 / 0.525 resolve to ≈ 1,550 / 20,150 / 32,550 (≈ 7,750 to answer); asserted in a test.
- [ ] **7. Per-tier trim.**
  - _Read:_ §3 (budget/compaction column), §12 Phase 2 budget-enforcement note.
  - _Do:_ `trim(tier, text)` truncates a tier's text to its budget using `count_tokens`.
  - _Validate:_ Feed over-budget text; assert `count_tokens(result) ≤ budget`.
- [ ] **8. Compaction signals.**
  - _Read:_ §3 core-loop invariant, §8 (progressive reflection).
  - _Do:_ Expose `size()` and `needs_compaction()` on `ContextWindow` (actual 50% compaction lives in `Reflector`, Phase 1).
  - _Validate:_ `needs_compaction()` flips true once `current_working_attention + cognitive_reflection_behavior` exceed their budgets.
- [ ] **9. `ContextWindow` unit tests.**
  - _Read:_ §15.1 (unit list).
  - _Do:_ `tests/framework/test_context_window.py` covering budgets, cascade, auto-infer, trim, compaction signal.
  - _Validate:_ `pytest tests/framework/test_context_window.py` green.
- [ ] **10. `ModelChain` skeleton + platform factory.**
  - _Read:_ §4 (models table), §11 (`ModelChain.py`), the existing `Ollama` / `OpenRouter` clients.
  - _Do:_ Create `src/framework/ModelChain.py`: parse `models[]`; factory `ollama→Ollama`, `open_router→OpenRouter`.
  - _Validate:_ Build the §13a two-model ladder; `chain[0]` is the Ollama client, `chain[1]` the OpenRouter one.
- [ ] **11. Reachability selection + `"auto"`.**
  - _Read:_ §4 ("Selection & the ladder"), §3 (fractions apply to any model).
  - _Do:_ Select the first **reachable** model on the ladder (health/ping); `"auto"`/omitted `max_tokens` sizes to the platform default before fractions apply.
  - _Validate:_ With the top model reachable it wins; mark it unreachable and the next model is chosen.
- [ ] **12. Retry budget + switch.**
  - _Read:_ §2 (`max_retries_untill_switching_models`, default **5**), §4 (retry budget), §16 #3.
  - _Do:_ Track retries per model (quality self-eval + infra combined); on reaching the budget, advance the ladder pointer and reset the per-model counter.
  - _Validate:_ Feed 5 "not good enough" verdicts; assert the active model advances to index 1.
- [ ] **13. Infra failures share the budget.**
  - _Read:_ §2 (`max_retries_untill_switching_models`), §4 (one budget for quality + infra), §16 #3.
  - _Do:_ Count infra failures (timeout/HTTP/unreachable) against the **same** counter as quality failures; exhausting it advances the ladder.
  - _Validate:_ Mix 3 timeouts + 2 bad verdicts (= 5); assert the model advances after the 5th.
- [ ] **14. Success resets the ladder.**
  - _Read:_ §4 ("Success resets the ladder").
  - _Do:_ After a successful iteration, reset the ladder pointer to the **top** model for the next iteration.
  - _Validate:_ Advance to model 1, then a success; next selection starts again at model 0.
- [ ] **15. `ModelChain` unit tests.**
  - _Read:_ §15.1.
  - _Do:_ `tests/framework/test_model_chain.py` with stub clients: reachability selection, retry switch (5, quality + infra combined), success-reset, ladder exhaustion.
  - _Validate:_ `pytest tests/framework/test_model_chain.py` green.
- [ ] **16. `RawWorklog` (append-only).**
  - _Read:_ §8 (`raw_worklog.log` row), §17 (block delimiters + line ranges).
  - _Do:_ Create `src/framework/logging/RawWorklog.py`: `append(block) -> (start_line, end_line)`; never rewrite.
  - _Validate:_ Append 3 blocks; returned ranges are contiguous and re-reading those lines returns the exact block text.
- [ ] **17. `CognitiveIndex` (pointer map).**
  - _Read:_ §8 (`cognitive_index.jsonl`), §17 (record schema: `block_id, ts, agent_id, iteration, phase, actor, raw_lines, summary, keywords, tokens`).
  - _Do:_ Create `src/framework/logging/CognitiveIndex.py`: `append(pointer)`, `search(query)`, `compact(0.5)`; ~10–20-token summaries via `KeywordExtractor` / `SimpleEntityExtractor`.
  - _Validate:_ Each appended record matches the §17 schema; `search` returns the block whose keywords match.
- [ ] **18. Per-agent windows + single writer.**
  - _Read:_ §8 (`context_window.log` / `response_window.log`, "one serialized writer").
  - _Do:_ Create `ContextWindowLog.py`, `ResponseWindow.py`, and `Worklog.py` coordinating all four behind **one** serialized writer (`asyncio.Lock`/queue).
  - _Validate:_ Two concurrent `append` calls never interleave (blocks stay whole in `raw_worklog`).
- [ ] **19. `RunLogger` owns `<worklog_folder>/<run_id>/`.**
  - _Read:_ §8 (folder tree), §17.
  - _Do:_ Rework `logging/RunLogger.py` to create `<worklog_folder>/<run_id>/` and emit terminal + per-block events through the `Worklog` writer.
  - _Validate:_ After a fake run, `<worklog_folder>/<run_id>/` contains `raw_worklog.log`, `cognitive_index.jsonl`, `context_window.log`, `response_window.log`.
- [ ] **20. Progressive reflection (50%) — integrity.**
  - _Read:_ §3 (compaction), §8 ("Progressive reflection").
  - _Do:_ Implement `CognitiveIndex.compact(0.5)` + `ContextWindowLog.compact(0.5)` (merge pointers / drop stale blocks); `raw_worklog` untouched.
  - _Validate:_ Append N blocks → compact → assert index/context shrink ~50%, `raw_worklog` byte-identical, and every surviving pointer still resolves to correct lines.

---

## Phase 1 — Recursive core agent (runnable vertical slice) 🟡

_Goal: a single `ProgressiveAgentSLM` that retrieves, routes, calls a tool, delegates once, and streams an answer through `create_chat_backend`._

- [ ] **1. Orient on the object + loop.**
  - _Read:_ §2 (object table), §5 (cognitive_behavior), §6 (tools), §7 (delegates), §10 (control flow), §12 Phase 1, §14 (reuse map).
  - _Do:_ List the per-step loop stages (retrieve → assemble → select model → route/act → answer → flush → self-eval).
  - _Validate:_ You can name, for each stage, the primitive from Phase 0 it uses.
- [ ] **2. Read the code to rework.**
  - _Read:_ `src/framework/AgentConfig.py`, `src/framework/ProgressiveAgentSLM.py` (flat), `src/framework/agents/Forwarder.py`, `agents/Reflector.py`, `ToolRegistry.py`, `tools/ReadFileTool.py`; `AssistantOrchestra._parse_agent_routing` / `_parse_eval_result`.
  - _Do:_ Mark exactly what to keep vs. rewrite for recursion.
  - _Validate:_ Notes reference concrete method names you will reuse.
- [ ] **3. `AgentConfig` fields.**
  - _Read:_ §2 (all fields incl. `system_prompt`, `worklog_folder`, `max_retries_untill_switching_models`).
  - _Do:_ Rework `AgentConfig.py` to parse every §2 field with the documented default (retry budget **5**).
  - _Validate:_ Loading the §13a parent dict yields all fields; missing optionals fall back to defaults.
- [ ] **4. Delegate inheritance.**
  - _Read:_ §2 inheritance note, §7, §13a ("omit `models`… inherit").
  - _Do:_ In `AgentConfig`, inherit `models` + `max_retries_untill_switching_models` + shared `worklog_folder` from parent; keep `context_window_breakdown`/`system_prompt`/`cognitive_behavior`/`tools` per-agent.
  - _Validate:_ A delegate omitting `models` reports the parent's ladder but its **own** `context_window_breakdown`.
- [ ] **5. Config unit test.**
  - _Read:_ §15.1.
  - _Do:_ `tests/framework/test_agent_config.py`: defaults, inheritance, per-agent isolation.
  - _Validate:_ `pytest` green; asserts delegate keeps own budget, shares `worklog_folder`.
- [ ] **6. `ToolRegistry` + base.**
  - _Read:_ §6 (each tool carries `when`), §11 (`ToolRegistry.py`).
  - _Do:_ Ensure `Tool` base has `name`, `description`, `when`, async `run`/`stream`; registry dispatches by `type`.
  - _Validate:_ Registering a stub tool makes it discoverable and its `when` retrievable for pruning.
- [ ] **7. `SupabaseTool` (primary).**
  - _Read:_ §6 (Supabase row), §14 (`SupabaseVectorStore.async_query`).
  - _Do:_ Create `tools/SupabaseTool.py`: pgvector RPC via `async_query`; take `function_name`; leave `ranking` as a flag (path in Phase 2).
  - _Validate:_ Against a stub store, calling with `match_n8n_documents_bvms_neo` invokes `async_query` with that function name.
- [ ] **8. `ReadFileTool` (traversal-safe).**
  - _Read:_ §6 (`ReadFileTool` row), §10 (tool safety).
  - _Do:_ Rework `tools/ReadFileTool.py`: resolve paths under the run's `worklog_folder`; reject path traversal / absolute escapes.
  - _Validate:_ Read inside `worklog_folder` works; `../` and absolute paths raise (OWASP A01/A03).
- [ ] **9. `TodoTool`.**
  - _Read:_ §6 (`TodoTool` row), §5 (todo checklist).
  - _Do:_ Create `tools/TodoTool.py`: model **rewrites the whole list** `[{id, content, status: pending|in_progress|completed}]` into `<worklog_folder>/todo.md`.
  - _Validate:_ Writing a list then reading returns it verbatim; malformed status rejected.
- [ ] **10. `Router` (route by description).**
  - _Read:_ §7 (route by description), §14 (`_parse_agent_routing`).
  - _Do:_ Create `agents/Router.py`: choose delegate(s) by `description` via generalized `_parse_agent_routing` (`delegate:<agent_id>`); prune the **tool** menu by each tool's `when`.
  - _Validate:_ Given a code question, the code delegate is selected by its `description`.
- [ ] **11. `Reflector` (50% compaction).**
  - _Read:_ §8 (reflection), §14 (`KnowledgeCompression`, `IterationSummarizer`).
  - _Do:_ Rework `agents/Reflector.py` to compact `context_window.log` + `cognitive_index` to 50% (reusing the compression primitives).
  - _Validate:_ Over-budget input returns ~half-size output; `raw_worklog` untouched; pointers still resolve.
- [ ] **12. `ProgressiveAgentSLM` skeleton.**
  - _Read:_ §2, §11 (class responsibilities).
  - _Do:_ Rewrite `ProgressiveAgentSLM.py` constructor to own `ContextWindow`, `ModelChain`, tools, `delegates`, and the run's `Worklog`.
  - _Validate:_ Instantiating the §13a parent builds the object graph (2 delegates nested) without error.
- [ ] **13. Retrieve step (index-and-retrieve).**
  - _Read:_ §3 core loop, §8 ("read path").
  - _Do:_ Implement per-step retrieval: `cognitive_index.search(question)` → pull matching line ranges from `raw_worklog` into `context_window`.
  - _Validate:_ With seeded blocks, only relevant blocks enter `context_window` (irrelevant ones excluded).
- [ ] **14. Prompt assembly.**
  - _Read:_ §3 (prompt-assembly block), §5 (cognitive_behavior render), §6/§7 (description-routed delegates + when-pruned tools).
  - _Do:_ Build the four-tier prompt: system (`system_prompt` + `cognitive_behavior` `when→then` + delegate descriptions + pruned tool menu) + awareness + retrieved context + question.
  - _Validate:_ Rendered prompt contains the `cognitive_behavior` rules and only the pruned tool menu; each tier ≤ its fraction of `max_tokens`.
- [ ] **15. Model call + streaming answer.**
  - _Read:_ §4 (selection), §14 (`AssistantOrchestra.stream`, `create_chat_backend`).
  - _Do:_ Call the `ModelChain`-selected model; stream chunks as an async generator of `str`; cap output at the answer-remainder budget into `response_window`.
  - _Validate:_ A stub model yields chunks that stream out; output never exceeds the answer-remainder budget.
- [ ] **16. Block flush.**
  - _Read:_ §8 ("write path, per block").
  - _Do:_ On completion, flush `response_window` → `raw_worklog` (get line range) + `cognitive_index` (pointer), then **clear** `response_window`.
  - _Validate:_ After a step, the answer is in `raw_worklog`, indexed, and `response_window` is empty.
- [ ] **17. Quick self-eval → switch signal.**
  - _Read:_ §4 (retry budget), §14 (`AnswerEvaluator`), §16 #3.
  - _Do:_ After each iteration, run a quick self-eval; a "not good enough" verdict increments the `ModelChain` retry counter.
  - _Validate:_ Repeated bad verdicts trigger a model switch via Phase 0 item 12.
- [ ] **18. Recursion into delegates.**
  - _Read:_ §7 (hands-down / delivers), §2 inheritance.
  - _Do:_ Run a chosen delegate's own full loop; it writes finished blocks to the **shared** `raw_worklog` under its `agent_id` but returns only its **final** answer to the parent.
  - _Validate:_ Parent receives one final block; `raw_worklog` shows the delegate's full work under its `agent_id`.
- [ ] **19. Stop conditions.**
  - _Read:_ §4 (stopping / ladder exhaustion), §7 (depth).
  - _Do:_ Enforce ladder-exhaustion (per-model retry budget spent) + a recursion-depth cap.
  - _Validate:_ A never-satisfied stub stops once the last model's retry budget is spent; deep nesting stops at the recursion cap.
- [ ] **20. Wire the demo (vertical slice).**
  - _Read:_ §11 (`progressive_agent_slm_demo.py`), §13b, §14 (`create_chat_backend`).
  - _Do:_ Build `progressive_agent_slm_demo.py`: construct the §13b agent → `create_chat_backend` → `uvicorn` on **8001**.
  - _Validate:_ Boot it, ask one multi-step question; observe streamed think/route/delegate/answer and a populated `<worklog_folder>/<run_id>/`.

---

## Phase 2 — Full tools, cognitive_behavior policies, model routing ⬜

_Goal: the complete tool catalog, declarative cognitive_behavior, ranking, live budget enforcement, and full-text log search._

- [ ] **1. Orient.**
  - _Read:_ §5 (cognitive_behavior), §6 (full tool catalog), §3 (budgets), §8 (read/compaction), §12 Phase 2.
  - _Do:_ List the seven remaining tools + the policy engine + ranking + budget + search deliverables.
  - _Validate:_ Each maps to a target file in §11.
- [ ] **2. `SearchFileTool`.**
  - _Read:_ §6 (`SearchFileTool` row), §14 (`FileHanlder`).
  - _Do:_ Create `tools/SearchFileTool.py`: search by name or content (+ optional `glob`), ripgrep-style; return `path + line + snippet`; resolve under `worklog_folder`.
  - _Validate:_ Seeded tree returns correct name/content hits; snippet + line number accurate.
- [ ] **3. Validate `SearchFileTool` traversal safety.**
  - _Read:_ §10 (tool safety).
  - _Do:_ Add traversal/absolute-escape rejection.
  - _Validate:_ Searching outside `worklog_folder` raises (OWASP A01/A03).
- [ ] **4. `WriteFileTool`.**
  - _Read:_ §6 (`WriteFileTool` row), §10 (safety), §14 (`FileHanlder`).
  - _Do:_ Create `tools/WriteFileTool.py`: overwrite-or-append write, resolve under `worklog_folder`, path-traversal rejection, optional `require_approval` (default false).
  - _Validate:_ Overwrite vs. append both work inside `worklog_folder`; escape rejected; `require_approval: true` gates the write.
- [ ] **5. `VectorMemoryTool`.**
  - _Read:_ §6 (`VectorMemoryTool` row), §14 (`SupabaseVectorStore` + `Embedding`), §16 #9.
  - _Do:_ Create `tools/VectorMemoryTool.py`: `recall(query, k)` (`function_name`) + `remember(text, tags?)` (`write_function_name`) over a Supabase memory table.
  - _Validate:_ `remember` then `recall` returns the item; a second process/run can recall it (cross-run).
- [ ] **6. `SkillTool` (progressive disclosure).**
  - _Read:_ §6 (`SkillTool` row), §10 (trusted-local only), §16 #10.
  - _Do:_ Create `tools/SkillTool.py`: parse `{id, description, when}` frontmatter from `skills_dir`; expose only those until `when` matches, then load the body.
  - _Validate:_ Body is hidden until matched; external/out-of-dir skill paths rejected (prompt-injection surface).
- [ ] **7. `GenerateDiagramTool`.**
  - _Read:_ §6 row, §5 (`visualize_diagram`).
  - _Do:_ Create `tools/GenerateDiagramTool.py` emitting Mermaid.
  - _Validate:_ Output parses as a valid ```mermaid block.
- [ ] **8. `RunPythonTool`.**
  - _Read:_ §6 row, §10 (autonomous-exec warning), §14 (`PythonCodeExecute`).
  - _Do:_ Create `tools/RunPythonTool.py` wrapping `PythonCodeExecute`; optional `require_approval` (default false); capture stdout/stderr.
  - _Validate:_ A snippet returns its stdout; `require_approval: true` gates execution.
- [ ] **9. `FileKnowledgeTool`.**
  - _Read:_ §9 (knowledge sources), §6.
  - _Do:_ Create `tools/FileKnowledgeTool.py` as a files-type knowledge source.
  - _Validate:_ It surfaces text-file content as retrievable context.
- [ ] **10. Register + prune all tools.**
  - _Read:_ §6 (menu pruning), §7.
  - _Do:_ Register every tool in `ToolRegistry`; confirm each exposes a `when` used by the `Router` pruner.
  - _Validate:_ For a given step, only `when`-matching tools appear in the assembled menu.
- [ ] **11. `CognitiveBehavior` engine.**
  - _Read:_ §5 (render each iteration + todo), §11 (`CognitiveBehavior.py`).
  - _Do:_ Create `CognitiveBehavior.py`: render `cognitive_behavior` `when → then` rules into the system prompt every iteration; also surface them as the todo checklist.
  - _Validate:_ The prompt contains each rule as "When …, then …".
- [ ] **12. Baseline policies.**
  - _Read:_ §5 (recommended set).
  - _Do:_ Ship `deep_think`, `double_check`, `visualize_diagram`, `say_no`.
  - _Validate:_ Config with these renders all four; ids unique.
- [ ] **13. Policy behavior.**
  - _Read:_ §5, §14 (`AnswerEvaluator`).
  - _Do:_ Wire `double_check` to re-iterate on gaps and `say_no` to refuse when the KB is empty.
  - _Validate:_ Empty-KB question yields an honest "not available" (no hallucination); a gap triggers one more iteration.
- [ ] **14. Supabase ranking path.**
  - _Read:_ §6 (`ranking`), §14 (`RagAssistant.stream` parallel `DocumentRanking`).
  - _Do:_ When `ranking: true`, re-rank retrieved chunks with parallel `DocumentRanking` batches.
  - _Validate:_ Ranking on vs. off changes chunk order; latency stays bounded (batched, not serial).
- [ ] **15. Live budget enforcement.**
  - _Read:_ §3 (budgets), §12 Phase 2 budget note.
  - _Do:_ In the live loop, measure tokens (`tokens.py`), trim each tier, apply cascade-on-zero.
  - _Validate:_ Assert every assembled request ≤ selected model `max_tokens` across a multi-iteration run.
- [ ] **16. Compaction under load.**
  - _Read:_ §8 (progressive reflection).
  - _Do:_ Trigger real 50% compaction mid-run when `current_working_attention + cognitive_reflection_behavior` exceed budgets.
  - _Validate:_ Working windows shrink ~50%; answers still cite detail recovered from `raw_worklog`.
- [ ] **17. `LogSearch` (FTS5).**
  - _Read:_ §8 (`<worklog_folder>/index.db`), §17, §11 (`LogSearch.py`).
  - _Do:_ Create `logging/LogSearch.py`: SQLite FTS5 over `raw_worklog` + `cognitive_index`; `search()` + CLI over all runs.
  - _Validate:_ CLI query returns the run and correct line ranges for a known term.
- [ ] **18. Native + prompted tool-calling.**
  - _Read:_ §10 (tool-call protocol).
  - _Do:_ Support native Ollama `/api/chat` tool-calling when available, with a prompted-JSON + robust-parser fallback.
  - _Validate:_ Same tool fires via both paths on a capable and a non-capable stub model.
- [ ] **19. Cross-tool integration.**
  - _Read:_ §6, §7.
  - _Do:_ Run a scenario exercising Supabase → Write → Todo → Diagram in one iteration.
  - _Validate:_ Each tool's block lands in `raw_worklog` under the right `actor` (§17).
- [ ] **20. Phase-2 end-to-end.**
  - _Read:_ §15.3.
  - _Do:_ Run the demo with all tools + policies enabled on a multi-step BVMS question.
  - _Validate:_ Every tool callable, a Mermaid diagram emitted, ranking applied, budgets never exceeded, `LogSearch` CLI finds the run.

---

## Phase 3 — Config loader (JSON + Python) ⬜

_Goal: build the whole agent tree from `example.json` (or a Python dict) with schema validation and delegate inheritance — no code change to add/remove agents._

- [ ] **1. Orient.**
  - _Read:_ §2 (object), §11 (`config/`), §13 (JSON + Python), §13a (inheritance note).
  - _Do:_ List the loader responsibilities: parse → validate → inherit → build tree.
  - _Validate:_ You can point to the single place inheritance will live (`load.py`).
- [ ] **2. Reconcile the canonical config.**
  - _Read:_ [example.json](example.json), §11 (`src/framework/example.json` live copy), §13a.
  - _Do:_ Decide the live copy path and align it field-for-field with §13a.
  - _Validate:_ `example.json` diff against §13a is empty.
- [ ] **3. Schema — core fields.**
  - _Read:_ §2 (types + required), §11 (`schema.json`).
  - _Do:_ Write `config/schema.json`: required `agent_id`, `description`, ≥1 `model`; type each field (`system_prompt` str, `worklog_folder` str, `max_retries_untill_switching_models` int, `context_window_breakdown` fractions, etc.).
  - _Validate:_ Schema lints as valid JSON Schema.
- [ ] **4. Schema — recursion.**
  - _Read:_ §7 (delegate = full agent).
  - _Do:_ Add a recursive `$ref` so each `delegates[]` entry is itself an agent.
  - _Validate:_ The two-level §13a tree validates through the recursive ref.
- [ ] **5. Schema — enums & unions.**
  - _Read:_ §4 (`platform`, `max_tokens`), §6 (tool `type`), §5 (policy shape).
  - _Do:_ Enforce `platform ∈ {ollama, open_router}`, tool `type` enum, `max_tokens: number | "auto"`, todo `status` enum.
  - _Validate:_ Valid values pass; a bad platform fails.
- [ ] **6. Validate canonical config.**
  - _Read:_ §13a.
  - _Do:_ Run the schema against `example.json`.
  - _Validate:_ Passes with zero errors.
- [ ] **7. Validate rejection.**
  - _Read:_ §2 (required), §4.
  - _Do:_ Feed a config missing `models` and one with a bad `platform`.
  - _Validate:_ Both fail with a message naming the offending field.
- [ ] **8. `load.py` — parse.**
  - _Read:_ §11 (`load.py`), §13b (Option A).
  - _Do:_ Implement `load_agent(path|dict)` → validate → build `AgentConfig` tree recursively.
  - _Validate:_ Loading `example.json` returns a 3-node tree (parent + 2 delegates).
- [ ] **9. `load.py` — inheritance.**
  - _Read:_ §2 inheritance note, §13a.
  - _Do:_ Apply parent→delegate inheritance of `models` + `max_retries_untill_switching_models` + shared `worklog_folder`; keep per-agent fields isolated.
  - _Validate:_ Delegates report the parent ladder + retry budget but their own `context_window_breakdown`/`system_prompt`/`tools`.
- [ ] **10. `load.py` — build objects.**
  - _Read:_ §11, Phase 1 (`ProgressiveAgentSLM`, `ToolRegistry`).
  - _Do:_ Instantiate `ProgressiveAgentSLM` from each `AgentConfig`, wiring tools via `ToolRegistry` and nesting delegates.
  - _Validate:_ The returned parent has 2 live delegate instances with their Supabase tools attached.
- [ ] **11. `load.py` — Python-dict parity.**
  - _Read:_ §13b (Option B).
  - _Do:_ Ensure a Python dict/kwargs path produces the same tree as the JSON path.
  - _Validate:_ JSON-loaded and dict-built trees compare equal (ids, budgets, tools, inheritance).
- [ ] **12. Friendly errors.**
  - _Read:_ §16 (author usability).
  - _Do:_ On validation failure, report the failing `agent_id` + field + reason.
  - _Validate:_ A broken delegate names itself in the error.
- [ ] **13. Place the live `example.json`.**
  - _Read:_ §11, §13a.
  - _Do:_ Write the canonical config to `src/framework/example.json`.
  - _Validate:_ `load_agent("src/framework/example.json")` succeeds.
- [ ] **14. Round-trip test (JSON).**
  - _Read:_ §15.2.
  - _Do:_ `tests/framework/test_load.py`: load `example.json`, assert tree shape + inheritance + tool wiring.
  - _Validate:_ `pytest` green.
- [ ] **15. Round-trip test (Python).**
  - _Read:_ §13b.
  - _Do:_ Build Option B in code; assert equivalence to the JSON tree.
  - _Validate:_ Equality assertion passes.
- [ ] **16. Fraction-sum guard.**
  - _Read:_ §3 (fractions sum < 1), §13a.
  - _Do:_ Add a load-time check that each agent's `context_window_breakdown` fractions sum **< 1** (leaving room for the answer).
  - _Validate:_ Canonical config (0.025 + 0.325 + 0.525 = 0.875) passes; fractions summing ≥ 1 fail the guard.
- [ ] **17. Wire loader into the demo.**
  - _Read:_ §13b (Option A).
  - _Do:_ Switch `progressive_agent_slm_demo.py` to `load_agent("src/framework/example.json")`.
  - _Validate:_ Demo boots on 8001 from the JSON alone.
- [ ] **18. Authoring README.**
  - _Read:_ §2, §5, §6, §7 (author-facing behavior).
  - _Do:_ Document every field, defaults, inheritance, description-based routing, and each tool shape.
  - _Validate:_ A newcomer can add a third delegate by editing only JSON.
- [ ] **19. Defaults-only example.**
  - _Read:_ §2 (defaults), §12 Phase 3.
  - _Do:_ Add a minimal single-agent config (no delegates, no optional budgets) to exercise the default path.
  - _Validate:_ It loads and runs using all defaults (retry budget 5, awareness 0.025).
- [ ] **20. Phase-3 acceptance.**
  - _Read:_ §15.2.
  - _Do:_ From a fresh checkout, load `example.json`, boot the demo, ask a question; then add a delegate via JSON only.
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
- [ ] **3. Config/inheritance tests.**
  - _Read:_ §2 inheritance, §15.1.
  - _Do:_ Assert delegate omitting `models`/retry budget inherits them, shares `worklog_folder`, keeps own `context_window_breakdown`/`response_window`.
  - _Validate:_ `pytest` green.
- [ ] **4. Budgeting tests.**
  - _Read:_ §3, §15.1.
  - _Do:_ Cover trim, cascade-on-zero donation, and auto token inference.
  - _Validate:_ Each rule asserted independently.
- [ ] **5. Cognitive-index compaction tests.**
  - _Read:_ §3, §8, §17.
  - _Do:_ Append N blocks → `compact(0.5)` → assert line-range integrity (every surviving pointer resolves) and `raw_worklog` immutability.
  - _Validate:_ Byte-compare `raw_worklog` before/after == equal.
- [ ] **6. Model-ladder tests.**
  - _Read:_ §4, §16 #3–#4, §15.1.
  - _Do:_ Assert the model switches after **5** combined retries (quality + infra on one counter), success-reset to top, ladder-exhaustion abort.
  - _Validate:_ Quality and infra failures share the one counter.
- [ ] **7. Router pruning tests.**
  - _Read:_ §7, §15.1.
  - _Do:_ Assert delegates are selected by `description`; `delegate:<agent_id>` parses; only `when`-matching tools enter the menu.
  - _Validate:_ Code vs. domain question route to the right delegate.
- [ ] **8. Supabase tool tests.**
  - _Read:_ §6, §14, §15.1.
  - _Do:_ Assert `async_query` called with the configured `function_name`; ranking path batches `DocumentRanking`.
  - _Validate:_ Mocked store records the exact call.
- [ ] **9. Four-file worklog tests.**
  - _Read:_ §8, §15.1.
  - _Do:_ Assert append/read behind one writer; parallel delegate blocks don't interleave; `response_window` flush→clear.
  - _Validate:_ Concurrency test shows whole, ordered blocks.
- [ ] **10. Logging + FTS round-trip.**
  - _Read:_ §8, §17, §15.1.
  - _Do:_ Assert JSONL block events written and `LogSearch` finds them.
  - _Validate:_ Search returns the seeded run + line ranges.
- [ ] **11. File-tool traversal-safety tests.**
  - _Read:_ §10 (OWASP A01/A03).
  - _Do:_ Assert Read/Search/Write reject `../` and absolute escapes; stay within `root`.
  - _Validate:_ Traversal attempts raise; in-root ops succeed.
- [ ] **12. Integration smoke.**
  - _Read:_ §15.2.
  - _Do:_ Load `example.json` with the stub model; assert tree builds, parent routes by description, delegate calls Supabase + writes under its `agent_id`, `cognitive_index ≤` budget, all four `worklog` files exist, FTS finds the run.
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
  - _Validate:_ `raw_worklog` line ranges stay consistent and every `cognitive_index` pointer resolves.
- [ ] **18. Resolve open questions.**
  - _Read:_ §16 (#7 token measurement, #8 index summaries, #9 VectorMemory store, #10 `worklog_folder` lifecycle).
  - _Do:_ Make each decision and flip the `_TBD_` rows to a resolution.
  - _Validate:_ [planning.md](planning.md) §16 has no remaining `_TBD_`.
- [ ] **19. CI wiring.**
  - _Read:_ §15, `requirements.txt`.
  - _Do:_ Add a `pytest` task/target and (optionally) coverage over `src/framework/`.
  - _Validate:_ One command runs the whole suite green.
- [ ] **20. Phase-4 acceptance.**
  - _Read:_ §15.3, §12 (statuses).
  - _Do:_ Run the full suite + the manual §15.3 launch; then update §12 phase statuses to ✅ and bump the footer date.
  - _Validate:_ Green suite **and** a live multi-step BVMS answer with searchable logs; plan statuses reflect reality.

---

_Companion to [planning.md](planning.md). Last updated: 2026-07-29._
