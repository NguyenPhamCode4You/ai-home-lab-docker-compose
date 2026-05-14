# Phase 5 — Supabase Insertion

## Status: ⏳ NOT STARTED

**Purpose:** Take all generated documents (Phase 3 enriched per-file docs + Phase 4 workflow synthesis docs) and insert them into the Supabase vector store `n8n_documents_bvms_code`. This reuses the existing insertion infrastructure from `CodeDocumentWorkflow.py` and `RagWorkflow.py` with no major changes.

---

## Files to Modify

| File                                      | Action                                  |
| ----------------------------------------- | --------------------------------------- |
| `src/agents/tools/SupabaseVectorStore.py` | Extend: add `delete_by_metadata()`      |
| `src/CSharpCodebaseWorkflow.py`           | Extend: add `insert_csharp_knowledge()` |

---

## Design Details

### 5.1 — Two Insertion Strategies (Already Exist in Project)

**Strategy A — Per-file enriched docs → `insert_code_documents()` (from `CodeDocumentWorkflow.py`)**

Used for: `csharp-docs/enriched/**/*.md`

The existing `insert_code_documents()` already handles this format correctly. It:

1. Splits the doc on `**Explanation**` boundary → stores code snippet as `content`, explanation as `summarize`
2. Extracts keywords from the code snippet
3. Stores `metadata: { file_name, section, keywords }`

This strategy preserves the code/explanation split, making retrieval more precise.

**Strategy B — Workflow/architecture docs → `insert_sentences()` (from `RagWorkflow.py`)**

Used for: `csharp-docs/workflows/**/*.md`

The existing `insert_sentences()` treats these as markdown knowledge documents. It:

1. Splits on markdown headers (`split_markdown_header_and_content`)
2. Compresses each section into a summary
3. Extracts keywords
4. Stores `metadata: { file_name, section, keywords }`

---

### 5.2 — `delete_by_metadata()` — New Method on `SupabaseVectorStore`

Required to support incremental re-learning (Phase 7) and safe re-insertion. Deletes existing rows by a metadata field value before re-inserting updated content.

```python
def delete_by_metadata(self, table_name: str, metadata_key: str, metadata_value: str) -> int:
    """
    Deletes all rows where metadata->>'{metadata_key}' = '{metadata_value}'.
    Returns count of deleted rows.
    Uses Supabase REST filter: ?metadata->>'file_name'=eq.{value}
    """
    response = requests.delete(
        f"{self.url}/rest/v1/{table_name}",
        headers=self.headers,
        params={ f"metadata->>{metadata_key}": f"eq.{metadata_value}" }
    )
    if response.status_code not in (200, 204):
        raise Exception(f"Failed to delete: {response.status_code}, {response.text}")
    # Supabase returns deleted count in Prefer: return=representation header
    return len(response.json()) if response.text else 0
```

---

### 5.3 — `insert_csharp_knowledge()` in `CSharpCodebaseWorkflow.py`

```
Input:  enriched_folder, workflows_folder, table_name, manifest
Output: Rows inserted into Supabase n8n_documents_bvms_code

Algorithm:
1. Load manifest
2. --- Enriched per-file docs ---
3. Collect all .md files in enriched_folder at phase="enriched" (not yet "inserted")
4. For each file:
   a. Delete existing rows for this file_name (idempotency guard)
   b. Call existing insert_code_documents(src_folder_path=file, table_name=table_name)
   c. Update manifest: phase="inserted"
5. --- Workflow docs ---
6. Collect all .md files in workflows_folder (no manifest phase check — always re-insert)
7. For each file:
   a. Delete existing rows for this file_name
   b. Call existing insert_sentences(src_folder_path=file, table_name=table_name)
8. Log total rows inserted
```

**Metadata stored per row:**

```json
{
  "file_name": "GetVoyageById",
  "section": "1. Handle — load voyage from database",
  "keywords": "GetVoyageById, Handle, VoyageEntity, DataContext, AsNoTracking, ApiException",
  "source_type": "code_file",          ← new field to distinguish from workflow docs
  "architecture_layer": "Business",
  "is_critical": false
}
```

The `source_type` field (`code_file` vs `workflow_doc`) allows the RAG assistant to optionally filter its searches.

---

### 5.4 — Insertion Order

Insert in this order so that the most searched content (critical workflow docs) benefits from full keyword extraction quality:

1. `BVMS_Architecture_Overview.md` (anchor doc)
2. `*_CRITICAL_deep_dive.md` files (highest retrieval value)
3. Other workflow docs
4. Enriched per-file docs (Domain entities first, then Business, Infrastructure, API)

---

## Verification

- [ ] Run Phase 5 on 5 enriched files
- [ ] Verify rows appear in Supabase `n8n_documents_bvms_code` table
- [ ] Verify `metadata.file_name` matches the source file name
- [ ] Verify `metadata.section` matches a real section header from the doc
- [ ] Query Supabase: `select count(*) from n8n_documents_bvms_code` — verify count grows
- [ ] Run Phase 5 again — verify `delete_by_metadata` removes old rows before re-inserting (no duplicates)
- [ ] Run insertion for workflow docs — verify `source_type = "workflow_doc"` in metadata
- [ ] Run full Phase 5 — verify manifest updated to `phase="inserted"` for all files

---

## What Was Done

_(Fill in after completion)_
