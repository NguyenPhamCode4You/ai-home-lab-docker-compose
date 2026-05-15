"""
cia_phase5_chunk.py

Phase 5 — RAG Chunking (no LLM)

Converts enriched per-file docs and workflow synthesis docs into RAG-ready
chunk files. Output format is identical to clean_src_folder output so that
insert_sentences (Phase 6) can process them directly.

Each output chunk line:
    # filename.md - SectionHeader
    chunk content (≤ chunk_size chars)

No LLM is called — this is pure deterministic text splitting.
LLM-generated docs are already clean; remove_excessive_spacing is intentionally
skipped to preserve code block formatting and paragraph structure.
"""

import os

from .cia_config import (
    DEFAULT_ENRICHED_FOLDER,
    DEFAULT_WORKFLOWS_FOLDER,
    DEFAULT_RAG_CHUNKS_FOLDER,
)
from .FileHanlder import split_markdown_header_and_content, recursive_split_chunks


def _chunk_file(file_name: str, content: str, out_path: str, chunk_size: int) -> int:
    """
    Split one markdown file into RAG-sized chunks and write to out_path.

    Returns the number of chunks written (0 = file was skipped / empty).
    """
    sections = split_markdown_header_and_content(content)
    output_parts = []

    for header, section_content in sections:
        header = header.strip()
        if not header:
            continue

        # Keep code block structure by NOT collapsing \n\n — just strip edges
        section_content = section_content.strip()
        if len(section_content) < 10:
            continue

        # Prefer paragraph breaks (\n\n) as primary split so code fences stay intact
        chunks = recursive_split_chunks(section_content, char="\n\n", limit=chunk_size)

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            output_parts.append(f"# {file_name} - {header}\n{chunk}\n\n")

    if not output_parts:
        return 0

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(output_parts)

    return len(output_parts)


async def chunk_for_rag(
    enriched_folder: str = DEFAULT_ENRICHED_FOLDER,
    workflows_folder: str = DEFAULT_WORKFLOWS_FOLDER,
    rag_chunks_folder: str = DEFAULT_RAG_CHUNKS_FOLDER,
    chunk_size: int = 800,
):
    """
    Phase 5: Chunk enriched per-file docs and workflow synthesis docs for RAG insertion.

    Processes two source folders:
      - enriched_folder  (Phase 3 output — per-file docs with Impact Scope + Used By)
      - workflows_folder (Phase 4 output — workflow synthesis + critical deep-dives)

    Output: rag_chunks_folder, preserving sub-folder hierarchy from each source.
    Existing chunk files are skipped (resumable).
    """
    total_chunked = 0
    total_skipped = 0
    total_empty = 0

    for src_folder in [enriched_folder, workflows_folder]:
        if not os.path.exists(src_folder):
            print(f"[Phase 5] Folder not found, skipping: {src_folder}")
            continue

        for root, _, files in os.walk(src_folder):
            for file in sorted(files):
                if not file.endswith(".md"):
                    continue

                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_folder)
                out_path = os.path.join(rag_chunks_folder, rel_path)

                if os.path.exists(out_path):
                    total_skipped += 1
                    continue

                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()

                chunks_written = _chunk_file(file, content, out_path, chunk_size)

                if chunks_written > 0:
                    total_chunked += 1
                    print(f"[Phase 5] Chunked ({chunks_written} chunks): {rel_path}")
                else:
                    total_empty += 1
                    print(f"[Phase 5] SKIP (no content): {rel_path}")

    print(
        f"[Phase 5] Complete. "
        f"{total_chunked} files chunked, "
        f"{total_skipped} already done, "
        f"{total_empty} empty/skipped."
    )
