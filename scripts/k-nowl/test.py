from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import pandas as pd
import os

from DataPreProcessing import DataPreProcessing
from Helpers import MarkdownHeaderMarker

paragraph_splitter = RecursiveCharacterTextSplitter(chunk_size=1250, chunk_overlap=0)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)

document_path = './BVMS-1.md'
document_path = './Sedna.md'

marker_char = 'VNLPAGL\n'

formatted_chunks = []

# Load the document using open
with open(document_path, 'r') as f:
    document = f.read()
    document = MarkdownHeaderMarker(document, marker_char)

    sections = document.split(marker_char)
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
    f.write('----------\n'.join(formatted_chunks))