# Phase 2 — Per-File Documentation

## Status: ⏳ NOT STARTED

**Purpose:** For every `.cs` file that reached `phase="indexed"`, generate a rich markdown document that explains its purpose, architecture layer, methods, and known dependencies. This is the largest phase and produces the raw per-file knowledge base that Phases 3 and 4 build upon.

---

## Files to Create / Modify

| File                                 | Action                                 |
| ------------------------------------ | -------------------------------------- |
| `src/agents/CSharpDocumentWriter.py` | Create                                 |
| `src/CSharpCodebaseWorkflow.py`      | Extend: add `write_csharp_documents()` |

---

## Design Details

### 2.1 — Model Selection Strategy

The same rule applies as Phase 1, but now the content being processed is the **full file + index context**, which can be even larger:

| File size                                | Model                                                      |
| ---------------------------------------- | ---------------------------------------------------------- |
| `<= 200 lines`                           | `Ollama(model=OLLAMA_CODE_MODEL)` — local, fast            |
| `> 200 lines`                            | `OpenRouter(model="qwen/qwen3-32b")` — large context cloud |
| Handler files with > 5 injected services | Force cloud regardless of line count                       |
| Critical business files (see §2.3)       | Force cloud regardless of line count                       |

The `CSHARP_LARGE_FILE_LINE_THRESHOLD` env var controls the 200-line cutoff.

---

### 2.2 — `CSharpDocumentWriter.py`

A `Task` subclass extending `CodeDocumentWriter`. The prompt is C#/CQRS-aware.

**Prompt template (key sections it instructs the model to generate):**

````
You are a senior .NET software architect documenting the BVMS C# backend codebase.
The codebase follows Clean Architecture with CQRS (MediatR), EF Core, and FluentValidation.

File info from index:
- file_type: {file_type}
- architecture_layer: {architecture_layer}
- namespace: {namespace}
- known_dependencies: {dependencies_from_index}
- known_callers: {used_by_from_index}

Generate a markdown document with EXACTLY these sections:

# General Purpose
One paragraph. What this file does and WHY it exists in the system.
Its role within the {architecture_layer} layer of CQRS/Clean Architecture.

# Architecture Layer
State: [Domain | Business | Infrastructure | API | ExternalClient | Functions]
Explain what responsibilities this layer has and how this file fits.

# Class: {ClassName}
Brief class-level description. Constructor dependencies. Any interface contracts implemented.

## 1. {MethodName} — {one-line purpose}
```csharp
{exact code snippet}
````

**Explanation**:
Detailed explanation: what this method does, what inputs it expects,
what it returns or what side-effects it produces, any important
business rules or conditions embedded in the logic.

(repeat ## N. for each public method)

# Dependencies

List each injected service and entity referenced, with a one-line note on WHY it is needed.

# Impact Scope

[PLACEHOLDER — will be filled in Phase 3]

Now document this file:
{context}

```

The `**Explanation**` delimiter is preserved intentionally — the existing `insert_code_documents()` in `CodeDocumentWorkflow.py` already splits on this boundary to store code and explanation as separate vector embeddings.

---

### 2.3 — `write_csharp_documents()` in `CSharpCodebaseWorkflow.py`

```

Input: codebase_path, index_path, output_folder="csharp-docs/raw/", manifest
Output: .md files in output_folder/{relative_path}/

Algorithm:

1. Load csharp_index.json and manifest
2. Collect all files at phase="indexed" (not yet "documented")
3. Sort by priority: Domain → Business → Infrastructure → API → ExternalClient
4. Process in async batches of 10 (not 20 — cloud API rate limits)
5. For each file:
   a. Read file content
   b. Count lines → select model
   c. Build index context: pull this file's entry + top-10 used_by entries (capped at 2000 chars)
   d. Run CSharpDocumentWriter.stream(context=file_content, question=index_context)
   e. Stream output to: output_folder/{relative_path_without_ext}.md
   f. Update manifest: phase="documented"
6. Every 10 files: flush manifest to disk (crash recovery)

````

**Output path example:**
- Source: `C:\Gitlab\...\Core\Business\VoyageManagement\Voyage\GetVoyageById.cs`
- Output: `csharp-docs/raw/Core/Business/VoyageManagement/Voyage/GetVoyageById.md`

**Idempotency:** If the `.md` already exists and manifest says `documented`, skip it. Re-run is safe.

---

### 2.4 — Batch Concurrency Details

```python
# Batch size: 10 files
# Within each batch: asyncio.gather (parallel)
# Between batches: 2 second sleep if using cloud model (rate limit guard)
# On cloud API error (429/503): exponential backoff, max 3 retries, then log + skip
````

---

## Verification

- [ ] Run Phase 2 on 5 files from `Core/Business/VoyageManagement/Voyage/`
- [ ] Verify each generated `.md` has all required sections: `General Purpose`, `Architecture Layer`, `Class:`, method entries with `**Explanation**`, `Dependencies`
- [ ] Verify `# Impact Scope` placeholder is present
- [ ] Verify output file saved at correct relative path under `csharp-docs/raw/`
- [ ] Verify large file (e.g., `DataContext.cs`) triggered cloud model — check log line
- [ ] Verify manifest updated to `documented` for processed files
- [ ] Re-run Phase 2 — verify already-documented files are skipped

---

## What Was Done

_(Fill in after completion)_
