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

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
directory_path = './documents'
file_index = 0
sentence_index = 0
file_output_format = "md"

SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_768"
supabase = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)
    
def word_count_less_than(chunk, count = 7):
  # Keep only alphabetic characters and spaces
  cleaned_text = ''.join(char for char in chunk if char.isalpha() or char.isspace())
  # Split by spaces to get the words and count them
  word_count = len(cleaned_text.split())
  # Check if the word count is less than 5
  return word_count < count

def clean_text(text):
  # Remove newlines, tabs, and extra spaces
  cleaned_text = text.strip().replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ")
  cleaned_text = cleaned_text.replace("|||", "").replace("| |", "")
  cleaned_text = cleaned_text.replace(" | ", "-")
  cleaned_text = cleaned_text.replace("**", "").replace("--", "")

  return cleaned_text

for root, _, files in os.walk(directory_path):
  for file in files:
    file_path = os.path.join(root, file)
    if (file_path.endswith(f".{file_output_format}") == True):
      print(f"Skipping {file_path}")
      file_index += 1
      continue

    filename = os.path.splitext(file)[0]
    md_file_path = os.path.join(root, f"{filename}.{file_output_format}")

    print(f"Processing {file_path} => {md_file_path}")
    cmd = f"docling {file_path} --output {directory_path} --to {file_output_format} --table-mode accurate"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()  # Wait for the command to finish

    print(f"Finish file: {file_index} - {md_file_path}")

    loader = TextLoader(file_path=md_file_path)
    documents = loader.load()
    paragraphs = text_splitter.split_documents(documents)

    for paragraph in paragraphs:
      try:
        if isinstance(paragraph, str):
          paragraph = paragraph
        else:
          paragraph = paragraph.page_content
        
        paragraph = clean_text(paragraph)
        paragraph = TextFormater(paragraph).run()

        print(f"oooooooooooo Processing paragraph:\n{paragraph}\n")

        chunks_response = TextSpliter(paragraph).run()

        chunks = [chunk for chunk in chunks_response.split("VNLPAGL")]
        for chunk in chunks:
          chunk = clean_text(chunk)
          if word_count_less_than(chunk, 5):
            continue

          # chunk_validation_response = ChunkValidator(chunk).run()
          # print(f"Chunk: {chunk}\n")
          # print(f"======>>>: {chunk_validation_response}")
          # if "No" in chunk_validation_response.strip():
          #   continue

          datadata_responses = MetadataExtractor(chunk).run()
          metadatas = [metadata for metadata in datadata_responses.split("VNLPAGL") if len(metadata) > 10]
        
          for metadata in metadatas:
            metadata = filename + ":" + metadata.strip()
            embedding = CreateEmbedding(metadata).run()
            supabase.insert_embedding(text=chunk, embedding=embedding, metadata=metadata)
            print(f"............ {chunk}\n")
            print(f">>>>>>>>>>>> {metadata}\n")
            print(f"File {file_index}/{len(files)} - Sentence {sentence_index}\n")
      except Exception as e:
        print(f"\n\n\n\n\nErrorn Errorn Errorn Error {file_index}/{len(files)}\n {chunk} {e}\n\n\n\n\n")
      
      sentence_index += 1
    file_index += 1
