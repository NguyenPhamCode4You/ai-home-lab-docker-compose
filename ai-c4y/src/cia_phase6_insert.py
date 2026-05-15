"""
cia_phase6_insert.py

Phase 6 — RAG Vector Store Insertion

Inserts RAG-ready chunk files (produced by Phase 5) into the Supabase
vector store using the existing insert_sentences workflow.

For each chunk, insert_sentences:
  1. Splits the file by markdown header → one (header, content) pair per chunk
  2. Extracts keywords via KeywordExtractor
  3. Compresses/summarizes via KnowledgeCompression
  4. Inserts (content, embedding, metadata) into Supabase

Resumable: processed files are tracked via .done markers in rag_done_folder.
Table name is read from CIA_RAG_TABLE_NAME env var (default: n8n_documents_csharp).
"""

import os

from .cia_config import (
    DEFAULT_RAG_CHUNKS_FOLDER,
    DEFAULT_RAG_DONE_FOLDER,
)
from .RagWorkflow import insert_sentences


async def insert_rag_chunks(
    rag_chunks_folder: str = DEFAULT_RAG_CHUNKS_FOLDER,
    rag_done_folder: str = DEFAULT_RAG_DONE_FOLDER,
    table_name: str = None,
    summary_max_char: int = 600,
    keyword_count: int = 20,
):
    """
    Phase 6: Insert RAG chunks from Phase 5 into the Supabase vector store.

    Each chunk file is processed by insert_sentences which:
      - Splits the file on markdown headers (each header = one chunk block)
      - Calls KeywordExtractor and KnowledgeCompression per chunk
      - Inserts into the specified Supabase table

    Resumable: already-inserted files have a .done marker in rag_done_folder.
    Set CIA_RAG_TABLE_NAME in your .env to control the destination table.
    """
    if not table_name:
        table_name = os.getenv("CIA_RAG_TABLE_NAME", "n8n_documents_csharp")

    if not os.path.exists(rag_chunks_folder):
        print(f"[Phase 6] Chunks folder not found: {rag_chunks_folder}")
        print("[Phase 6] Run --phase chunk first to generate RAG chunks.")
        return

    chunk_files = sum(
        1
        for root, _, files in os.walk(rag_chunks_folder)
        for f in files
        if f.endswith(".md")
    )
    print(f"[Phase 6] Inserting {chunk_files} chunk file(s) into table '{table_name}'")

    await insert_sentences(
        src_folder_path=rag_chunks_folder,
        done_folder_path=rag_done_folder,
        table_name=table_name,
        summary_max_char=summary_max_char,
        keyword_count=keyword_count,
    )

    print(f"[Phase 6] Complete. Done markers stored in: {rag_done_folder}")
