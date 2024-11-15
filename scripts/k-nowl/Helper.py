import re

# Define the regex pattern for Markdown headers
markdown_header_pattern = r"^#+[ ]*.+(\n|$)"

def SplitByMarkdownHeader(message: str):
    matches = re.findall(markdown_header_pattern, message, re.MULTILINE)
    return matches