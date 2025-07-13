import os
from typing import List
from .FileHanlder import for_each_file_in_folder, remove_excessive_spacing, split_markdown_header_and_content, recursive_split_chunks
from .agents.MarkdownContextCleaner import MarkdownContextCleaner
from .agents.KeywordExtractor import KeywordExtractor
from .agents.KnowledgeCompression import KnowledgeCompression
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding
from .agents.Task import Task

async def insert_sentences(
        src_folder_path: str,
        table_name: str,
        llm_vector_store: SupabaseVectorStore = None,
        llm_keyword_extractor: Task = None,
        llm_knowledge_compressor: Task = None,
        summary_max_char: int = 600,
        keyword_count: int = 10):
    async def handle_insert_file(file_content: str, folder_path: str, file_name: str) -> None:
        print(f"Inserting file {file_name} at {folder_path} ooooooooooooooooo")
        keyword_extractor = llm_keyword_extractor or KeywordExtractor(count=keyword_count)
        knowledge_compressor = llm_knowledge_compressor or KnowledgeCompression(max_char=summary_max_char)
        vector_store = llm_vector_store or SupabaseVectorStore(embedding=Embedding())
        sections = split_markdown_header_and_content(file_content)
        for header, content in sections:
            header = header.strip().replace(":","")
            sentence = remove_excessive_spacing(content)
            if not sentence or len(sentence) < 5:
                continue
            try:
                knowledge = f"# {header}: {sentence}"
                keywords = await keyword_extractor.run(context=knowledge)
                summarize = await knowledge_compressor.run(context=knowledge)
                metadata={"file_name": file_name, "section": header, "keywords": keywords}
                vector_store.insert(
                    table_name=table_name,
                    content=knowledge,
                    metadata=metadata,
                    summarize=summarize)
                print(f"ooooooooooooooooo Sentence inserted success ooooooooooooooooo")
            except Exception as e:
                print(f"Failed to insert sentence: {sentence}, error: {e}")
    await for_each_file_in_folder(src_folder_path, handle_insert_file)

async def clean_src_folder(
        src_folder_path: str, 
        target_folder_path: str = None,
        llm_context_cleaner: Task = None,
        allowed_file_extensions: List[str] = None, 
        ignored_file_pattern: List[str] = None,
        keep_folder_hierarchy: bool = False,
        context_chunk_size: int = 600):
    async def handle_clean_file(file_content: str, folder_path: str, file_name: str) -> None:
        print(f"Cleaning file {file_name} at {folder_path} ooooooooooooooooo ")
        cleaner = llm_context_cleaner or MarkdownContextCleaner()
        adjusted_folder_path = target_folder_path or src_folder_path + "_cleaned"
        if keep_folder_hierarchy:
            adjusted_folder_path = os.path.join(adjusted_folder_path, folder_path)
        os.makedirs(adjusted_folder_path, exist_ok=True)
        target_file_name = file_name.strip().split(".")[0] + ".md"
        target_file_path = os.path.join(adjusted_folder_path, target_file_name)
        with open(target_file_path, "w", encoding="utf-8") as file:
            sections = split_markdown_header_and_content(file_content)
            for header, content in sections:
                header = header.strip()
                content = remove_excessive_spacing(content)
                chunks = recursive_split_chunks(document=content, char=".", limit=context_chunk_size)
                for index, chunk in enumerate(chunks):
                    print(f"Processing chunk {index + 1}/{len(chunks)} with length {len(chunk)}")
                    response = ""
                    async for response_chunk in cleaner.stream(context=chunk):
                        print(response_chunk, end="", flush=True)
                        response += response_chunk
                    markdown = f"\n# {target_file_name} - {header}\n{response}"
                    file.write(markdown)
                    file.flush()
            print(f"File {file_name} cleaned and saved to {target_file_path} ooooooooooooooooo")
    await for_each_file_in_folder(src_folder_path, handle_clean_file, allowed_file_extensions, ignored_file_pattern)

if __name__ == "__main__":
    import asyncio
    async def clean():
        await clean_src_folder(
            src_folder_path="docs/bvms",
            context_chunk_size=1600,
        )
    async def insert():
        await insert_sentences(
            src_folder_path="docs/bvms_cleaned",
            table_name="n8n_documents_bvms_neo",
        )
    asyncio.run(clean())
