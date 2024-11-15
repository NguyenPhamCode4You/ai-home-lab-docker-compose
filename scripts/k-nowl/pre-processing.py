import os

from DataPreProcessing import DataPreProcessing
from Helper import SplitByMarkdownHeader

document_path = './documents'
processed_prefix = 'processed'

for root, _, files in os.walk(document_path):
    for file in files:
        file_path = os.path.join(root, file)
        filename = os.path.splitext(file)[0]
        
        processed_file_path = os.path.join(root, f"{filename}.{processed_prefix}.md")
        formatted_chunks = []

        with open(file_path, 'r') as file:
            document = file.read()
            sections = SplitByMarkdownHeader(document)
            for section in sections:
                section = DataPreProcessing(section).run()
                print(section)
                formatted_chunks.append(section)

        with open(processed_file_path, 'w') as f:
            f.write('\n----------\n'.join(formatted_chunks))