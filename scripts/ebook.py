from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import pandas as pd
import os
import subprocess

from ChunkValidator import ChunkValidator
from CreateEmbedding import CreateEmbedding
from MetadataExtractor import MetadataExtractor
from SupabaseVectorStore import SupabaseVectorStore
from TextFormater import TextFormater
from TextSpliter import TextSpliter
from Helper import word_count_less_than, remove_duplicated, clean_text

paragraph_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=0)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)

directory_path = './ebooks'
file_index = 0
sentence_index = 0
file_output_format = "md"

SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_ebook"
supabase = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)

for root, _, files in os.walk(directory_path):
  for file in files:
    file_path = os.path.join(root, file)
    filename = os.path.splitext(file)[0]
    md_file_path = os.path.join(root, f"{filename}.{file_output_format}")

    # check if md_file_path exists
    if os.path.exists(md_file_path) == False:
      print(f"Processing {file_path} => {md_file_path}")
      cmd = f"docling {file_path} --output {directory_path} --to {file_output_format} --table-mode accurate"
      process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout, stderr = process.communicate()  # Wait for the command to finish

    print(f"Finish file: {file_index} - {md_file_path}")

    loader = TextLoader(file_path=md_file_path)
    documents = loader.load()
    paragraphs = paragraph_splitter.split_documents(documents)

    for paragraph in paragraphs:
      try:
        if isinstance(paragraph, str):
          paragraph = paragraph
        else:
          paragraph = paragraph.page_content
        
        paragraph = clean_text(paragraph)
        paragraph = TextFormater(paragraph).run()

        print(f"oooooooooooo Processing paragraph:\n{paragraph}")

        chunks_response = TextSpliter(paragraph).run()

        chunks = [chunk for chunk in chunks_response.split("VNLPAGL")]
        chunks = remove_duplicated(chunks)

        for chunk in chunks:
          chunk = clean_text(chunk)
          if word_count_less_than(chunk, 5):
            continue

          datadata_responses = MetadataExtractor(chunk).run()
          metadatas = [metadata for metadata in datadata_responses.split("VNLPAGL") if len(metadata) > 10]
          metadatas = remove_duplicated(metadatas)
        
          for metadata in metadatas:
            metadata = filename + ":" + metadata.strip()
            embedding = CreateEmbedding(chunk).run()
            embedding2 = CreateEmbedding(metadata).run()
            supabase.insert_embedding(text=chunk, embedding=embedding, metadata=metadata, embedding2=embedding2)
            print(f"............ {chunk}\n")
            print(f">>>>>>>>>>>> {metadata}\n")
            print(f"File {file_index}/{len(files)} - Sentence {sentence_index}\n")
            
            sentence_index += 1

      except Exception as e:
        print(f"\n\n\n\n\nErrorn Errorn Errorn Error {file_index}/{len(files)}\n {chunk} {e}\n\n\n\n\n")
      
    file_index += 1
