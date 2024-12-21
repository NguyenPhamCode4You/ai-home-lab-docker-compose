src_folder_path = ""
target_folder_path = ""

import os
from FileHanlder import for_each_file_in_folder, remove_excessive_spacing, split_markdown_header_and_content, recursive_split_chunks
from agents.tools.SupabaseVectorStore import SupabaseVectorStore
from agents.tools.Embedding import Embedding
from agents.MarkdownContextCleaner import MarkdownContextCleaner

vector_store = SupabaseVectorStore(
    embedding=Embedding()
)

context_cleaner = MarkdownContextCleaner()

async def handle_clean_file(file_content: str, file_path: str, file_name: str) -> None:
    print(f"Cleaning file {file_name} at {file_path}...")
    target_file_name = file_name.split(".")[0] + ".md"
    target_file_folder_path = os.path.join(target_folder_path, file_path)
    os.makedirs(target_file_folder_path, exist_ok=True)
    target_file_path = os.path.join(target_file_folder_path, target_file_name)
    with open(target_file_path, "w", encoding="utf-8") as file:
        
        sections = split_markdown_header_and_content(file_content)
        chunk_size = 600

        for header, content in sections:
            content = remove_excessive_spacing(content)
            chunks = recursive_split_chunks(document=content, char=".", limit=chunk_size)

            for chunk in chunks:
                markdown = f"## {header}\n{chunk}"
                async for response_chunk in context_cleaner.stream(context=markdown):
                    file.write(response_chunk)
                    file.flush()

        print(f"File {file_name} cleaned and saved to {target_file_path}")

async def clean():
    for_each_file_in_folder(src_folder_path, handle_clean_file)

if __name__ == "__main__":
    import asyncio
    asyncio.run(clean())
