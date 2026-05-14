# Phase 0 — Infrastructure Setup

## Status: ⏳ PENDING (Manual steps — do not automate)

This phase is entirely manual. No code is written or executed. The developer performs these setup steps once before running any phase.

---

## Steps to Complete Manually

### 0.1 — Environment Variables

Add the following keys to `ai-c4y/.env` and `ai-c4y/.env.example`:

```env
# C# Codebase RAG — Code Knowledge Agent
CSHARP_CODEBASE_PATH     = C:\Gitlab\bbc-bvms-net-back-end-modular
BVMS_CODE_TABLE_NAME     = n8n_documents_bvms_code

# --- File Filtering (optional) ---
# Comma-separated glob patterns. If set, ONLY files matching these patterns are processed.
# Leave empty to process entire codebase.
# Example: **/Voyage/**/*.cs,**/Estimate/**/*.cs
CSHARP_FOCUS_ONLY_FILES  =

# Comma-separated glob/path patterns to always skip.
# Example: **/Migrations/**,**/*.Designer.cs,**/obj/**,**/bin/**
CSHARP_IGNORE_FILES      = **/Migrations/**,**/*.Designer.cs,**/obj/**,**/bin/**,**/*.g.cs,**/AssemblyInfo.cs
```

**Notes on filtering:**

- `CSHARP_FOCUS_ONLY_FILES` — when non-empty, the entire workflow only processes files that match at least one of the provided patterns. Useful when you want to focus learning on a specific module (e.g., VoyageManagement only) before expanding to the full codebase.
- `CSHARP_IGNORE_FILES` — always applied regardless of focus. Skips generated files, migrations, and build artifacts which add noise without knowledge value.
- Both accept comma-separated `fnmatch`-style glob patterns evaluated against the file's path relative to `CSHARP_CODEBASE_PATH`.

---

### 0.2 — Supabase Table & RPC Function

Create a new table in Supabase (self-hosted or cloud) using the **same schema** as the existing `n8n_documents_bvms_neo` table.

```sql
-- Table
CREATE TABLE n8n_documents_bvms_code (
  id          bigserial PRIMARY KEY,
  content     text,
  metadata    jsonb,
  summarize   text,
  embedding   vector(768),   -- nomic-embed-text dimension
  embedding2  vector(768)
);

-- Vector search RPC (mirrors match_n8n_documents_bvms_neo)
CREATE OR REPLACE FUNCTION match_n8n_documents_bvms_code(
  query_embedding  vector(768),
  match_count      int DEFAULT 200,
  filter           jsonb DEFAULT '{}'
)
RETURNS TABLE (
  id        bigint,
  content   text,
  metadata  jsonb,
  summarize text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    n8n_documents_bvms_code.id,
    n8n_documents_bvms_code.content,
    n8n_documents_bvms_code.metadata,
    n8n_documents_bvms_code.summarize,
    1 - (n8n_documents_bvms_code.embedding <=> query_embedding) AS similarity
  FROM n8n_documents_bvms_code
  ORDER BY n8n_documents_bvms_code.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

---

### 0.3 — Output Folder Structure

Create the following folder structure inside `ai-c4y/` (or wherever you prefer — set in env/config):

```
ai-c4y/
└── csharp-docs/
    ├── raw/          ← Phase 2 output: per-file .md docs
    ├── enriched/     ← Phase 3 output: cross-reference enriched docs
    ├── workflows/    ← Phase 4 output: synthesized business workflow docs
    └── done/         ← Phase 5 marker: tracks successfully inserted docs
```

```bash
mkdir -p ai-c4y/csharp-docs/raw
mkdir -p ai-c4y/csharp-docs/enriched
mkdir -p ai-c4y/csharp-docs/workflows
mkdir -p ai-c4y/csharp-docs/done
```

---

### 0.4 — Manifest File Schema

The file `ai-c4y/csharp-manifest.json` is created automatically by Phase 1. Its schema is:

```json
{
  "C:\\Gitlab\\...\\VoyageManagement\\Voyage\\GetVoyageById.cs": {
    "hash": "sha256-of-file-content",
    "processed_at": "2026-05-14T10:00:00Z",
    "doc_path": "csharp-docs/raw/VoyageManagement/Voyage/GetVoyageById.md",
    "phase": "inserted",
    "file_type": "Handler",
    "lines": 45
  }
}
```

Valid phase values in order of progression:
`unprocessed` → `indexed` → `documented` → `enriched` → `synthesized` → `inserted`

---

## Done Checklist

- [ ] `.env` vars added
- [ ] Supabase table `n8n_documents_bvms_code` created
- [ ] Supabase RPC `match_n8n_documents_bvms_code` created
- [ ] Output folders created under `ai-c4y/csharp-docs/`
- [ ] `CSHARP_CODEBASE_PATH` verified to point at the correct repo root

---

## What Was Done

_(Fill in after completion)_
