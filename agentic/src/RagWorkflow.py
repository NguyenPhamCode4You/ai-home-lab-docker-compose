import os
from .FileHanlder import for_each_file_in_folder, remove_excessive_spacing, split_markdown_header_and_content, recursive_split_chunks
from .agents.MarkdownContextCleaner import MarkdownContextCleaner
from .agents.DocumentLinesExtractor import DocumentLinesExtractor
from .agents.KeywordExtractor import KeywordExtractor
from .agents.ContextSummarizer import ContextSummarizer
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding
from .agents.Task import Task

async def insert_sentences(
        src_folder_path: str,
        table_name: str,
        llm_vector_store: SupabaseVectorStore = None,
        llm_sentence_extractor: Task = None,
        llm_keyword_extractor: Task = None,
        llm_context_summarizer: Task = None,
        sentence_delimeter: str = "VNAGL-NEWLINE",
        summary_max_char: int = 250,
        keyword_count: int = 10):
    async def handle_insert_file(file_content: str, folder_path: str, file_name: str) -> None:
        print(f"Inserting file {file_name} at {folder_path} ooooooooooooooooo")
        sentence_extractor = llm_sentence_extractor or DocumentLinesExtractor(line_delimiter=sentence_delimeter)
        keyword_extractor = llm_keyword_extractor or KeywordExtractor(count=keyword_count)
        context_summarizer = llm_context_summarizer or ContextSummarizer(max_char=summary_max_char)
        vector_store = llm_vector_store or SupabaseVectorStore(embedding=Embedding())
        sections = split_markdown_header_and_content(file_content)
        for header, content in sections:
            header = header.strip().replace(":","")
            content = remove_excessive_spacing(content)
            chunks_string = await sentence_extractor.run(context=content)
            sentences = chunks_string.split(sentence_delimeter) if chunks_string else []
            for sentence in sentences:
                if not sentence or len(sentence) < 5:
                    continue
                try:
                    content = f"# {header}: {sentence}"
                    keywords = await keyword_extractor.run(context=content)
                    summarize = await context_summarizer.run(context=content)
                    metadata={"file_name": file_name, "section": header, "keywords": keywords}
                    vector_store.insert(
                        table_name=table_name,
                        content=content,
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
                for chunk in chunks:
                    markdown = f"# {target_file_name} - {header}\n{chunk}"
                    async for response_chunk in cleaner.stream(context=markdown):
                        print(response_chunk, end="", flush=True)
                        file.write(response_chunk)
                        file.flush()
            print(f"File {file_name} cleaned and saved to {target_file_path} ooooooooooooooooo")
    await for_each_file_in_folder(src_folder_path, handle_clean_file)

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
