"""
CSharpCodebaseWorkflow.py — Backward-compatibility shim.

The implementation has been split into focused phase files:
  src/cia_config.py            — shared config, constants, _load_index/_save_index
  src/cia_phase1_index.py      — Phase 1: build_codebase_index
  src/cia_phase2_document.py   — Phase 2: write_csharp_documents
  src/cia_phase3_enrich.py     — Phase 3: enrich_with_cross_references
  src/cia_phase4_synthesize.py — Phase 4: synthesize_workflow_documents
  src/cia_phase5_chunk.py      — Phase 5: chunk_for_rag (no LLM)
  src/cia_phase6_insert.py     — Phase 6: insert_rag_chunks (vector store)

This file re-exports everything so existing code importing from
`src.CSharpCodebaseWorkflow` continues to work without changes.
"""

from .cia_config import (  # noqa: F401
    CSHARP_CODEBASE_PATH,
    CSHARP_FOCUS_ONLY_FILES,
    CSHARP_IGNORE_FILES,
    CSHARP_LARGE_FILE_LINE_THRESHOLD,
    OPENROUTER_SYNTHESIS_MODEL,
    OPENROUTER_CRITICAL_MODEL,
    CLOUD_BATCH_DELAY,
    BATCH_SIZE,
    DEFAULT_INDEX_PATH,
    DEFAULT_RAW_DOCS_FOLDER,
    DEFAULT_ENRICHED_FOLDER,
    DEFAULT_WORKFLOWS_FOLDER,
    DEFAULT_RAG_CHUNKS_FOLDER,
    DEFAULT_RAG_DONE_FOLDER,
    LAYER_PRIORITY,
    VERB_CLUSTERS,
    PRIORITY_CRITICAL_FLOWS,
    _load_index,
    _save_index,
)
from .cia_phase1_index import build_codebase_index  # noqa: F401
from .cia_phase2_document import write_csharp_documents  # noqa: F401
from .cia_phase3_enrich import enrich_with_cross_references  # noqa: F401
from .cia_phase4_synthesize import synthesize_workflow_documents  # noqa: F401
from .cia_phase5_chunk import chunk_for_rag  # noqa: F401
from .cia_phase6_insert import insert_rag_chunks  # noqa: F401
