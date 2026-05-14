# Phase 1 — Codebase Indexing (Structural Extraction)

## Status: ⏳ NOT STARTED

**Purpose:** Walk every `.cs` file in the codebase (respecting `CSHARP_FOCUS_ONLY_FILES` / `CSHARP_IGNORE_FILES` filters), extract its structural metadata into a JSON index, and build a reverse-lookup (`used_by`) map that shows which files reference each class. This is a fast, low-cost pass — the output feeds every subsequent phase.

---

## Files to Create

| File                        | Location                                                      |
| --------------------------- | ------------------------------------------------------------- |
| `CSharpFileAnalyzer.py`     | `ai-c4y/src/agents/`                                          |
| `CSharpManifest.py`         | `ai-c4y/src/`                                                 |
| `CSharpCodebaseWorkflow.py` | `ai-c4y/src/` _(create skeleton, add `build_codebase_index`)_ |
| `code_learn_csharp.py`      | `ai-c4y/` _(entry point, `--phase index` mode)_               |

---

## Design Details

### 1.1 — `CSharpFileAnalyzer.py`

A `Task` subclass. Its prompt asks the model to extract structured JSON from a `.cs` file.

**Model selection logic (important):**

- File `<= 200 lines` → use local `Ollama(model=OLLAMA_CODE_MODEL)` (fast, free)
- File `> 200 lines` → switch to `OpenRouter` with a large-context cloud model (e.g., `qwen/qwen3-32b` or `google/gemini-flash-1.5`) to avoid local context window truncation

The line threshold `200` is the default. It can be overridden via `CSHARP_LARGE_FILE_LINE_THRESHOLD` env var.

**Extraction prompt target JSON:**

```json
{
  "class_name": "GetVoyageById",
  "namespace": "Core.Business.VoyageManagement.Voyage",
  "file_type": "Handler",
  "architecture_layer": "Business",
  "handler_verb": "Get",
  "methods": [
    {
      "name": "Handle",
      "return_type": "VoyageCrudDto",
      "is_public": true,
      "parameters": ["Request request", "CancellationToken cancellationToken"],
      "calls": ["context.Voyages", "mapper.Map", "throw ApiException"]
    }
  ],
  "using_imports": [
    "Core.Domain.VoyageManagement",
    "Core.Infrastructure.DbContext"
  ],
  "injected_services": ["DataContext", "IMapper"],
  "entities_referenced": ["VoyageEntity", "VoyageCrudDto"],
  "external_clients_used": [],
  "is_critical": false
}
```

**`file_type` values:** `Handler | Entity | Dto | Service | Controller | Validator | ExternalClient | Function | Middleware | Configuration | Other`

**`architecture_layer` values:** `Domain | Business | Infrastructure | API | ExternalClient | Functions | CronJobs`

If the LLM output is not valid JSON, the analyzer retries once with a stricter prompt. On second failure, logs the error and records `file_type: "Other"` with an empty methods list — never blocks the pipeline.

---

### 1.2 — `CSharpManifest.py`

Utility class wrapping `csharp-manifest.json`. Created/loaded at startup.

```python
class CSharpManifest:
    def load() -> dict
    def save(manifest: dict)
    def get_phase(file_path: str) -> str | None
    def set_phase(file_path: str, phase: str, extra: dict = {})
    def get_all_at_phase(phase: str) -> list[str]
    def reset_file(file_path: str)   # sets back to "unprocessed"
    def get_dependents(file_path: str, index: dict) -> list[str]  # reverse-lookup
    def compute_hash(file_path: str) -> str  # sha256 of file content
    def has_changed(file_path: str) -> bool  # compares stored hash vs current
```

---

### 1.3 — `CSharpCodebaseWorkflow.py` — `build_codebase_index()`

```
Input:  codebase_path, index_output_path, manifest
Output: csharp_index.json, updated manifest

Algorithm:
1. Walk all .cs files under codebase_path
2. Apply CSHARP_FOCUS_ONLY_FILES filter (if set)
3. Apply CSHARP_IGNORE_FILES filter (always)
4. For each file NOT yet at phase >= "indexed" in manifest:
   a. Count lines
   b. Select model: local Ollama if <= threshold, OpenRouter if >
   c. Run CSharpFileAnalyzer.run(context=file_content)
   d. Parse JSON result
   e. Append to index dict keyed by relative file path
   f. Update manifest: phase="indexed", hash, file_type, lines
5. Every 50 files: save checkpoint of index + manifest
6. After all files: build used_by reverse map
   - For each file A in index, scan ALL other files' content for mentions of A's class_name
   - used_by[class_name] = [relative_paths of files that reference it]
7. Save final csharp_index.json
```

**`csharp_index.json` structure:**

```json
{
  "files": {
    "Core/Business/VoyageManagement/Voyage/GetVoyageById.cs": { ...analyzer output... }
  },
  "used_by": {
    "GetVoyageById": ["APIs/OrderRequest/Controllers/VoyagesController.cs"],
    "VoyageEntity": ["Core/Business/VoyageManagement/Voyage/GetVoyageById.cs", "...30+ more"]
  },
  "stats": {
    "total_files": 480,
    "by_layer": { "Business": 210, "Domain": 120, "Infrastructure": 80, "API": 40, "ExternalClient": 30 },
    "by_type": { "Handler": 160, "Entity": 70, "Dto": 60, "Service": 40, "Controller": 25 },
    "generated_at": "2026-05-14T10:00:00Z"
  }
}
```

---

### 1.4 — `code_learn_csharp.py` — Entry Point

```bash
# Run Phase 1 only
python code_learn_csharp.py --phase index

# Run all phases
python code_learn_csharp.py --phase all

# Incremental mode (Phase 7)
python code_learn_csharp.py --phase all --mode incremental

# Focus on specific files (overrides env var for this run)
python code_learn_csharp.py --phase index --focus "**/VoyageManagement/**"
```

---

## Processing Order (Priority)

Process files in this order to maximise early knowledge value:

1. `Core/Domain/**` — Entities and DTOs first (everything references these)
2. `Core/Business/**` — Handlers and Services (core business logic)
3. `Core/Infrastructure/**` — DbContext, AutoMapper, Middleware
4. `APIs/**` — Controllers
5. `ExternalClients/**` — Adapters
6. `Functions/**` + `CronJobs/**` — Background jobs

---

## Verification

- [ ] Run `python code_learn_csharp.py --phase index --focus "**/VoyageManagement/**"`
- [ ] Verify `csharp_index.json` is created with correct `class_name`, `file_type`, `methods`
- [ ] Verify `used_by["VoyageEntity"]` contains 20+ referencing files
- [ ] Verify large files (> 200 lines) triggered cloud model (check logs)
- [ ] Verify ignored paths (`Migrations/`, `bin/`, `obj/`) are absent from index
- [ ] Run on full codebase, verify stats section counts are reasonable

---

## What Was Done

_(Fill in after completion)_
