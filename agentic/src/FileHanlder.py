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
    sentences = document.split(char)
    paragraphs = []
    paragraph = ""
    while len(sentences) > 0:
        sentence = sentences.pop(0)
        if len(paragraph) + len(sentence) < limit:
            paragraph += f"{sentence}. "
        else:
            paragraphs.append(paragraph)
            paragraph = f"{sentence}. "
    if len(paragraph) > 0:
        paragraphs.append(paragraph)
    return paragraphs

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