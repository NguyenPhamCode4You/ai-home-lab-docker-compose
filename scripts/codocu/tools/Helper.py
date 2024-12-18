import re

# Define the regex pattern to identify Markdown headers
markdown_header_pattern = r"^(#+[ ]*.+)$"

def SplitByMarkdownHeader(message: str):
    """
    Splits a Markdown message into chunks by headers and their associated content.

    Args:
        message (str): The Markdown message.

    Returns:
        list: List of chunks, where each chunk contains a header and its content.
    """
    parts = re.split(markdown_header_pattern, message, flags=re.MULTILINE)
    
    # Reconstruct chunks with headers and associated content
    chunks = []
    for i in range(1, len(parts), 2):  # Headers are in odd indices
        header = parts[i].strip()  # Strip unnecessary whitespace
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        chunks.append(f"{header}\n{content}")
    return chunks

def ExtractMarkdownHeadersAndContent(text):
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

def RemoveExcessiveSpacing(text):
    while "  " in text:
        text = text.replace("  ", " ")
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    while "...." in text:
        text = text.replace("....", "")
    while "----" in text:
        text = text.replace("----", "")
    return text

def HardSplitSentences(document: str, limit: int = 1000):
    # Hard split mode: enforce character limit strictly
    paragraphs = []
    while len(document) > limit:
        # Find the last possible split point within the limit
        split_index = document[:limit].rfind(" ")
        if split_index == -1:
            # No spaces found; force a hard split at the limit
            split_index = limit
        paragraphs.append(document[:split_index].strip())
        document = document[split_index:].strip()

    # Add the remaining text
    if document:
        paragraphs.append(document)

    return paragraphs

def RecursiveSplitSentences(document: str, limit: int = 1000):
    # Split the document into sentences
    sentences = document.split(".")
    
    # Recursively split long sentences
    paragraphs = []
    paragraph = ""
    while len(sentences) > 0:
        sentence = sentences.pop(0)
        if len(paragraph) + len(sentence) < limit:
            paragraph += f"{sentence}. "
        else:
            paragraphs.append(paragraph)
            paragraph = f"{sentence}. "

    # Add the last paragraph
    if len(paragraph) > 0:
        paragraphs.append(paragraph)

    return paragraphs

def RecursiveSplitLines(document: str, limit: int = 1000):
    lines = document.split("\n")
    paragraphs = []
    paragraph = ""
    for line in lines:
        if len(paragraph) + len(line) < limit:
            paragraph += f"{line}\n"
        else:
            paragraphs.append(paragraph)
            paragraph = f"{line}\n"

    if len(paragraph) > 0:
        paragraphs.append(paragraph)

    return paragraphs

    