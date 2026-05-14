# Phase 7 — Incremental Re-Learning (MR-Triggered)

## Status: ⏳ NOT STARTED

**Purpose:** Enable efficient re-processing when code changes are merged. Instead of re-running the full pipeline on the entire codebase (hundreds of files), only the changed files and their dependents are re-indexed, re-documented, re-enriched, and re-inserted. This keeps the knowledge base fresh without hours of reprocessing.

---

## Files to Modify

| File                                      | Action                                                                       |
| ----------------------------------------- | ---------------------------------------------------------------------------- |
| `src/CSharpManifest.py`                   | Already planned in Phase 1 — extend with `reset_file()`, `get_dependents()`  |
| `src/agents/tools/SupabaseVectorStore.py` | Already extended in Phase 5 — `delete_by_metadata()`                         |
| `src/CSharpCodebaseWorkflow.py`           | Extend: add `get_changed_files_from_git()`, `reset_files_for_reprocessing()` |
| `code_learn_csharp.py`                    | Extend: add `--mode=incremental`, `--changed-files` flag                     |

---

## Design Details

### 7.1 — How Incremental Mode Works

```
Trigger → Identify changed files → Expand to dependents → Reset manifest → Re-run Phases 1–5
```

**Step 1 — Identify changed files:**

Option A (automatic): Read from git

```bash
git -C {CSHARP_CODEBASE_PATH} diff --name-only origin/main HEAD
```

Option B (manual): Pass a list via CLI

```bash
python code_learn_csharp.py --mode=incremental \
  --changed-files "Core/Business/VoyageManagement/Voyage/CreateVoyage.cs,Core/Domain/VoyageManagement/Entities/VoyageEntity.cs"
```

Both return a list of relative file paths.

**Step 2 — Expand to dependents:**

For each changed file:

1. Look up its `class_name` in `csharp_index.json`
2. Find all files in `used_by[class_name]`
3. For `is_critical=true` files: also include files in the same domain module cluster (because workflow synthesis docs will need regeneration)
4. Deduplicate the full expanded set

This expansion is critical: if `VoyageEntity` changes, the 30+ handlers that use it also need re-documentation to reflect the change.

**Step 3 — Reset manifest:**

For each file in the expanded set:

- Set `phase = "unprocessed"` in `csharp-manifest.json`
- Do NOT delete the old generated docs yet (keep as backup)

**Step 4 — Re-run Phases 1–5 for the affected set only:**

The pipeline already supports this natively via manifest phase checks — files at `phase="unprocessed"` are picked up and processed; files at later phases are skipped.

After phases 1–5 complete:

- Old generated docs are overwritten with new ones
- Old Supabase rows are deleted before new ones are inserted (via `delete_by_metadata`)

---

### 7.2 — Workflow Synthesis Invalidation

When a file that belongs to a critical workflow cluster is changed, the corresponding Phase 4 workflow docs are also stale. The incremental runner handles this by:

1. Detecting which workflow clusters contain any of the changed files
2. Deleting the corresponding `csharp-docs/workflows/{module}/` files
3. Re-running `synthesize_workflow_documents()` for those clusters only

---

### 7.3 — CLI Interface

```bash
# Incremental mode — auto-detect changed files from git (compares HEAD vs origin/main)
python code_learn_csharp.py --mode=incremental

# Incremental mode — manually specify changed files
python code_learn_csharp.py --mode=incremental \
  --changed-files "Core/Business/VoyageManagement/Voyage/CreateVoyage.cs"

# Incremental mode — skip git detection, use a file list from stdin
git diff --name-only origin/main HEAD | python code_learn_csharp.py --mode=incremental --from-stdin

# Full re-learn (wipes manifest and re-runs everything)
python code_learn_csharp.py --mode=full --phase all

# Run a specific phase only (for debugging / partial re-runs)
python code_learn_csharp.py --phase document
python code_learn_csharp.py --phase enrich
python code_learn_csharp.py --phase synthesize
python code_learn_csharp.py --phase insert
```

---

### 7.4 — GitLab CI Integration (Optional — Future)

To wire incremental re-learning into the GitLab MR pipeline, add a job to `.gitlab-ci.yml` in the BVMS backend repo:

```yaml
# .gitlab-ci.yml (in bbc-bvms-net-back-end-modular)
stages:
  - build
  - test
  - knowledge-sync # ← new stage

update-rag-knowledge:
  stage: knowledge-sync
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: always
  script:
    - cd /path/to/ai-c4y
    - pip install -r requirements.txt
    - python code_learn_csharp.py --mode=incremental --from-stdin <<< "$CI_MERGE_REQUEST_DIFF_BASE_SHA"
  allow_failure: true # Knowledge sync failure should not block deployment
```

This is optional and not required for initial release. Start with manual invocation.

---

### 7.5 — `get_dependents()` Logic in `CSharpManifest.py`

```python
def get_dependents(self, file_path: str, index: dict) -> list[str]:
    """
    Given a changed file path, return all files in the index that
    reference its class_name. Used to expand the re-processing scope.
    """
    file_entry = index["files"].get(file_path, {})
    class_name = file_entry.get("class_name", "")
    if not class_name:
        return []
    used_by = index.get("used_by", {}).get(class_name, [])
    return used_by
```

---

## Estimated Impact by Change Type

| Changed File Type                    | Typical # Dependents  | Re-process Time |
| ------------------------------------ | --------------------- | --------------- |
| A single Handler (leaf node)         | 1–3 (controller only) | < 5 min         |
| A Service used by many handlers      | 10–30 handlers        | 15–30 min       |
| A Domain Entity (e.g., VoyageEntity) | 20–50+ files          | 30–60 min       |
| Core Infrastructure (DataContext)    | Near-entire codebase  | Run full mode   |

If expanded set exceeds 50 files, prompt user to confirm before proceeding:

```
⚠️  Incremental expansion affects 73 files. This is large.
   Consider running --mode=full instead.
   Continue? [y/N]
```

---

## Verification

- [ ] Modify one leaf handler file in the C# codebase (e.g., add a comment)
- [ ] Run `python code_learn_csharp.py --mode=incremental`
- [ ] Verify only that file (and 1–3 dependents) are reset in manifest
- [ ] Verify old Supabase rows for that file are deleted
- [ ] Verify new rows are inserted with updated content
- [ ] Modify `VoyageEntity.cs` — verify 20+ dependents are included in expanded set
- [ ] Verify threshold warning appears when expanded set > 50 files
- [ ] Verify `--changed-files` flag correctly limits scope to specified files

---

## What Was Done

_(Fill in after completion)_
