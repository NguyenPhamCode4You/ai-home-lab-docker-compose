import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import pandas as pd
import os
import subprocess

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "codegemma:7b-instruct-v1.1-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class ChunkedTextExtractor:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in analyzing markdown documents and extracting key sentences that convey essential information. Follow these guidelines to extract meaningful content:

        1. Key Sentence Composition: Each key sentence should consist of 1 to 3 sentences from the original text.
        2. Length Restriction: Limit each key sentence to a maximum of 250 characters.
        3. Replace the markdown title with the bracketed title, e.g., ## title -> [title].
        
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
        VNLPAGL[Features] It is designed so that it can be converted to HTML and many other formats using a tool by the same name. Markdown supports headers, lists, emphasis, links, images. Syntax is designed for readability.
        VNLPAGL[Example Code] ```python def hello_world(): print("Hello, world!") ```

        6. For table, put the column name before the value, also dont forget the Markdown Titles as Keyword!
        Here is the example of a table:

        Example -----------------------------------------------------
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |
        End of example.----------------------------------------------

        Output:
        VNLPAGL[Product Comparison] Product: Product A, Price: 10, Rating: 4.5, Description: Affordable and high-quality.
        VNLPAGL[Product Comparison] Product: Product B, Price: 20, Rating: 4.8, Description: Premium quality with extra features.
        VNLPAGL[Product Comparison] Product: Product C, Price: 15, Rating: 4.2, Description: Good value for the price.

        7. For Code block, always try to put them together as one row. 
        8. If Code blocks are too long, seperated rows should also contain the function name at the beginning!

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

        Again, Important Notes:
        - Always use "VNLPAGL" to separate key sentences.
        - Always put the title of the markdown section in square brackets before the key sentence.
        - For code blocks, try to keep them as one key sentence. If they are too long, put the function name or the main idea of the code block at the beginning!.
        
        Now, please extract the key sentences from the following text: 
        """

    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            ollama_instruct_url,
            json={"model": ollama_instruct_model, "prompt": self.base_prompt + self.message, "stream": False}
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

class MetadataExtractor:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in analyzing markdown documents and extracting key purposes that convey essential topic of discussion of the paragraph or sentences.
        When receiving the paragraph or sentences, follow the guidelines below to extract the key purposes:

        1. Split sentences: Split the paragraph or sentences into groups of related sentences.

        Then, for each group of sentences:
        2. Analyze the Purpose: Identify the main idea or purpose the sentences.
        3. Then, Output the following Format: 
          - [k]: Commas separated keywords mentioned in the paragraph or sentences.
          - [a]: Verbs or adjectives that describe properties or actions in the paragraph or sentences.
          - [s]: A brief summary of the main idea or purpose, less than 100 characters.

        4. For each group of sentences, use "VNLPAGL" to separate the groups.

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
        VNLPAGL[k]: Markdown [a]: lightweight [s]: Markdown is a lightweight markup language with plain-text formatting syntax, supports headers, lists, emphasis, links, images.
        VNLPAGL[k]: python, code, hello_world, [a]: code [s]: Example code that prints "Hello, world!".

        5. For table, put the table name in the [k] section, column names in the [a] section and summarize the purpose of table in the [s] section.
        Here is the example of a table:

        Example -----------------------------------------------------
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |
        End of example.----------------------------------------------

        Output:
        VNLPAGL[k]: Product Comparison [a]: Price, Rating, Description [s]: Comparing products based on price, rating, and description for Product A, Product B, and Product C.

        6. For Code block, put the function name or the main idea of the code block in the [k] section, important variables or parameters in the [a] section and summarize the purpose of the code block in the [s] section.

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
        VNLPAGL[k]: process_data, code [a]: cleaned_data, transformed_data [s]: This function processes data by cleaning and transforming it using python.

        Again, Important Notes:
        - Always use "VNLPAGL" to separate key sentences.
        - Always include [k], [a], and [s] in the output.
        - [k] should contain keywords, [a] should contain verbs or adjectives, and [s] should contain a brief summary, less than 100 characters.
        
        Now, please extract the key sentences from the following text:  
        """

    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            ollama_instruct_url,
            json={"model": ollama_instruct_model, "prompt": self.base_prompt + self.message, "stream": False}
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


class CreateEmbedding:
    def __init__(self, message: str):
        self.message = str(message)
    
    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            ollama_embeding_url,
            json={"model": ollama_embeding_model, "input": self.message}
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

    def insert_embedding(self, text: str, embedding: list[float], metadata: str = ""):
        """
        Inserts an embedding into the Supabase Postgres database.
        
        :param text: The original text for which the embedding was created.
        :param embedding: A list of floats representing the embedding vector.
        :return: The response from the Supabase API call.
        """
        data = {
            "content": text,
            "metadata": { "extracted": metadata },
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
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=10)

file_index = 0
sentence_index = 0

# Define Supabase credentials
SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_768"

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
        chunk = chunk.page_content
      
      chunk = chunk.strip()
      chunk = chunk.replace("\n", " ")
      chunk = chunk.replace("\r", " ")
      chunk = chunk.replace("\t", " ")
      chunk = chunk.replace("  ", "")

      if len(chunk) < 10 or chunk.isspace() or "**" in chunk or "----" in chunk:
        continue
      try:
        datadata_responses = MetadataExtractor(chunk).run()
        metadatas = [metadata for metadata in datadata_responses.split("VNLPAGL") if len(metadata) > 10]
      except Exception as e:
        print(f"Error extracting sentences: {e}")
        continue
    
      for metadata in metadatas:
        metadata = filename + ":" + metadata.strip()
        try:
            embedding = CreateEmbedding(metadata).run()
            # supabase.insert_embedding(sentence, embedding)
            supabase.insert_embedding(text=chunk, embedding=embedding, metadata=metadata)
            print(f">>>>> File {file_index}/{len(files)} Chunk:\n\n\n {chunk}\n\n\n")
            print(f">>>>>>> {metadata}\n\n\n\n\n\n")
        except Exception as e:
            print(f"\n\n\n\n\nErrorn Errorn Errorn Error {file_index}/{len(files)}\n {chunk}\n\n\n\n\n")
        
        sentence_index += 1
    file_index += 1
