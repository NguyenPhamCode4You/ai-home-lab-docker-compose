import os

from DataPreProcessing import DataPreProcessing
from Helper import SplitByMarkdownHeader

document_path = './BVMS-1.md'
document_path = './Sedna.md'

formatted_chunks = []

with open(document_path, 'r') as file:
    document = file.read()
    sections = SplitByMarkdownHeader(document)
    for section in sections:
        section = DataPreProcessing(section).run()
        print(section)
        formatted_chunks.append(section)

formated_prefix = 'processed'
root, file = os.path.split(document_path)

file_path = os.path.join(root, file)
filename = os.path.splitext(file)[0]
processd_file_path = os.path.join(root, f"{filename}.{formated_prefix}.md")

with open(processd_file_path, 'w') as f:
    f.write('\n----------\n'.join(formatted_chunks))