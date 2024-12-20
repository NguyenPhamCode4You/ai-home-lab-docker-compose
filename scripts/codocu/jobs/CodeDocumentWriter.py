import asyncio
import json
import os
import re
import httpx
from typing import List
from urllib.parse import urlencode

# Main assistant class
class CodeDocumentWriter:
    def __init__(
        self,
        url: str = "http://localhost:11434",
        model: str = "gemma2:9b-instruct-q8_0",
    ):
        self.url = f"{url}/api/generate"
        self.model = model
    
    async def write_documents(self, original_folder_path: str, result_folder_path: str, allowed_file_extensions: List[str] = [], ignored_file_pattern: List[str] = [], document_writter = None, summarizer = None):
        if not document_writter or not summarizer or not keyword_extractor:
            raise ValueError("Code documentor, code summarizer, and keyword extractor must be set before writing documents.")
        
        root_folder_name = original_folder_path.split("\\")[-1]
        output_path = f"{result_folder_path}\\{root_folder_name}"

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        files_list = []
        for root, _, files in os.walk(original_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if not is_allowed_file(file_path, allowed_file_extensions, ignored_file_pattern):
                    continue
                if file_path not in files_list:
                    files_list.append(file_path)

        file_index = 1
        for file_path in files_list:
            print(f"\n\n\n\n\noooooooooooooooooooo Processing File {file_index}/{len(files_list)} - {file_path} oooooooooooooooooooo \n\n\n\n\n")
            filename = os.path.basename(file_path)
            folder_path = file_path.replace(original_folder_path, "").replace(filename, "").strip("\\")
            try:
                with open(file_path, 'r', encoding="utf-8") as file:
                    file_content = file.read()

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue

            chunks = RecursiveSplitLines(file_content, 5000)
            document_content = ""
            document_summarize = ""
            document_keywords = set()  # Use a set to ensure uniqueness

            for chunk in chunks:
                try:
                    print(f"\n\nooooooooo Writing documentation for file {file_path} - Chunk: {len(chunk)} tokens \n\n")
                    await asyncio.sleep(1)
                    async for blob_extractor in document_writter.stream(chunk):
                        if (len(blob_extractor) > 1000):
                            continue
                        agent_response = json.loads(blob_extractor)["response"]
                        document_content += agent_response
                        print(agent_response, end="", flush=True)  # Real-time console output

                    print(f"\n\nooooooooo Summarizing file {file_path} - Chunk: {len(chunk)} tokens \n\n")
                    await asyncio.sleep(1)
                    async for blob_extractor in summarizer.stream(chunk):
                        if (len(blob_extractor) > 1000):
                            continue
                        agent_response = json.loads(blob_extractor)["response"]
                        document_summarize += agent_response
                        print(agent_response, end="", flush=True)  # Real-time console output

                    print(f"\n\nooooooooo Extracting keywords for file {file_path} - Chunk: {len(chunk)} tokens \n\n")
                    await asyncio.sleep(1)

                    chunk_keywords = keyword_extractor.run(chunk)
                    print(chunk_keywords, end="", flush=True)  # Real-time console output
                    chunk_keywords_set = {keyword.strip() for keyword in chunk_keywords.split(",")}
                    document_keywords.update(chunk_keywords_set)
                
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                    continue

            final_summary = ""
            if len(chunks) > 1:
                print(f"\n\nooooooooo Write final Summzry for file {file_path} - Full Document: {len(document_summarize)} tokens \n\n")
                async for blob_extractor in summarizer.stream(document_summarize):
                    if (len(blob_extractor) > 1000):
                        continue
                    agent_response = json.loads(blob_extractor)["response"]
                    final_summary += agent_response
                    print(agent_response, end="", flush=True)
            else:
                final_summary = document_summarize

            # get unique keywords
            final_keywords = ", ".join(sorted(document_keywords))
            document_content += f"\n\n#### Summary:\n {final_summary}"
            document_content += f"\n\n#### Keywords:\n {final_keywords}"

            try:
                processed_folder_path = os.path.join(output_path, folder_path)
                processed_file_name = filename.replace(original_folder_path, "")
                processed_file_path = os.path.join(processed_folder_path, f"{processed_file_name}.md")

                if not os.path.exists(processed_folder_path):
                    os.makedirs(processed_folder_path)

                with open(processed_file_path, 'w', encoding="utf-8") as f:
                    f.write(document_content)
                    print(f"File Analyzed: {processed_file_path}")
            
            except Exception as e:
                print(f"Error writing file {processed_file_path}: {e}")
                continue

            metadata = {"f": filename, "p": processed_file_path, "k": final_keywords}
            embedding = self.embedder.run(metadata)
            embedding2 = self.embedder.run(final_summary)

            self.vector_store.insert_document({"content": processed_file_path, "embedding": embedding, "embedding2": embedding2, "metadata": metadata, "summarize": final_summary})
            print(f"\n\n\n\nooooooooo Document inserted: {processed_file_path} ooooooooo\n\n\n\n")
            file_index += 1

import httpx
import requests

class CodeSummarizer:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and you are asked to explain a code block.
        1. Explain should include the purpose of the code block and how it works, mention any important details.
        2. Should be clear and concise, but detailed enough to be understood by a junior developer.
        3. Total explanation should be no longer than 200 characters.
        Important: Just return the explanation, do not include any additional information, no code, no prompt.
        Explain the code block.
        Code Block:

        """

    def run(self, message: str) -> str:
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": self.base_prompt + str(message), "stream": False}
        )
        
        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        
        # Clean and format the JSON response
        return self._clean_json_response(response.json())
    
    async def stream(self, message: str):
        prompt = self.base_prompt + str(message)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response