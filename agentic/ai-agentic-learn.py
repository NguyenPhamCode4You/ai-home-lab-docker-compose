import os
src_folder_path = os.path.join("src")
cleaned_folder_path = os.path.join("docs", "agentic-cleaned")

from src.CodeDocumentWorkflow import write_code_document
from src.agents.CodeDocumentWriter import CodeDocumentWriter

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
    asyncio.run(clean())