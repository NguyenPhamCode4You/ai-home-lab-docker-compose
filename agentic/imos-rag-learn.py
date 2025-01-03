import os
src_folder_path = os.path.join("docs", "imos")
overwrite_folder_path = os.path.join("docs", "imos-overwrite")
cleaned_folder_path = os.path.join("docs", "imos-cleaned")

from src.RagWorkflow import clean_src_folder, insert_sentences
from src.agents.ContextOverwriter import ContextOverwriter
from src.agents.MarkdownContextCleaner import MarkdownContextCleaner

async def overwrite():
    await clean_src_folder(
        src_folder_path=src_folder_path, 
        target_folder_path=overwrite_folder_path, 
        llm_context_cleaner=ContextOverwriter(),
        context_chunk_size=1600)
    print("Overwrite done")

async def clean():
    await clean_src_folder(
        src_folder_path=overwrite_folder_path, 
        target_folder_path=cleaned_folder_path, 
        llm_context_cleaner=MarkdownContextCleaner(),
        context_chunk_size=1600)
    print("Clean done")

async def insert():
    await insert_sentences(
        src_folder_path=cleaned_folder_path,
        table_name="n8n_documents_ops")
    print("Insert done")

if __name__ == "__main__":
    import asyncio
    asyncio.run(insert())