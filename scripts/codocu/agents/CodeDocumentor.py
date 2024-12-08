import asyncio
import json
import re
from shlex import quote
from fastapi import Request
import httpx
import requests
from typing import List, Optional

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

def RemoveSpecialCharacters(text: str) -> str:
    return re.sub(r"[^a-zA-Z]+", "", text)

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class CodeDocumentor:
    def __init__(
        self,
        url: str = "http://localhost:11434/api/generate",
        model: str = "gemma2:9b-instruct-q8_0"
    ):
        self.url = url
        self.model = model
        self.embedder = None                    # Placeholder for an embedding function or model
        self.vector_store = None                # Placeholder for a vector database
        self.base_prompt = None
        self.be_host_url = None
        self.match_count = 100
        self.max_context_tokens_length = 5500   # 5500 is the best length for the context tokens, for typescript & PL questions
        self.max_history_tokens_length = 500    # 6000 is the maximum length, thus 6000 - 5500 = 500 for the history tokens
    
    def set_max_context_tokens_length(self, max_context_tokens_length: int):
        self.max_context_tokens_length = max_context_tokens_length
        return self
    
    def set_max_history_tokens_length(self, max_history_tokens_length: int):
        self.max_history_tokens_length = max_history_tokens_length
        return self

    def set_base_prompt(self, base_prompt: str):
        self.base_prompt = base_prompt
        return self

    # Setters to customize the instance
    def set_match_count(self, match_count: int):
        self.match_count = match_count
        return self

    def set_embedder(self, embedder):
        self.embedder = embedder
        return self

    def set_vector_store(self, vector_store):
        self.vector_store = vector_store
        return self
    
    def set_code_block_extractor(self, code_block_extractor):
        self.code_block_extractor = code_block_extractor
        return self
    
    def set_be_host_url(self, be_host_url: str):
        self.be_host_url = be_host_url
        return self
    
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
    
    async def stream(self, question: str, messages: List[Message] = None):
        if not self.embedder or not self.vector_store:
            raise ValueError("Embedder and vector store must be set before retrieving documents.")
        
        question_embedding = self.embedder.run(question)
        documents = self.vector_store.query_documents(query_embedding=question_embedding, match_count=self.match_count)
        if len(documents) == 0:
            yield json.dumps({"error": "No files found or smart file picker not set."})
            return
        
        def format_file_name(file_name: str, path: str, highlight: str = None) -> str:
            # Strip leading/trailing spaces
            file_name = file_name.strip()
            path = path.strip()

            # Ensure the path uses forward slashes
            relative_path = path.replace("\\", "/")

            # Build the Markdown Viewer URL
            markdown_viewer_url = f"markdown-viewer?path={relative_path}"
            if self.be_host_url:
                markdown_viewer_url = f"{self.be_host_url}/{markdown_viewer_url}"
            if highlight:
                markdown_viewer_url += f"&highlight={quote(highlight)}"

            # Return the formatted Markdown link
            return f"[{file_name}]({markdown_viewer_url})"
        
        current_file_index = 1
        
        async with httpx.AsyncClient() as client:
            yield json.dumps({"response": f"📚 Finding top {len(documents)} documents basing on relevance level ...\n\n"})
            await asyncio.sleep(2)
            for index, document in enumerate(documents):
                if (index + 1) > 10:
                    break
                file_path = document["content"]
                file_name = document["metadata"]["f"]
                file_name = format_file_name(file_name, file_path)
                yield json.dumps({"response": f"📌 Document {index + 1}: {file_name}\n"})
                await asyncio.sleep(0.25)

            yield json.dumps({"response": f"\n\n### 🤖 Start the reading process... \n\n\n"})
            await asyncio.sleep(2)

            knowledge_context = ""
            for index, document in enumerate(documents):
                if current_file_index > self.match_count:
                    break
                if len(knowledge_context) >= self.max_context_tokens_length:
                    break

                file_path = document["content"]
                file_name = document["metadata"]["f"]
                file_name = format_file_name(file_name, file_path)

                yield json.dumps({"response": f"\n📖✏️  Reading file: {file_name} 👀 - File: **{current_file_index}**/**{len(documents)}** \n\n"})
                await asyncio.sleep(2)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                        chunks = SplitByMarkdownHeader(content)
                        headers_list = []
                        for chunk in chunks:
                            header = chunk.split("\n")[0].replace("#", "").strip()
                            content = chunk.split("\n", 1)[1]

                            if len(content) < 100:
                                continue

                            if "example" in header or "test" in header or "demo" in header or "keyword" in header or "summary" in header or "note" in header or "general purpose" in header or "business logic" in header:
                                continue

                            headers_list.append(header)

                        header_block_string = ""
                        async for header_block in self.code_block_extractor.stream(question, "\n".join(headers_list)):
                            try:
                                header_block_string += json.loads(header_block)["response"]
                                yield header_block
                            except Exception as e:
                                yield ""
                                continue

                        headers_list = [header for header in header_block_string.split("\n") if len(header) > 0]

                        for chunk in chunks:
                            original_header = chunk.split("\n")[0].strip()
                            original_header = original_header.replace("#", "").strip()
                            header_1 = RemoveSpecialCharacters(original_header)
                            if len(header_1) == 0:
                                continue

                            for header_line in headers_list:
                                header_extracted = header_line.split(":")[0].strip()
                                header_extracted = header_extracted.replace("#", "").strip()
                                header_2 = RemoveSpecialCharacters(header_extracted)
                                if len(header_2) == 0:
                                    continue

                                if header_1.lower() in header_2.lower() or header_2.lower() in header_1.lower():
                                    knowledge_context += f"\n{file_name}:\n{chunk}"
                                    original_header_url = format_file_name(original_header, file_path, highlight="")
                                    yield json.dumps({"response": f"\n- Learned ✅ **{original_header_url}** into **Memmory**: {len(knowledge_context)}/{self.max_context_tokens_length} tokens ... \n\n"} )
                                    await asyncio.sleep(3)
                                    break

                            if len(knowledge_context) >= self.max_context_tokens_length:
                                break

                        current_file_index += 1

                        if len(knowledge_context) >= self.max_context_tokens_length:
                            break

                except Exception as e:
                    yield json.dumps({"response": f"\n⛔️ Error reading file: {file_name}, {str(e)}"})
                    continue

            knowledge_context = knowledge_context[:self.max_context_tokens_length]
            await asyncio.sleep(1)

            histories = ""
            if messages and len(messages) > 0:
                histories = "\n".join([f"{message.role}: {message.content}" for message in messages or []])
                histories = histories[-self.max_history_tokens_length:]

            prompt = (
                self.base_prompt
                .replace("{question}", question)
                .replace("{histories}", histories)
                .replace("{context}", knowledge_context)
            )
            
            yield json.dumps({"response": f"\n ✨ Total relevant tokens: {len(knowledge_context)}/{self.max_context_tokens_length} 👀 \n\n"})
            await asyncio.sleep(1)
            yield json.dumps({"response": f"\n### 🎯 Lets have one final revise for the question: {question} ...\n\n"})
            await asyncio.sleep(1)
            # Send streaming request to Ollama
            
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
    
    def run(self, question: str, messages: List[Message] = None) -> str:
        prompt = self.get_final_prompt(question, messages)

        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        
        return self._clean_json_response(response.json())
    
    # Run the assistant to answer the question
    def get_final_prompt(self, question: str, messages: List[Message] = None) -> str:
        histories = ""
        if messages and len(messages) > 0:
            histories = "\n".join([f"{message.role}: {message.content}" for message in messages or []])
            histories = histories[-self.max_history_tokens_length:]
        
        context = self.retrieve_documents(question)
        context = context[:self.max_context_tokens_length]

        prompt = (
            self.base_prompt
            .replace("{context}", context)
            .replace("{question}", question)
            .replace("{histories}", histories)
        )

        return prompt
    
    # Clean the API response
    def _clean_json_response(self, response_data: dict) -> str:
        return response_data.get("response", "")
