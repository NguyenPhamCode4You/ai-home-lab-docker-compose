from docling.document_converter import DocumentConverter

filename = "Sedna.pdf"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(filename)
print(result.document.export_to_markdown())  # output: "## Docling Technical Report[...]"

# Save the result to a file filename.md
with open(f"{filename}.md", "w") as file:  # use f-string for proper variable formatting
    file.write(result.document.export_to_markdown())
