"""
cia_phase6_insert.py

Phase 6 — RAG Vector Store Insertion

Inserts RAG-ready chunk files (produced by Phase 5) into the Supabase
vector store.

Concurrency model: chunks from ALL files are flattened into one work queue.
N concurrent workers (--cloud N / --local N) each pull one chunk at a time.
This avoids the problem where one large file blocks a worker slot while
many small files finish instantly.

Resume model: each chunk gets its own .done marker named:
  {rag_done_folder}/{file_name}_c{chunk_idx}.done
If a run fails mid-file, only the failed/remaining chunks are retried next run.
No duplicate DB inserts.

Backward-compat: if a legacy per-file .done marker exists ({file_name}.done),
all chunks of that file are treated as already done.

Table name is read from CIA_RAG_TABLE_NAME env var (default: n8n_documents_csharp).
"""

import asyncio
import os

from tqdm import tqdm

from .cia_config import (
    DEFAULT_RAG_CHUNKS_FOLDER,
    DEFAULT_RAG_DONE_FOLDER,
)
from .FileHanlder import split_markdown_header_and_content, remove_excessive_spacing
from .agents.KeywordExtractor import KeywordExtractor
from .agents.KnowledgeCompression import KnowledgeCompression
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding
from .agents.models.Ollama import Ollama
from .agents.models.OpenRouter import OpenRouter
from .agents.constants import OLLAMA_CODE_MODEL

OPENROUTER_PHASE6_MODEL = os.getenv("CIA_OPENROUTER_MODEL", "qwen/qwen3-32b")


def _make_agents(force_cloud: bool, force_local: bool, keyword_count: int, summary_max_char: int):
    """Return (keyword_extractor, knowledge_compressor) wired to the correct model."""
    if force_cloud:
        model = OpenRouter(model=OPENROUTER_PHASE6_MODEL)
    else:
        model = Ollama(model=OLLAMA_CODE_MODEL)

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

    Concurrency is per-chunk (not per-file): all chunks across all files are
    processed by N concurrent workers. Each worker does:
      keyword extract → compress → embed → DB insert → write .done marker

    Resume: per-chunk .done markers mean only failed/skipped chunks are retried.
    """
    if not table_name:
        table_name = os.getenv("CIA_RAG_TABLE_NAME", "n8n_documents_csharp")

    if not os.path.exists(rag_chunks_folder):
        print(f"[Phase 6] Chunks folder not found: {rag_chunks_folder}")
        print("[Phase 6] Run --phase chunk first to generate RAG chunks.")
        return

    os.makedirs(rag_done_folder, exist_ok=True)

    # ── Step 1: collect all chunk files ──────────────────────────────────────
    all_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(rag_chunks_folder)
        for f in sorted(files)
        if f.endswith(".md")
    ]

    # ── Step 2: flatten files → individual (file_name, chunk_idx, header, text) ──
    all_chunks = []
    for file_path in all_files:
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Backward-compat: legacy per-file .done means all its chunks are done
        legacy_done = os.path.join(rag_done_folder, file_name + ".done")
        if os.path.exists(legacy_done):
            continue

        with open(file_path, "r", encoding="utf-8") as fh:
            content = fh.read()

        sections = split_markdown_header_and_content(content)
        for chunk_idx, (header, section_content) in enumerate(sections):
            header = header.strip().replace(":", "")
            sentence = remove_excessive_spacing(section_content)
            if not sentence or len(sentence) < 5:
                continue

            chunk_key = f"{file_name}_c{chunk_idx}"
            done_marker = os.path.join(rag_done_folder, chunk_key + ".done")
            if os.path.exists(done_marker):
                continue  # already inserted in a previous run

            all_chunks.append((file_name, chunk_idx, header, sentence, done_marker))

    total_chunks = len(all_chunks)

    if force_cloud:
        # Set OpenRouter concurrency to match worker count so each worker gets
        # its own request slot (no cross-worker throttling).
        OpenRouter.set_concurrency(concurrency)
        print(f"[Phase 6] Cloud mode (OpenRouter), {concurrency} parallel workers, table='{table_name}'")
    elif force_local:
        print(f"[Phase 6] Local mode (Ollama), concurrency={concurrency} chunks, table='{table_name}'")
    else:
        print(f"[Phase 6] Local mode (Ollama), concurrency=1 chunk, table='{table_name}'")

    print(f"[Phase 6] {total_chunks} chunk(s) to insert (across {len(all_files)} file(s)).")

    if total_chunks == 0:
        print("[Phase 6] Nothing to do — all chunks already inserted.")
        return

    # ── Step 3: shared resources ──────────────────────────────────────────────
    vector_store = SupabaseVectorStore(embedding=Embedding())
    results = {"done": 0, "error": 0}

    progress = tqdm(
        total=total_chunks,
        desc="[Phase 6] Inserting",
        unit="chunk",
        dynamic_ncols=True,
        bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {bar}",
    )

    # ── Step 4: queue + N isolated workers (each has its own agent instances) ─
    # Each worker owns its agents — Task.state is mutable so sharing across
    # concurrent workers causes data corruption.

    queue: asyncio.Queue = asyncio.Queue()
    for chunk_data in all_chunks:
        queue.put_nowait(chunk_data)

    # Signals workers to stop picking up new chunks (set on Ctrl+C).
    # In-flight chunks are allowed to finish so their .done markers are written.
    shutdown_event = asyncio.Event()

    async def _worker(_worker_id: int):
        keyword_extractor, knowledge_compressor = _make_agents(
            force_cloud, force_local, keyword_count, summary_max_char
        )
        while not shutdown_event.is_set():
            try:
                file_name, chunk_idx, header, sentence, done_marker = queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            inserted = False
            try:
                knowledge = f"# {header}: {sentence}"
                keywords = await keyword_extractor.run(context=knowledge)
                summarize = await knowledge_compressor.run(context=knowledge)
                vector_store.insert(
                    table_name=table_name,
                    content=knowledge,
                    metadata={"file_name": file_name, "section": header, "keywords": keywords},
                    summarize=summarize,
                )
                inserted = True
                open(done_marker, "w").close()
                results["done"] += 1
            except asyncio.CancelledError:
                # If the DB insert already completed, write the marker so we
                # don't re-insert this chunk on the next run.
                if inserted:
                    try:
                        open(done_marker, "w").close()
                        results["done"] += 1
                    except Exception:
                        pass
                raise
            except Exception as e:
                results["error"] += 1
                tqdm.write(f"[Phase 6] ERROR in {file_name} / {header}: {e}")
            finally:
                progress.update(1)
                progress.set_postfix(ok=results["done"], err=results["error"], refresh=False)

    # ── Step 5: launch N workers and wait for all to drain the queue ──────────
    n_workers = max(1, concurrency)
    workers = [asyncio.create_task(_worker(i)) for i in range(n_workers)]
    try:
        await asyncio.gather(*workers)
    except (KeyboardInterrupt, asyncio.CancelledError):
        shutdown_event.set()
        tqdm.write("\n[Phase 6] Interrupt received — waiting for in-flight chunks to finish...")
        await asyncio.gather(*workers, return_exceptions=True)
        progress.close()
        remaining = queue.qsize()
        print(
            f"[Phase 6] Stopped safely. "
            f"{results['done']} inserted, {results['error']} errors, "
            f"{remaining} remaining. Re-run the same command to resume."
        )
        return

    progress.close()
    print(
        f"[Phase 6] Complete. "
        f"{results['done']} inserted, "
        f"{results['error']} failed (re-run to retry failed chunks)."
    )
