from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import pandas as pd
import os

from DataPreProcessing import DataPreProcessing
from ProcessMarkdownHeader import ProcessMarkdownHeader

paragraph_splitter = RecursiveCharacterTextSplitter(chunk_size=1250, chunk_overlap=0)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)

document_path = './BVMS-1.md'
document_path = './Sedna.md'

formatted_chunks = []

loader = TextLoader(document_path)
documents = loader.load()
documents = paragraph_splitter.split_documents(documents)

for document in documents:
    if isinstance(document, str):
        document = document
    else:
        document = document.page_content

    document = ProcessMarkdownHeader(document)
    sections = [section for section in document.split("VNLPAGL") if len(section) > 5]

    for section in sections:
        # section = DataPreProcessing(section).run()
        print(section)
        formatted_chunks.append(section)

formated_prefix = 'processed'
root, file = os.path.split(document_path)

file_path = os.path.join(root, file)
filename = os.path.splitext(file)[0]
processd_file_path = os.path.join(root, f"{filename}.{formated_prefix}.md")

with open(processd_file_path, 'w') as f:
    f.write('----------\n'.join(formatted_chunks))