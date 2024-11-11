from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.chains import create_extraction_chain
from typing import Optional, List
from langchain.chains import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import pandas as pd
import os
import subprocess

class OllamaEndpoint:
    def __init__(self, message: str, url: str = "http://localhost:11434/api/generate", model: str = "llama3.2:latest"):
        self.message = str(message)
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at analyzing and extracting key sentences from a document.
        1. Each key sentence can contain 1 to 3 original sentences.
        2. Each key sentence should not exceed 200 characters.
        3. Each key sentence should contain meaningful information.
        4. Ignore key sentences that contain only numbers or special characters.
        5. Ignore key sentences that contain less than 7 words.
        6. For code, always try to keep them together as one key sentence.
        7. Dont return blank sentences, or sentence with only special characters.

        Here are the sentences from the document. Please truncate them into key sentences, each on a new line.
        Return only the key sentences, nothing else, no extra information or explanations.
        """

    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            self.url,
            json={"model": self.model, "prompt": self.base_prompt + self.message, "stream": False}
        )
        
        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        
        # Clean and format the JSON response
        return self._clean_json_response(response.json())

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response


class OllamaEmbeddingEndpoint:
    def __init__(self, message: str, url: str = "http://localhost:11434/api/embed", model: str = "nomic-embed-text:137m-v1.5-fp16"):
        self.message = str(message)
        self.url = url
        self.model = model
    
    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            self.url,
            json={"model": self.model, "input": self.message}
        )
        
        # Check if the response is successful
        response_data = response.json()
        
        # Extract embeddings from the response data, assuming it's stored under a key called "embeddings"
        embeddings = response_data.get("embeddings")
        if embeddings is None:
            raise ValueError("No embeddings found in the response.")
        
        # Return the embeddings
        return embeddings[0]
    
class SupabaseVectorStore:
    def __init__(self, url: str, token: str, table_name: str):
        self.url = url
        self.token = token
        self.table_name = table_name
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "apikey": self.token  # Supabase requires both Authorization and apikey headers
        }

    def insert_embedding(self, text: str, embedding: list[float]):
        """
        Inserts an embedding into the Supabase Postgres database.
        
        :param text: The original text for which the embedding was created.
        :param embedding: A list of floats representing the embedding vector.
        :return: The response from the Supabase API call.
        """
        data = {
            "content": text,
            "metadata": {},
            "embedding": embedding
        }
        
        response = requests.post(
            f"{self.url}/rest/v1/{self.table_name}",
            headers=self.headers,
            json=data
        )

        # Check if the insertion was successful
        if response.status_code != 201:
            raise Exception(f"Failed to insert embedding: {response.status_code}, {response.text}")
        
        return True

directory_path = './documents'
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

file_index = 0
sentence_index = 0

# Define Supabase credentials
SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_norm"

supabase = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)

for root, _, files in os.walk(directory_path):
  for file in files:
    file_path = os.path.join(root, file)
    filename = os.path.splitext(file)[0]
    md_file_path = os.path.join(root, f"{filename}.md")

    print(f"Processing {file_path} => {md_file_path}")
    cmd = f"docling {file_path} --output {directory_path}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()  # Wait for the command to finish

    print(f"Finish file: {file_index} - {md_file_path}")

    # read the file
    try:
      loader = TextLoader(file_path=md_file_path)
      documents = loader.load()
      chunked_texts = text_splitter.split_documents(documents)
    except Exception as e:
      print(f"Error loading documents: {e}")
      continue

    for chunk in chunked_texts:
      try:
        ollama_response = OllamaEndpoint(chunk, model="codegemma:7b-instruct-v1.1-q8_0").run()
        sentences = [sentence for sentence in ollama_response.split("\n") if len(sentence) > 9]
      except Exception as e:
        print(f"Error extracting sentences: {e}")
        continue
    
    for sentence in sentences:
        sentence = filename + ": " + sentence.strip()
        print(f"File {file_index}/{len(files)} Sentence {sentence_index}: {sentence}")
        try:
            embedding = OllamaEmbeddingEndpoint(sentence).run()
            supabase.insert_embedding(sentence, embedding)
            print(f"File {file_index}/{len(files)} Inserted embedding for: {sentence}")
        except Exception as e:
            print(f"File {file_index}/{len(files)} Error inserting embedding for: {sentence}")
        
        sentence_index += 1
    file_index += 1
