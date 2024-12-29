import os
src_folder_path = os.path.join("src")
cleaned_folder_path = os.path.join("docs", "agentic-cleaned")

from src.CodeDocumentWorkflow import write_code_document, insert_code_documents
from src.agents.CodeDocumentWriter import CodeDocumentWriter

async def insert():
    await insert_code_documents(
        src_folder_path=cleaned_folder_path,
        table_name="n8n_documents_agentic_neo",
        keyword_count=25,
    )
    print("Insert done")

async def clean():
    await write_code_document(
        src_folder_path=src_folder_path,
        target_folder_path=cleaned_folder_path, 
        allowed_file_extensions=[".py"],
        ignored_file_pattern=["__pycache__"],
        llm_code_document_writer=CodeDocumentWriter(
            max_context_tokens=10000,
        ))
    print("Clean done")

if __name__ == "__main__":
    import asyncio
    asyncio.run(insert())