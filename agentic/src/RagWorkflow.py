import os
from FileHanlder import for_each_file_in_folder, remove_excessive_spacing, split_markdown_header_and_content, recursive_split_chunks
from agents.MarkdownContextCleaner import MarkdownContextCleaner

async def clean_src_folder(src_folder_path: str, target_folder_path: str = None, chunk_size: int = 600) -> None:
    async def handle_clean_file(file_content: str, folder_path: str, file_name: str) -> None:
        print(f"Cleaning file {file_name} at {folder_path}...")
        target_file_name = file_name.strip().split(".")[0] + ".md"
        os.makedirs(target_folder_path, exist_ok=True)
        target_file_path = os.path.join(target_folder_path, target_file_name)
        with open(target_file_path, "w", encoding="utf-8") as file:
            sections = split_markdown_header_and_content(file_content)
            for header, content in sections:
                header = header.strip()
                content = remove_excessive_spacing(content)
                chunks = recursive_split_chunks(document=content, char=".", limit=chunk_size)
                for chunk in chunks:
                    markdown = f"# {target_file_name} - {header}\n{chunk}"
                    async for response_chunk in context_cleaner.stream(context=markdown):
                        print(response_chunk, end="", flush=True)
                        file.write(response_chunk)
                        file.flush()
            print(f"File {file_name} cleaned and saved to {target_file_path}")

    context_cleaner = MarkdownContextCleaner()
    target_folder_path = target_folder_path or src_folder_path + "_cleaned"
    await for_each_file_in_folder(src_folder_path, handle_clean_file)

if __name__ == "__main__":
    import asyncio
    asyncio.run(clean_src_folder("docs/bvms"))
