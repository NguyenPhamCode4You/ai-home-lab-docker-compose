import os
src_folder_path = os.path.join("docs", "output")
cleaned_folder_path = os.path.join("docs", "output-cleaned")

from src.RagWorkflow import clean_src_folder, insert_sentences
from src.agents.MarkdownContextCleaner import MarkdownContextCleaner

async def clean():
    await clean_src_folder(
        src_folder_path=src_folder_path,
        target_folder_path=cleaned_folder_path, 
        llm_context_cleaner=MarkdownContextCleaner(),
        context_chunk_size=600)
    print("Clean done")

async def insert():
    await insert_sentences(
        src_folder_path=cleaned_folder_path,
        table_name="n8n_documents_imos_neo",
        summary_max_char=600, keyword_count=20)
    print("Insert done")

if __name__ == "__main__":
    import asyncio
    asyncio.run(clean())