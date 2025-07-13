import os
import re
from typing import Callable, List

async def for_each_file_in_folder(folder_path: str, executor: Callable[[str, str, str], None], allowed_file_extensions: List[str] = None, ignored_file_pattern: List[str] = None):
    for root, _, files in os.walk(folder_path):
        for index, file in enumerate(files):
            print(f"Processing file {index + 1}/{len(files)}: {file} in {root} ooooooooooooooooo")
            file_path = os.path.join(root, file)
            file_name = os.path.splitext(file)[0]
            if allowed_file_extensions is not None and ignored_file_pattern is not None and not is_allowed_file(file_path, allowed_file_extensions, ignored_file_pattern):
                continue
            try:
                file_content = _read_file(file_path)
            except Exception as e:
                print(f"Failed to read file '{file_path}': {e}")
                continue
            try:
                await executor(file_content, root, file_name)
            except Exception as e:
                print(f"Failed to execute handler for file '{file_path}': {e}")

def _read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()
    
markdown_header_pattern = r"^(#+[ ]*.+)$"

def remove_excessive_spacing(text: str) -> str:
    while "  " in text:
        text = text.replace("  ", " ")
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    while "...." in text:
        text = text.replace("....", "")
    while "----" in text:
        text = text.replace("----", "")
    return text

def split_markdown_header_and_content(text):
    """
    Extracts Markdown headers and their associated content from a given text.

    Args:
        text (str): The input text containing Markdown.

    Returns:
        list of tuples: A list where each tuple contains a header and its associated content.
    """
    # Split the text into parts based on headers
    parts = re.split(markdown_header_pattern, text, flags=re.MULTILINE)
    
    # Group headers with their associated content
    header_content_pairs = []
    for i in range(1, len(parts), 2):  # Headers are in odd indices
        header = parts[i].strip()  # Strip whitespace from the header
        header = header.replace("#", " ")  # Replace newline characters with spaces
        header = header.replace("  ", "")  # Replace newline characters with spaces
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""  # Get content after the header
        header_content_pairs.append((header, content))
    
    return header_content_pairs

def recursive_split_chunks(document: str, char: str = ".", limit: int = 600):
    """
    Recursively split document into chunks under the specified limit.
    Uses multiple splitting strategies with fallback options.
    """
    if not document or len(document.strip()) == 0:
        return []
    
    # If document is already under limit, return as-is
    if len(document) <= limit:
        return [document.strip()]
    
    # Define splitting delimiters in order of preference
    delimiters = [
        "\n\n",    # Paragraph breaks
        ". ",      # Sentence endings
        "! ",      # Exclamation sentences
        "? ",      # Question sentences
        "; ",      # Semicolon breaks
        ", ",      # Comma breaks
        " ",       # Word breaks
        ""         # Character-by-character (last resort)
    ]
    
    def split_by_delimiter(text: str, delimiter: str, limit: int):
        """Split text by delimiter and combine into chunks under limit"""
        if not delimiter:  # Character-by-character splitting
            chunks = []
            current_chunk = ""
            for char in text:
                if len(current_chunk + char) <= limit:
                    current_chunk += char
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = char
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            return [chunk for chunk in chunks if chunk.strip()]
        
        # Split by delimiter
        parts = text.split(delimiter)
        chunks = []
        current_chunk = ""
        
        for i, part in enumerate(parts):
            # Reconstruct delimiter except for last part
            part_with_delimiter = part + (delimiter if i < len(parts) - 1 else "")
            
            # Check if current part alone exceeds limit
            if len(part_with_delimiter) > limit:
                # Save current chunk if not empty
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # Recursively split the oversized part with next delimiter
                next_delimiter_index = delimiters.index(delimiter) + 1
                if next_delimiter_index < len(delimiters):
                    sub_chunks = split_by_delimiter(part_with_delimiter, delimiters[next_delimiter_index], limit)
                    chunks.extend(sub_chunks)
                else:
                    # Last resort: just add it (shouldn't happen with character splitting)
                    chunks.append(part_with_delimiter.strip())
            else:
                # Check if adding this part would exceed limit
                if len(current_chunk + part_with_delimiter) > limit:
                    # Save current chunk and start new one
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = part_with_delimiter
                else:
                    # Add to current chunk
                    current_chunk += part_with_delimiter
        
        # Add remaining chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if chunk.strip()]
    
    # Start with the specified delimiter or first one if not provided
    start_delimiter = char if char in delimiters else delimiters[0]
    start_index = delimiters.index(start_delimiter) if start_delimiter in delimiters else 0
    
    # Try splitting with each delimiter starting from the specified one
    for delimiter in delimiters[start_index:]:
        chunks = split_by_delimiter(document, delimiter, limit)
        
        # Check if all chunks are under limit
        if all(len(chunk) <= limit for chunk in chunks):
            return chunks
    
    # Fallback: return original document if all strategies fail (shouldn't happen)
    return [document.strip()]

def extract_rag_sentences(text: str, min_chars = 100):
    extracted_sentences = []
    sentences = text.split(". ")
    for sentence in sentences:
        if "```" in sentence or "===" in sentence or "'''" in sentence:
            extracted_sentences.append(sentence)
            continue
        if "{" in sentence and "}" in sentence and '"' in sentence and ":" in sentence:
            extracted_sentences.append(sentence)
            continue
        sub_sentences = sentence.split("\n")
        current_sentence = ""
        for sub_sentence in sub_sentences:
            if len(current_sentence) + len(sub_sentence) < min_chars:
                current_sentence += f"{sub_sentence}. "
                continue
            extracted_sentences.append(current_sentence)
            current_sentence = f"{sub_sentence}. "
        if len(current_sentence) > 0:
            extracted_sentences.append(current_sentence)
    return extracted_sentences

def is_allowed_file(file_path, allowed_file_extensions: List[str], ignored_file_pattern: List[str]):
    if not any(file_path.endswith(ext) for ext in allowed_file_extensions):
        return False
    
    if not is_allowed_path(file_path, ignored_file_pattern):
        return False
    
    return True

def is_allowed_path(file_path, ignored_file_pattern: List[str]):
    if any(pattern.lower() in file_path.lower() for pattern in ignored_file_pattern):
        return False
    
    return True