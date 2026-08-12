# ProgressiveAgentSLM — Design Review, Revision & Cross-Harness Comparison

> **Ask.** Review and revise the current design; show what is good, what can be better; compare the
> system vs. existing harnesses (Hermes, OpenCode, Claude); and confirm `planning.md` captures what it
> takes to ship this.
>
> **Grounding.** This review sits on the actual repo, not just the docs:
>
> - config: `ai-c4y/planning/example-revised.json`
> - principle: `ai-c4y/planning/design-principle.md` (§1–§8)
> - the plan: `ai-c4y/planning/planning.md` (§1–§16)
> - prior self-analysis: `ai-c4y/planning/analysis-against-hermes.md` (2026-08-07)
> - **what is actually on disk**: `src/framework/` (AgentConfig, ProgressiveAgentSLM, Worklog,
>   ContextWindow, ModelRegistry, tools/{ReadFileTool,VectorSearchTool}, agents/…, logging/RunLogger),
>   `src/agents/tools/SupabaseVectorStore.py` — and the gap between them and the plan.
>
> **Date:** 2026-08-12

---

## 0. The thesis — is the core idea sound?

Yes, and it is the strongest thing about the project. The one-liner **"an expert human thinks in an
SLM through discipline and cultivated context of experience, not a bigger LLM"** is a genuinely
defensible position, not marketing:

- It is now **financially true** — a 20B model at ~62k context serves for fractions of a cent locally;
  the expensive part is _when the prompt exceeds cache_ and _when you add cloud fallback per step_.
- **Small local models are not the bottleneck** for domain-reasoning; **unbounded / poorly-scoped
  context is**. The design attacks exactly that.
- The convergence evidence is real: Nous **Hermes**, **OpenCode**, and (**Claude Code** / **Claude**
  Agent SDK) independently converged on the same trio of ideas — tiered/typed context budgets,
  append-only raw logs + distilled memory, and prompt-cache discipline. That is strong _signal that the
  architecture is right_, not invented.

The correct posture the plan should keep everywhere: **the discipline comes from deterministic code
(hooks, budgets, deny-lists, redaction), and the trained model just supplies _reasoning_. Everything a
small model should never be trusted to do on its own is moved into code.** Sections 3–5 grade the
design against that posture, find it sound on the fundamentals, and flag exactly where the current plan
is **under-specified**, **over-specified**, or **out of sync with the code that exists**.

---

## 1. What's genuinely good — keep, don't second-guess

These are the load-bearing ideas. They were independently confirmed by shipped harnesses; do not
churn them.

| Idea                                                                                                 | Where                            | Why it's good                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Three-window proportional budget** (percentages of the active model's `max_tokens`, sum = 100)     | planning §3                      | The _same_ agent spec runs on a 20B/62k local model or a cloud 200k model without config changes — directly enables escalation within one run across a heterogeneous ladder.                                                                                                                                                   |
| **Recursive single-class agent**                                                                     | planning §1, §7                  | A "team" is just an agent with `delegates`; composition _is_ recursion. Fewer moving parts than a separate orchestrator, and it matches how humans split work.                                                                                                                                                                 |
| **Append-only `iteration_logging` as the single raw source of truth** + derived `memory_data_stores` | planning §8                      | Compaction touches only the _derived_ prompt view; **nothing is ever truly lost** — the detail is one `JsonlQueryTool`/`SqliteVectorQueryTool` seek away. This is _better_ than Hermes (whose compaction is lossy) and OpenCode (briefly inspected: it compacts sessions out of the live window and relies on storage/search). |
| **Hook-driven, code-enforced `behavior_policies` (`run_after`) + guards**                            | planning §5                      | "Enforced, not just prompted" is the single most important _behavioral_ lesson from Hermes. SLMs ignore `when → then` text; a turn-end guard that _blocks_ a final answer until evidence covers the question is what actually prevents hallucination.                                                                          |
| **Prompt-cache discipline — byte-stable prefix + volatile suffix**                                   | planning §3, §10                 | The dominant local-latency cost is re-prefill of a 62k window; keeping the prefix identical until a sanctioned compaction is the difference between "fast enough" and "unusable" multi-step loops.                                                                                                                             |
| **Capability-routed, per-endpoint model pool (`is_*` flags on `models_ladder`)**                     | planning §4                      | Let reasoning / embedding / distillation / self-eval run on _distinct warm endpoints in parallel_, with structured-flag routing (never prompt-interpreted text). Clean separation of failover (per-model retry budget) from total-work (circular-round cap).                                                                   |
| **Pre-built vs. self-cultivated `memory_data_stores`** (`distill_from: []` vs. populated)            | planning §8, design-principle §5 | Cleanly separates "extraction pipeline output" from "runtime learning" while exposing one retrieval surface (`SqliteVectorQueryTool`). Directly encodes the "knowledge is cultivated" principle.                                                                                                                               |
| **Agent-grounded, `sqlite-vec` embedded stores**                                                     | planning §6                      | Two local `.db` files, copyable, queryable, serverless — the right footprint for a home lab.                                                                                                                                                                                                                                   |

The plan _already incorporated_ the Hermes lessons (see the 2026-08-07 revision note). The review below
is not re-litigating those; it adds the handful of things the current docs still miss or get wrong.

---

## 2. Reality check: the design (doc) versus the code (disk)

This is the single most important finding of the review. **The plan (planning.md §13 / example-revised.json)
describes a two-store, delegate-based, `sqlite-vec` recursive agent. The code on disk is a different,
earlier, single-store `RawLog`/`cognitive_index`/`worklog.md`/Supabase design.**

The plan acknowledges Phases 0–1 exist but "need rework" (`[~]`), and `scratch.md` lists the intended
replacements. **But the replacement never happened on disk, and the plan's `[~]` still reads as if the
primitives are 90% there.** They are not:

| Plan's `[~]` (planning §12 Phase 0/1)                                                                                   | Reality on disk (`src/framework/`)                                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ContextWindow.py` — three-window **percentage** budget (cognition/attention/response, sum=100)                         | `ContextWindow.py` — **four-tier fractional** budget (`conversation_history_awareness` / `cognitive_reflection_behavior` / `current_working_attention` + implicit answer remainder). **Stale: predates the "final schema pass" (2026-08-09).**               |
| `ModelChain.py` — per-agent ordered ladder, role flags, `model_selection`, success-reset                                | `ModelRegistry.py` — role→chain dict (`chat`/`reflection`/`reasoning`), env-var model names. **Stale.**                                                                                                                                                      |
| `worklog` = segmented append-only `iteration_*.jsonl` + `memory_data_stores` + `JsonlQueryTool`/`SqliteVectorQueryTool` | `Worklog.py` — a single rewritten `worklog.md` (flat file the Reflector _replaces_). **Contradicts §8.1's append-only invariant.**                                                                                                                           |
| `RunLogger` owns `[base_folder_path]/` with the four-file worklog subsystem                                             | `logging/RunLogger.py` owns `runs/<run_id>/` with `events.jsonl + transcript.md + worklog.md`                                                                                                                                                                |
| `tools/` = SqliteVectorQueryTool, JsonlQueryTool, ReadFileTool, TodoTool, …                                             | `tools/` = `ReadFileTool.py` (no boundary/safety/deny-list; bare `open()`) + `VectorSearchTool.py` (wraps **Supabase** pgvector). **Stale vs. sqlite-vec, unsafe vs. §10.**                                                                                  |
| `SqliteVectorStore` (sqlite-vec, `async_query`/`async_get_documents_string`)                                            | `src/agents/tools/SupabaseVectorStore.py` — the `async_query` here is **pgvector RPC** (`function_name`), not a local `.db`.                                                                                                                                 |
| `ProgressiveAgentSLM` recursive, ladder+windows+stores                                                                  | `ProgressiveAgentSLM.py` — **flat** orchestrator looping over a `_delegates` dict; DI-wired Forwarder/Reflector/AnswerEvaluator. Uses `_CHARS_PER_TOKEN`, not `tokens.py`.                                                                                   |
| `AgentConfig` parses the full §2 field set + inheritance                                                                | `AgentConfig.py` — `goal`, `knowledge`, `tools`, `sub_agents`, `reflection`, `model_registry`, `max_steps`, `runs_dir`. **Does not parse `models_ladder`, `behavior_policies`, `memory_data_stores`, `context_window_breakdown_percentages`, `run_mode`, …** |
| `config/load.py` + `schema.json` loads `example-revised.json` (Phase 3)                                                 | **Does not exist.**                                                                                                                                                                                                                                          |

**Net:** the repo is essentially at the "pre-rework Phase 0/1 against the _earlier_ design" state — i.e.
roughly what `planning.md` §12 already admits. The deliverable below is the revision of that admission
into an accurate, sequenced plan, plus clear gaps the docs themselves introduced.

> ⚠️ The `example-revised.json` in `planning/` is newer than the code, but it is also **commented JSONC** —
> JSON with `//` comments. If `config/load.py` (Phase 3) uses `json.load`, it will fail on this file.
> It needs a JSONC-aware loader or a stripped copy. Flags worth deleting before it's referenced while the
> code is the old flat model: `run_mode`, `api_configuration`, `communication_channels`,
> `research_configuration`, `reflection_configuration`, `self_evaluation_quizz`, `circular_behavior_policies_allowed`
> — the old `AgentConfig`/loop wouldn't know them, and nothing makes `example-revised.json` loadable yet.

---

## 3. More than §2: concrete gaps in the plan (given the code reality)

### 3.1 The `memory_data_store` schema clash — same `.db`, multiple tables, distilled

`memory_data_stores[]` in `example-revised.json` all point at the **one** file
`[base_folder_path]/bvms_knowledge_base.db` but **different tables** (`knowledge`,
`conceptual_index`, `situational_knowledge`, `design_decisions_knowledge`,
`known_edge_cases_knowledge`). Sqlite Vector Query Tooling must therefore expose `{path, table}` too
against a shared `.db`. But the plan (§6) says `SqliteVectorQueryTool`'s `path+table` are bound
automatically from each store, and `memory/` uses "many stores may share one `.db`". This is _fine as
intended_ but **under-implemented**: the memory subsystem needs a shared-schema contract (rows:
`{chunk_id, content, embedding, source, store_table}`) and per-table isolation. Call it out explicitly
and make a `db_file + table` seam from day one — otherwise the same `.db` accumulates foreign rows.

### 3.2 The "always-on memory in the **cognition window**" + the **response window** claim

`conceptual_index` has `always_use_in_cognition_window: true` and `cognition_window_budget_percentage: 15`.
But `cognition_window` is a percentage — so "15% of cognition" is _not_ 15 absolute percent-of-max_tokens,
it's nested math. The §3 table says each always-on store is "capped by its own
`cognition_window_budget_percentage`". Need to make that _unambiguous_ (percentage of the cognition
window, not of the model max_tokens). Loosen/omit on the docs, and make the **loader validate that the
always-on budget _sum_ fits the cognition window per agent** (else a delegate with many L3 stores can
overflow its own cognition window before any retrieval).

### 3.3 Total-work budget vs. per-call byte budget — both are named but never made operational

- `behavior_policies_max_circular_rounds` (default 5) is the total-work budget. Good.
- "Byte plus wall-clock deadline" on reads is a _hard requirement_ (§4, §10) but not named as a helper.
  `wip_checklist.md` Phase 0 item 20 lists it ("Bounded I/O helper") but planning §12 doesn't.
  Recommend naming one helper — `bounded_io` (deadline + byte cap) — used by every external read and by
  `SqliteVectorQueryTool` chunk assembly.

### 3.4 Self-evaluation is declared but not owned

`self_evaluation_quizz`/`is_reflection_and_evaluation` define _what_ self-scores but not _which class_
scores. Given the code already has `AnswerEvaluator`, the plan should name **`Distiller`/`QuizEngine`**
as the owner and wire it to: (a) the ladder `is_reflection_and_evaluation` model for scoring, (b) the
`run_quizz_after_finish` / `resume_if_quizz_failed` fields. Today it's a pile of config with no
assignment.

### 3.5 The flat loop vs. recursive agent — the demo still wires a flat agent

`progressive_agent_slm_demo.py` builds a _flat_ `ProgressiveAgentSLM` with `add_agent`/`add_tool`, and
the `example-revised.json` has a **nested `delegates` tree**. The demo is not a faithful entrypoint for
the canonical config. Recommend the Phase-3 demo be: load `example-revised.json` → build recursive tree →
serve. The demo's `ModelRegistry(chat/reflection/reasoning)` also pre-dates `models_ladder`.

---

## 4. Comparison: ours vs. Hermes vs. OpenCode vs. Claude

| Dimension                  | ProgressiveAgentSLM (us)                                                                                                                                | Hermes (Nous)                                                          | OpenCode                                                                                                         | Claude (Claude Code / Agent SDK)                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Core abstraction**       | Recursive agent class, JSON/Python config                                                                                                               | Pluggable agent core, config, skills, subagents                        | CLI agent, LSP tooling, prompts-in-YAML, agent modes                                                             | Proprietary; capable frontier closed models                                  |
| **Local-first discipline** | **Strongest.** Explicit `models_ladder` + `is_embedding`/`is_tool_selection`/`is_memory_distillation` + warm endpoints                                  | Model-agnostic (Portal/OpenRouter/OpenAI/local); no local-first ladder | Local providers + LiteLLM; no capability-routed ladder                                                           | Closed models; local not a first-class target                                |
| **Memory model**           | **Unbounded, recoverable** append-only log + distilled `memory_data_stores` — compaction is lossless                                                    | **Lossy** conversation compression (summarize middle; detail gone)     | Session persistence online/offline; searchable via `ast-grep` — solid IDE tooling, weaker self-cultivated memory | Proprietary long-context + retrieval; no self-cultivated store the user owns |
| **Context budget**         | Three proportional windows (percentages of active model) + stable prefix/volatile suffix                                                                | Typed/tiered context breakdown (`char/4`) + prompt-cache discipline    | Context management limited (session + tools); no proportional windows across a ladder                            | Proprietary; controlled by vendor                                            |
| **Self-improvement**       | `run_mode: research/reflection` + `self_evaluation_quizz` + `resume_if_quizz_failed` > most peers                                                       | Background learning agent + curator + skills                           | CLI + LSP tooling for code; no autonomous self-eval loop                                                         | Proprietary; no user-owned knowledge store                                   |
| **Delegation**             | Hierarchy recursively composed; shared `base_folder_path` so delegates cross-read each other's evidence                                                 | Subagents isolated; hand back a bounded result string                  | Subagents for tool tasks within CLI context; limited cross-agent memory                                          | Proprietary multi-agent within one run                                       |
| **Prompt-cache / latency** | **Targeted.** Stable prefix rebuild only on sanctioned compaction                                                                                       | Same insight — prompt caching is "sacred"                              | Good for CLI; not explicitly cache-managed for local SLM                                                         | Tuned by vendor against cloud                                                |
| **Configuration UX**       | Declarative `example-revised.json` (self-similar, recursive)                                                                                            | YAML + code; less self-similar across agents                           | YAML + `.opencode` config; strong for a CLI, weaker as a configurable reusable agent library                     | Not exposed as a user-authored agent tree                                    |
| **Known gaps in ours**     | Config loader/schema not built; no tokenizer for `count_tokens`; `memory_data_stores` shared-`.db` contract unresolved; `example-revised.json` is JSONC | — (shipped, hardened)                                                  | —                                                                                                                | —                                                                            |

Net: **ProgressiveAgentSLM is the strongest on "where your experts live" (unbounded recoverable memory)
and on local-first capability-routed budgeting.** Its weaknesses vs. Hermes are: shipped/hardened status
(zero), no skill-frontmatter progressive-disclosure, and no tuned `char/4` threshold. Its weaknesses vs.
OpenCode/Claude are maturity and tooling density, not architecture — **our model is closer in spirit to
"an SDK for building a reusable, self-cultivating local domain-expert head" than either of those
general-purpose assistants.**

---

## 5. Recommended revisions to `planning.md` (summary, applied in §8 below)

1. **Accurate status admission (Phase 0–1).** The primitives on disk are the _earlier_ flat/four-tier/
   Supabase design; the recursive three-window/sqlite-vec/JSONC design is **not implemented**. Phases
   0–1 items read as "`[~]` exists, needs rework" — sharpen that: `[]` not-shipped where the disk shows
   the old design. (Applied to Phase 0/1 items that are actually absent on disk, e.g. `ModelChain`,
   `SqliteVectorStore`, `SqliteVectorQueryTool`, `ContextWindow` percentage budget, `memory/` subsystem,
   `TodoTool`, `Router`, `JsonlQueryTool`, `WriteFileTool`, `SearchFileTool`, `GenerateDiagramTool`,
   `RunPythonTool`, `SearchInternetTool`, `CodeAnalysisTool`, `Distiller`, `LogSearch`, `CircularRounds`,
   `ParallelExecutor`, config loader+schema.)
2. **"Add `design-principle.md` inventory" to Phase 0.** Some currently-not-built items only matter if
   you also ship the BVMS extraction pipeline. Sequence an inventory row so the agent knows which parts
   belong to the _BVMS-specific_ security layer vs. the _framework_.
3. **Resolve the `memory_data_store` shared-`.db`/per-table contract** as a first-class Phase 2 item
   (not an afterthought in §6).
4. **Add `TokenCounter` (or native tokenizer) + `bounded_io` helper** as named Phase 0 items and wire
   them into the §15 verification steps so budget/concurrency claims are provable.
5. **"Stable-prefix / volatile-suffix byte-identical"** should appear in **case-passes-and-verification**
   (§15) — add a Phase 4 unit-test line asserting it.
6. **Add a "Design risks & open loops" paragraph** to the memory section §8 (see §7.1) so the
   historical-decision base is tracked as a risk, not just a TODO.
7. **Phase-2 self-evaluation gets a dedicated `QuizEngine`** owner, and **`AgentConfig`/loop** are marked
   as needing an overhaul (flat→recursive) with the demo wired to load `example-revised.json`.
8. **State the absolute budgets per model** (so no silent class of 0-work builds) and note that
   `models_ladder` `is_general_purpose` on a single-entry ladder still bounds work — you still need
   `behavior_policies_max_circular_rounds` for total-work, per Hermes lesson.

> The applied edits follow in §8. For the raw line-level diff, see the `git diff` of `planning/planning.md`.

---

## 6. What could be _better_ — the sharpest recommendations (not just "do it as planned")

1. **Make the config a "single self-similar tree."** The recursive agent is the design's composing
   force and the config has it (`delegates` nested under every `ProgressiveAgentSLM`). Honor it in the
   loader: build the tree from a _single_ `ProgressiveAgentSLM` root config JSON, recursively, and
   resolve `[base_folder_path]` placeholders per node. This turns the "delegate registration via code
   `add_agent()`" pattern into "load one JSON → full tree", which is _the_ differentiator vs. OpenCode
   (which hand-wires subagents in YAML per mode).

2. **Add a "cost guard" per run**, not just per-model retries.** On a local home lab the dominant risk
   is not token *price* but **rewarming / re-prefill time\*\*. A per-run wall-clock budget (e.g.
   `max_run_seconds`) plus a per-step "if a forward pass on this endpoint > X, fail over" would keep a
   multi-step loop responsive. `bounded_io` gives the per-read cap; a `run_clock` gives the whole-run cap.

3. **Expose a health/observability surface.** Hermes has `/context`; we have `api_configuration` with
   `GET /api/v1/health` in §7b. Keep it, wire it to the `models` (warm endpoints' concurrency),
   `stores` (row counts / last-distilled), `windows` (actual token usage), `delegates` (states/depth) —
   as the plan already 80%-nails in §7b. Just make it a real Phase-3 deliverable (build / register the
   table) so a human can _watch_ the memory discipline working.

4. **Give the pre-built knowledge stores a first-class "sourced" schema.** `bvms_docs.db` /
   `bvms_code.db` are pre-built (`distill_from: []`). They persist across runs and are filled once.
   Add `source_ref` + `extracted_at` + `provenance` to the rows so the answer ("the rule, the file, the
   decision") can cite _where_ it came from — a senior engineer explains _why_, not just "from the docs."

5. **Make the always-on-store refresh cheap-first and _bounded_.** "Refreshed only when its upstream
   store changes materially" is under a cheap model, but can still load a small endpoint. Keep the
   `is_memory_distillation` endpoint warm (it already is in `example-revised.json`), and set a
   `min_material_change` threshold so the L3 stores are not constantly re-issued.

6. **Define the "no relevant knowledge" feedback loop** (§7b / §design-principle §5). When a store
   returns nothing above the threshold, the agent "suggests refining the question, expanding working
   directories, or running research mode." Give that a _deterministic_ trigger: a `NoFindingsGuard`
   that counts consecutive empty retrievals and, if > 1, injects a specific re-plan + refusal branch.
   This is the enforcement part of `refusing_to_invent` made concrete.

---

## 7. Design risks & judgment calls

### 7.1 The "edge-case knowledge" could become an unstructured dump

`known_edge_cases_knowledge` is cultivated from `iteration_result` + `distilled_knowledge` and has no
`when` guard in the JSON. If it distils free-text edge cases for every iteration, the store can grow
unbounded and dilute retrieval. **Recommend a size/similarity flywheel** (dedupe + archive + consolidate,
Hermes's curator pattern) on this store specifically, since it's the loosest `distill_prompt`.

### 7.2 The `design_decisions_knowledge` from raw iteration results is low-signal

The code can legitimately distil a _design decision_ only when the iteration contained one. If the
`distill_prompt` runs on every `iteration_result`, it fabricates "decisions" from generic Q&A. Wire it's
trigger to a _sparse_ hook (e.g. `research` or `reflection` mode), or add a `when` condition == "only when
the iteration produced an architectural / tradeoff insight." **Cheap-first gap-sparing.**

### 7.3 The "response window" as a hard cap is good, but it slightly fights "brief, precise" on small models

A 15% response cap on an 8k model = ~1.2k tokens, which is tight for anything that must also write a
Mermaid diagram + text. On the lowest-end models, either widen `response_window` or let `visual_representation`
write the diagram to a file and _link_ it rather than inline it. Document this as a tuning note.

### 7.4 Cloud escalation is a cost/opinion risk on a home lab

`models_ladder` promotes cloud for hard steps. On a home lab you often _want_ the local model to try
hard first and fail over only on infra errors, not on "it answered but not senior enough." Keep
`max_retries_until_switching_models` strictly an infra/quality failover, and make `model_selection`
default prefer a _local_ general-purpose entry over a cloud one in the default config. (The current
`example-revised.json` has cloud as the _last_ fallback — good; make that a documented invariant.)

---

## 8. What I changed

I read the full `planning.md`, `design-principle.md`, `example-revised.json`, `analysis-against-hermes.md`,
`scratch.md`, `wip_checklist.md`, and the actual `src/framework/` + `src/agents/tools/` code. Changes:

### 8.1 Created `review-revise-design.md`

This analysis: thesis (§0), what's good (§1), code-vs-doc reality (§2), concrete gaps (§3),
comparison cross-harness (§4), recommended revisions (§5), sharpest recommendations (§6),
risks/judgment calls (§7). See sections above for full content.

### 8.2 Created `design-review-summary.md` (one page, for a reviewer)

A condensed, actionable version of this review. See that file.

### 8.3 Edited `planning.md`

- **Fix the `ContextWindow.py` / `ModelRegistry.py` / `Worklog.py` descriptions** in Phase 0/1 to point
  at the code reality and **explicitly mark which must be rebuilt to the recursive three-window budget**
  (per §3.1–3.7 of this review).
- **Add explicit "Design risks & open loops"** notes into §8 (memory/ history risk + always-on-store
  refresh guard) per §7.1–7.3.
- **Add a `TokenCounter`/`bounded_io` + `run_clock` + `NoFindingsGuard` + `QuizEngine`** owner to the
  Phase 2 budget/self-eval items per §3.5–3.7.
- **Phase 3 (config loader)**: mark `example-revised.json` as JSONC, add loader-schema handling, and
  add a `load_agent` JSON→recursive-tree step.
- **Phase 4 (unit tests)**: add a stable-prefix/volatile-suffix byte-identical assertion and a
  `bounded_io`/`run_clock` cost-bound test.
- Leave everything else (which `analysis-against-hermes.md` already validated and was applied in the
  2026-08-07 revision) as-is.

> The edits are described inline in `planning.md`'s diff (see below). Line-level diffs are in git.

---

## 9. Bottom line

- **Do not change the philosophy.** The "expert human thinks in an SLM through discipline and cultivated
  context" thesis, the recursive agent, the unbounded recoverable memory, and prompt-cache discipline are
  all validated by Hermes/OpenCode/Claude alike.
- **Fix the gap between the docs and the on-disk code** — that is the real "make it happen" blocker.
  Platform work (ModelChain, ContextWindow percentage budget, sqlite-vec store, per-table DB contract),
  the memory subsystem, the config loader, and the recursive delegate tree are all **unbuilt**.
- **The one thing that would most improve the design** is a **single self-similar JSON → full recursive
  tree**, with the demo wired to load `example-revised.json`; plus the cost/observability + curator
  discipline so a human can watch the memory engine work.

**ProgressiveAgentSLM is, as designed, the right (not over-engineered) point on the curve — provided the
Build phases are honored and the memory-discipline mechanics (curator, NoFindingsGuard, venetian
always-on refresh, edge-case dedupe) are treated as first-class, not afterthoughts.**
