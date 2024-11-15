import os

from DataPreProcessing import DataPreProcessing
from Helper import SplitByMarkdownHeader, RecursiveSplitSentences

document_path = 'documents'
processed_prefix = 'processed'

section_max_length = 1400

for root, _, files in os.walk(f"./{document_path}"):
    for file in files:
        file_path = os.path.join(root, file)
        filename = os.path.splitext(file)[0]

        processed_root = os.path.join(root, processed_prefix)
        if not os.path.exists(processed_root):
            os.makedirs(processed_root)
        
        processed_file_path = os.path.join(processed_root, f"{filename}.{processed_prefix}.md")
        if os.path.exists(processed_file_path):
            continue

        formatted_chunks = []

        with open(file_path, 'r') as file:
            document = file.read()
            sections = SplitByMarkdownHeader(document)
            for section in sections:
                section_parts = RecursiveSplitSentences(section, section_max_length)
                for section in section_parts:
                    section = DataPreProcessing(section).run()
                    print(section)
                    formatted_chunks.append(section)

        with open(processed_file_path, 'w') as f:
            f.write('\n----------\n'.join(formatted_chunks))