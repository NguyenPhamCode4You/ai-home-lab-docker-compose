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

Supports --cloud N / --local N: routes KeywordExtractor and KnowledgeCompression
to OpenRouter / Ollama with bounded concurrency, matching the pattern of all other
pipeline phases.

Resumable: processed files are tracked via .done markers in rag_done_folder.
Table name is read from CIA_RAG_TABLE_NAME env var (default: n8n_documents_csharp).
"""

import asyncio
import os

from .cia_config import (
    DEFAULT_RAG_CHUNKS_FOLDER,
    DEFAULT_RAG_DONE_FOLDER,
)
from .RagWorkflow import insert_sentences
from .agents.KeywordExtractor import KeywordExtractor
from .agents.KnowledgeCompression import KnowledgeCompression
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_GENERAL_MODEL

OPENROUTER_PHASE6_MODEL = os.getenv("CIA_OPENROUTER_MODEL", "qwen/qwen3-32b")


def _make_agents(force_cloud: bool, force_local: bool, keyword_count: int, summary_max_char: int):
    """Return (keyword_extractor, knowledge_compressor) wired to the correct model."""
    if force_cloud:
        model = OpenRouter(model=OPENROUTER_PHASE6_MODEL)
    elif force_local:
        model = Ollama(model=OLLAMA_GENERAL_MODEL)
    else:
        model = Ollama(model=OLLAMA_GENERAL_MODEL)

    return (
        KeywordExtractor(count=keyword_count, llm_model=model),
        KnowledgeCompression(max_char=summary_max_char, llm_model=model),
    )


async def insert_rag_chunks(
    rag_chunks_folder: str = DEFAULT_RAG_CHUNKS_FOLDER,
    rag_done_folder: str = DEFAULT_RAG_DONE_FOLDER,
    table_name: str = None,
    summary_max_char: int = 600,
    keyword_count: int = 20,
    force_cloud: bool = False,
    force_local: bool = False,
    concurrency: int = 1,
):
    """
    Phase 6: Insert RAG chunks from Phase 5 into the Supabase vector store.

    Supports --cloud N / --local N for routing keyword extraction and summarization
    to OpenRouter or Ollama with N concurrent workers (matches other phase behaviour).

    Each chunk file is processed by insert_sentences which:
      - Splits the file on markdown headers (each header = one chunk block)
      - Calls KeywordExtractor and KnowledgeCompression per chunk
      - Inserts into the specified Supabase table

    Resumable: already-inserted files have a .done marker in rag_done_folder.
    """
    if not table_name:
        table_name = os.getenv("CIA_RAG_TABLE_NAME", "n8n_documents_csharp")

    if not os.path.exists(rag_chunks_folder):
        print(f"[Phase 6] Chunks folder not found: {rag_chunks_folder}")
        print("[Phase 6] Run --phase chunk first to generate RAG chunks.")
        return

    # Collect all pending chunk files
    all_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(rag_chunks_folder)
        for f in sorted(files)
        if f.endswith(".md")
    ]

    if force_cloud:
        OpenRouter.set_concurrency(concurrency)
        print(f"[Phase 6] Cloud mode (OpenRouter, concurrency={concurrency}), table='{table_name}'")
    elif force_local:
        print(f"[Phase 6] Local mode (Ollama, concurrency={concurrency}), table='{table_name}'")
    else:
        print(f"[Phase 6] Local mode (Ollama, concurrency=1), table='{table_name}'")

    print(f"[Phase 6] {len(all_files)} chunk file(s) to process.")

    sem = asyncio.Semaphore(max(1, concurrency))
    total_done = 0
    total_skip = 0

    async def _process_file(file_path: str, idx: int):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        done_marker = os.path.join(rag_done_folder, file_name + ".done")
        if os.path.exists(done_marker):
            return "skip"

        keyword_extractor, knowledge_compressor = _make_agents(
            force_cloud, force_local, keyword_count, summary_max_char
        )
        async with sem:
            print(f"[Phase 6] [{idx}/{len(all_files)}] Inserting: {os.path.basename(file_path)}")
            with open(file_path, "r", encoding="utf-8") as fh:
                content = fh.read()

            # Re-use insert_sentences for a single file by writing a temp-like call
            # Pass the agents explicitly so model routing is respected
            from .FileHanlder import split_markdown_header_and_content, remove_excessive_spacing
            from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
            from .agents.tools.Embedding import Embedding

            vector_store = SupabaseVectorStore(embedding=Embedding())
            sections = split_markdown_header_and_content(content)
            for header, section_content in sections:
                header = header.strip().replace(":", "")
                sentence = remove_excessive_spacing(section_content)
                if not sentence or len(sentence) < 5:
                    continue
                try:
                    knowledge = f"# {header}: {sentence}"
                    keywords = await keyword_extractor.run(context=knowledge)
                    summarize = await knowledge_compressor.run(context=knowledge)
                    metadata = {"file_name": file_name, "section": header, "keywords": keywords}
                    vector_store.insert(
                        table_name=table_name,
                        content=knowledge,
                        metadata=metadata,
                        summarize=summarize,
                    )
                except Exception as e:
                    print(f"[Phase 6] ERROR in {file_name} / {header}: {e}")

            os.makedirs(rag_done_folder, exist_ok=True)
            open(done_marker, "w").close()
            return "done"

    results = await asyncio.gather(
        *[_process_file(fp, i + 1) for i, fp in enumerate(all_files)]
    )
    total_done = results.count("done")
    total_skip = results.count("skip")

    print(
        f"[Phase 6] Complete. "
        f"{total_done} files inserted, "
        f"{total_skip} already done."
    )
