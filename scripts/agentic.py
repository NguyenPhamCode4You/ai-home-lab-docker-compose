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
        You are an expert in analyzing markdown documents and extracting key sentences that convey essential information. Follow these guidelines to extract meaningful content:

        1. Key Sentence Composition: Each key sentence should consist of 1 to 3 sentences from the original text.
        2. Length Restriction: Limit each key sentence to a maximum of 200 characters.
        3. Informational Value: Each key sentence must convey meaningful information, ignoring sentences that contain only numbers, special characters, or fewer than 7 words.
        4. Code Blocks: When a sentence includes code, keep it as one key sentence.
        5. Exclusion of Blank or Irrelevant Sentences: Do not return blank sentences or sentences with only special characters.
        6. Markdown Titles as Keywords: Precede each key sentence with the title of its markdown section in square brackets as a keyword for context (e.g., [Introduction]).
        7. Seperated Sentences: Each key sentence should be separated by a "VNLPAGL".
        
        Here is an example of how to format your output:

        Example -----------------------------------------------------
        # Introduction
        Markdown is a lightweight markup language with plain-text formatting syntax. 

        ## Features
        Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.

        ## Example Code
        ```python
        def hello_world():
            print("Hello, world!")
        ```
        End of example.----------------------------------------------

        Output:
        VNLPAGL[Introduction] Markdown is a lightweight markup language with plain-text formatting.
        VNLPAGL[Introduction][Features] It is designed so that it can be converted to HTML and many other formats using a tool by the same name.
        VNLPAGL[Introduction][Features] Markdown supports headers, lists, emphasis, links, images. Syntax is designed for readability.
        VNLPAGL[Introduction][Example Code] ```python def hello_world(): print("Hello, world!") ```

        Here is another example of table:

        Example -----------------------------------------------------
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |

        ## Summary
        Product B has the highest rating and is recommended for users seeking premium features.
        End of example.----------------------------------------------

        Output:
        VNLPAGL[Product Comparison] Product A is affordable and high-quality, priced at $10 with a 4.5 rating.
        VNLPAGL[Product Comparison] Product B, priced at $20, is premium quality with extra features and a 4.8 rating.
        VNLPAGL[Product Comparison] Product C offers good value at $15 with a 4.2 rating.
        VNLPAGL[Summary] Product B has the highest rating and is recommended for premium features.

        Note:
        - Always put the title of the markdown section in square brackets before the key sentence.
        - For lines contain only the title, ignore them.
        - For code blocks, keep them as one key sentence, if they are too long, put the function name or the main idea of the code block as the title.

        Example -----------------------------------------------------
        # Data Processing Code
        ```python
        def process_data(data):
            # This function processes data by cleaning and transforming it
            cleaned_data = [item.strip().lower() for item in data if isinstance(item, str)]
            transformed_data = [int(item) for item in cleaned_data if item.isdigit()]
            return transformed_data
        ```
        End of example.----------------------------------------------

        Output
        VNLPAGL[Data Processing Code] ```python def process_data(data): cleaned_data = [item.strip().lower() for item in data if isinstance(item, str)]; ```
        VNLPAGL[Data Processing Code] ```python def process_data(data): transformed_data = [int(item) for item in cleaned_data if item.isdigit()]; return transformed_data```

        Again, always use "VNLPAGL" to separate key sentences.
        Now, please extract the key sentences from the following text: 
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
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

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
    if (file_path.endswith(".md") == True):
      print(f"Skipping {file_path}")
      file_index += 1
      continue

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
      if isinstance(chunk, str):
        chunk = chunk
      else:
        chunk = str(chunk)
      chunk = chunk.strip()
      chunk = chunk.replace("\n", " ")
      chunk = chunk.replace("\r", " ")
      chunk = chunk.replace("\t", " ")
      chunk = chunk.replace("  ", "")
      try:
        ollama_response = OllamaEndpoint(chunk, model="codegemma:7b-instruct-v1.1-q8_0").run()
        sentences = [sentence for sentence in ollama_response.split("VNLPAGL") if len(sentence) > 7]
      except Exception as e:
        print(f"Error extracting sentences: {e}")
        continue
    
      for sentence in sentences:
        if len(sentence) < 10 or sentence.isspace() or "**" in sentence or "----" in sentence:
          continue
        sentence = filename + ": " + sentence.strip()
        try:
            embedding = OllamaEmbeddingEndpoint(sentence).run()
            supabase.insert_embedding(sentence, embedding)
            print(f"File {file_index}/{len(files)} Success embedding for: {sentence}")
        except Exception as e:
            print(f"File {file_index}/{len(files)} Error inserting embedding for: {sentence}")
        
        sentence_index += 1
    file_index += 1
