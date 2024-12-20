import asyncio
import json
import os
import re
import httpx
from typing import List
from urllib.parse import urlencode

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class CodeSnippetProvider:
    def __init__(
        self,
        url: str = "http://localhost:11434",
        model: str = "gemma2:9b-instruct-q8_0",
        embedder = None,
        vector_store = None,
        base_prompt: str = None,
        max_context_tokens_length: int = 5500,
        match_count: int = 100,
    ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.embedder = embedder                    
        self.vector_store = vector_store                
        self.match_count = match_count
        self.max_context_tokens_length = max_context_tokens_length   
        self.base_prompt = base_prompt or """
        You are an experienced software developer and your task is reading a code document to answer user questions.
        Here is the code document you need to read:
        {context}
        User Question: {question}
        Try your very best to assist the user with their question.
        """
    
    
    async def learn(self, folder_path: str, keyword_extractor = None) -> str:
        if not self.embedder or not self.vector_store:
            raise ValueError("Embedder and vector store must be set before learning.")
        
        file_index = 1
        line_index = 1

        print(f"Learning from documents in {folder_path}...")

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                filename = os.path.splitext(file)[0]
                try:
                    with open(file_path, 'r', encoding="utf-8") as file:
                        document = file.read()
                except Exception as e:
                    print(f"Error: {e}")
                    continue

                sections = SplitByMarkdownHeader(document)
                section_index = 1

                for section in sections:
                    try:
                        header, content = ExtractMarkdownHeadersAndContent(section)[0]
                    except Exception as e:
                        print(f"Error: {e}")
                        header, content = "", section

                    if "Explanation" not in content:
                        continue

                    try:
                        code_block = content.split("Explanation")[0]
                        explaination = content.split("Explanation")[1]

                        keywords = keyword_extractor.run(code_block)
                        metadata = {"f": filename, "k": keywords, "h": header}
                        content = f"{header}: {code_block}"

                        embedding = self.embedder.run(metadata)
                        embedding2 = self.embedder.run(explaination)

                        print(f"\nEmbedding1: {metadata}")
                        print(f"\nEmbedding2: {explaination}")
                        print(f"\nContent: {content}")
                        self.vector_store.insert_document({"content": content, "embedding": embedding, "embedding2": embedding2, "metadata": metadata, "summarize": explaination})
                        print(f"\noooooooooooooooooooo File {file_index}/{len(files)} - Line {line_index} - Section {section_index}/{len(sections)} - {file_path} oooooooooooooooooooo")
                    except Exception as e:
                        print(f"Error: {e}")
                    line_index += 1
                section_index += 1
            file_index += 1
    
    async def stream(self, question: str, messages: List[Message] = None):
        prompt = self.get_final_prompt(question, messages)
        print(f"Prompt: {prompt}")
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    # Organize retrieved documents into structured sections
    def organize_documents(self, documents: List[dict]) -> List[dict]:
        # Extract titles and organize by unique titles
        titles = [document["content"].split(":")[0] for document in documents]
        unique_titles = list(dict.fromkeys(titles))

        sections = []
        for title in unique_titles:
            counts = len([doc for doc in documents if doc["content"].split(":")[0] == title])
            docs = [
                document["content"].replace(title, "", 1).replace(":", "", 1).strip()
                for document in documents
                if document["content"].split(":")[0] == title
            ]
            context = "\n".join(docs)

            sections.append({"title": title, "counts": counts, "context": context})

        return sections
    
    def get_final_prompt(self, question: str, messages: List[Message] = None) -> str:
        context = self.retrieve_documents(question)
        context = context[:self.max_context_tokens_length]
        prompt = (
            self.base_prompt
            .replace("{context}", context)
            .replace("{question}", question)
        )
        return prompt

    # Retrieve documents relevant to the question
    def retrieve_documents(self, question: str) -> str:
        if not self.embedder or not self.vector_store:
            raise ValueError("Embedder and vector store must be set before retrieving documents.")
        
        question_embedding = self.embedder.run(question)
        documents = self.vector_store.query_documents(query_embedding=question_embedding, match_count=self.match_count)

        sections = self.organize_documents(documents)
        context = ""
        for section in sections:
            context += f"""\n# {section["title"]}:\n{section['context']}"""
        return context
        

markdown_header_pattern = r"^(#+[ ]*.+)$"

def SplitByMarkdownHeader(message: str):
    """
    Splits a Markdown message into chunks by headers and their associated content.

    Args:
        message (str): The Markdown message.

    Returns:
        list: List of chunks, where each chunk contains a header and its content.
    """
    parts = re.split(markdown_header_pattern, message, flags=re.MULTILINE)
    
    # Reconstruct chunks with headers and associated content
    chunks = []
    for i in range(1, len(parts), 2):  # Headers are in odd indices
        header = parts[i].strip()  # Strip unnecessary whitespace
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        chunks.append(f"{header}\n{content}")
    return chunks

def ExtractMarkdownHeadersAndContent(text):
    # Split the text into parts based on headers
    parts = re.split(markdown_header_pattern, text, flags=re.MULTILINE)
    # Group headers with their associated content
    header_content_pairs = []
    for i in range(1, len(parts), 2):  # Headers are in odd indices
        header = parts[i].strip()  # Strip whitespace from the header
        header = header.replace("#", " ")  # Replace newline characters with spaces
        header = header.replace("  ", "")  # Replace newline characters with spaces
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""  # Get content after the header
        header_content_pairs.append((header, content))
    
    return header_content_pairs