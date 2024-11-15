from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import pandas as pd
import os

from DataPreProcessing import DataPreProcessing

paragraph_splitter = RecursiveCharacterTextSplitter(chunk_size=1400, chunk_overlap=50)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)

document_path = './BVMS-1.md'
document_path = './Sedna.md'

loader = TextLoader(document_path)
document = loader.load()

paragraphs = paragraph_splitter.split_documents(document)

formatted_chunks = []

for paragraph in paragraphs:
    if isinstance(paragraph, str):
        paragraph = paragraph
    else:
        paragraph = paragraph.page_content

    paragraph = DataPreProcessing(paragraph).run()
    print(paragraph)
    formatted_chunks.append(paragraph)


formated_prefix = 'processed'
root, file = os.path.split(document_path)

file_path = os.path.join(root, file)
filename = os.path.splitext(file)[0]
processd_file_path = os.path.join(root, f"{filename}.{formated_prefix}.md")

with open(processd_file_path, 'w') as f:
    f.write('----------\n'.join(formatted_chunks))