# Phase 3 — Cross-Reference Enrichment (Reflection Pass)

## Status: ⏳ NOT STARTED

**Purpose:** Re-read every generated Phase 2 doc and enrich it with two additional sections: a full `# Impact Scope` analysis (replacing the placeholder) that explains what breaks if this file changes, and a `# Used By` section listing all known callers. Then identify **critical business files** and tag them for deeper synthesis in Phase 4.

---

## Files to Create / Modify

| File                                 | Action                                       |
| ------------------------------------ | -------------------------------------------- |
| `src/agents/CSharpImpactAnalyzer.py` | Create                                       |
| `src/CSharpCodebaseWorkflow.py`      | Extend: add `enrich_with_cross_references()` |

---

## Design Details

### 3.1 — Model Selection Strategy

Same rule as Phase 2, but inputs are now the Phase 2 doc (text) + caller list (text) — not raw `.cs` source:

| Input size                                 | Model                                |
| ------------------------------------------ | ------------------------------------ |
| Doc + callers combined `<= 6000 chars`     | `Ollama(model=OLLAMA_GENERAL_MODEL)` |
| Doc + callers combined `> 6000 chars`      | `OpenRouter(model="qwen/qwen3-32b")` |
| File tagged as `is_critical=true` in index | Force cloud regardless               |

---

### 3.2 — `CSharpImpactAnalyzer.py`

A `Task` subclass. Prompt receives two inputs:

- `{context}` = the Phase 2 markdown doc for this file
- `{question}` = JSON list of caller file paths + their class names from `used_by`

**Prompt generates:**

```markdown
# Impact Scope

**Impact Rating:** [Low | Medium | High | Critical]

**Impact Justification:**
[1-2 sentences explaining WHY this rating was assigned]

**What breaks if this file changes:**

1. [Specific handler / flow / business operation that depends on this]
2. [Another dependent]
   ...

**Affected Business Areas:**

- VoyageManagement: [how affected]
- Finance: [how affected]
  ...

**Safe to modify:** [Yes / With caution / Requires full regression test]

# Used By

[Formatted list from the used_by index — grouped by architecture layer]

**Business Layer (Handlers):**

- `GetVoyageById.cs` — reads this entity directly
- `CreateVoyageFromEstimate.cs` — creates an instance of this entity

**Infrastructure Layer:**

- `DataContext.cs` — has a DbSet for this entity
- `MappingProfile.cs` — maps this entity to DTOs

**API Layer:**

- `VoyagesController.cs` — exposes endpoints that use this entity via handlers
```

---

### 3.3 — Critical File Detection

During enrichment, the analyzer also scores each file for **criticality** based on:

| Signal                                                                                              | Score weight |
| --------------------------------------------------------------------------------------------------- | ------------ |
| `used_by` count > 20 files                                                                          | +3           |
| `architecture_layer = Domain` AND entity is `VoyageEntity`, `ShipmentEntity`, `EstimateEntity`      | +3           |
| `file_type = Handler` AND `handler_verb` in `[Calculate, Complete, Create]`                         | +2           |
| Impact Rating returned as `Critical` or `High`                                                      | +2           |
| File name contains any of: `Voyage`, `Estimate`, `ProfitAndLoss`, `Calculate`, `Finance`, `Payment` | +1           |

Files with **total score >= 5** are tagged `"is_critical": true` in the manifest and in `csharp_index.json`. These files receive priority treatment in Phase 4 (dedicated workflow synthesis).

---

### 3.4 — `enrich_with_cross_references()` in `CSharpCodebaseWorkflow.py`

```
Input:  raw_folder, enriched_folder, index_path, manifest
Output: enriched .md files in enriched_folder/{same relative path}

Algorithm:
1. Load csharp_index.json and manifest
2. Collect all files at phase="documented"
3. Process in async batches of 10
4. For each file:
   a. Read Phase 2 .md doc from raw_folder
   b. Look up used_by entries from index for this file's class_name
   c. Build caller context string (capped at 3000 chars)
   d. Select model based on combined input size
   e. Run CSharpImpactAnalyzer.run(context=doc_content, question=caller_context)
   f. Replace "# Impact Scope\n[PLACEHOLDER — will be filled in Phase 3]"
      with the generated Impact Scope + Used By sections
   g. Save to enriched_folder/{relative_path}.md
   h. Score criticality, update manifest + index
   i. Update manifest: phase="enriched"
5. After full pass: save updated csharp_index.json with is_critical flags
6. Print summary: X files marked Critical, Y marked High
```

---

## Verification

- [ ] Run Phase 3 on 5 files from `Core/Domain/VoyageManagement/`
- [ ] Verify `# Impact Scope` section replaced placeholder with real analysis
- [ ] Verify `# Used By` section lists correct callers
- [ ] Verify `VoyageEntity.cs` is tagged `is_critical=true` (high used_by count)
- [ ] Verify `GetVoyageById.cs` has Low or Medium rating (it's a simple read)
- [ ] Verify `CalculateVoyage.cs` has High or Critical rating
- [ ] Verify combined input > 6000 chars used cloud model
- [ ] Re-run — verify already-enriched files are skipped

---

## What Was Done

_(Fill in after completion)_
