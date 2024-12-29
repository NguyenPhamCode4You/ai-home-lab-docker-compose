import os
from typing import List
from .FileHanlder import for_each_file_in_folder, split_markdown_header_and_content
from .agents.CodeDocumentWriter import CodeDocumentWriter
from .agents.Task import Task
from .agents.KeywordExtractor import KeywordExtractor
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding

async def insert_code_documents(
        src_folder_path: str,
        table_name: str,
        llm_vector_store: SupabaseVectorStore = None,
        llm_keyword_extractor: Task = None,
        keyword_count: int = 10):
    async def handle_insert_file(file_content: str, folder_path: str, file_name: str) -> None:
        print(f"Inserting file {file_name} at {folder_path} ooooooooooooooooo")
        keyword_extractor = llm_keyword_extractor or KeywordExtractor(count=keyword_count)
        vector_store = llm_vector_store or SupabaseVectorStore(embedding=Embedding())
        sections = split_markdown_header_and_content(file_content)
        for header, content in sections:
            header = header.strip().replace(":","")
            if "**Explanation**" not in content:
                continue
            code_block = content.split("**Explanation**")[0]
            explaination = content.split("**Explanation**")[1]
            try:
                knowledge = f"# {header}:\n\n {code_block}"
                keywords = await keyword_extractor.run(context=knowledge)
                metadata={"file_name": file_name, "section": header, "keywords": keywords}
                vector_store.insert(
                    table_name=table_name,
                    content=knowledge,
                    metadata=metadata,
                    summarize=explaination)
                print(f"ooooooooooooooooo Sentence inserted success ooooooooooooooooo")
            except Exception as e:
                print(f"Failed to insert: {header}, error: {e}")
    await for_each_file_in_folder(src_folder_path, handle_insert_file)

async def write_code_document(
        src_folder_path: str, 
        target_folder_path: str = None,
        llm_code_document_writer: Task = None,
        allowed_file_extensions: List[str] = None, 
        ignored_file_pattern: List[str] = None,
        keep_folder_hierarchy: bool = False):
    async def handle_clean_file(file_content: str, folder_path: str, file_name: str) -> None:
        print(f"Writeing document for file {file_name} at {folder_path} ooooooooooooooooo ")
        document_writer = llm_code_document_writer or CodeDocumentWriter()
        adjusted_folder_path = target_folder_path or src_folder_path + "_cleaned"
        if keep_folder_hierarchy:
            adjusted_folder_path = os.path.join(adjusted_folder_path, folder_path)
        os.makedirs(adjusted_folder_path, exist_ok=True)
        target_file_name = file_name.strip().split(".")[0] + ".md"
        target_file_path = os.path.join(adjusted_folder_path, target_file_name)
        with open(target_file_path, "w", encoding="utf-8") as file:
            async for response_chunk in document_writer.stream(context=file_content):
                print(response_chunk, end="", flush=True)
                file.write(response_chunk)
                file.flush()
            print(f"File {file_name} done and saved to {target_file_path} ooooooooooooooooo")
    await for_each_file_in_folder(src_folder_path, handle_clean_file, allowed_file_extensions, ignored_file_pattern)