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

def RecursiveSplitSentences(document: str, limit: int = 1000):
    # Split the document into sentences
    sentences = document.split(".")
    
    # Recursively split long sentences
    paragraphs = []
    paragraph = ""
    while len(sentences) > 0:
        sentence = sentences.pop(0)
        if len(paragraph) + len(sentence) < limit:
            paragraph += f"{sentence.strip()}. "
        else:
            paragraphs.append(paragraph.strip())
            paragraph = f"{sentence.strip()}. "

    # Add the last paragraph
    if len(paragraph) > 0:
        paragraphs.append(paragraph.strip())

    return paragraphs

    