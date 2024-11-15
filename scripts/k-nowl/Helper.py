import re

# Define the regex pattern to identify Markdown headers
markdown_header_pattern = r"^(#+[ ]*.+)$"

def SplitByMarkdownHeader(message: str):
    # Split the message by headers, capturing the headers
    parts = re.split(markdown_header_pattern, message, flags=re.MULTILINE)
    
    # Reconstruct chunks with headers and associated content
    chunks = []
    for i in range(1, len(parts), 2):  # Headers are in odd indices
        header = parts[i].strip()  # Strip unnecessary whitespace
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        chunks.append(f"{header}\n{content}")
    return chunks