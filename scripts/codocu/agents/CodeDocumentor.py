import asyncio
import json
import re
from shlex import quote
from fastapi import Request
import httpx
import requests
from typing import List, Optional

markdown_header_pattern = r"^(#+[ ]*.+)$"

def read_file_content(file_path):
    """Reads content from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def convert_paragraphs_for_validation(paragraphs):
    """Extracts and validates headers from file chunks."""
    result = []
    for header, content in paragraphs:
        if len(content) >= 100 and not any(
            kw in header.lower() for kw in ["example", "test", "summary", "keyword", "general"]
        ):
            if "Explanation" in content:
                explanation = content.split("Explanation", 1)[1]
            else:
                explanation = content
            result.append((f"**{header.strip()}**", explanation[:250].strip()))
    return result

def format_document_url(document, highlight: str = None, host_url: str = None) -> str:
    relative_path = document["content"].strip().replace("\\", "/")
    file_name = RemoveSpecialCharacters(document["metadata"]["f"])
    document_url = f"markdown-viewer?path={relative_path}"
    if host_url:
        document_url = f"{host_url}/{document_url}"
    if highlight:
        document_url += f"&highlight={quote(highlight)}"
    return f"[{file_name}]({document_url})"

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

def RemoveSpecialCharacters(text: str) -> str:
    text = re.sub(r"[^a-zA-Z]+", "", text)
    return text

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
        yield json.dumps({"response": f"📚 Finding top {self.match_count} documents basing on relevance level ...\n\n"})
        question_embedding = self.embedder.run(question)
        documents = self.vector_store.query_documents(query_embedding=question_embedding, match_count=self.match_count)
        # ---------------------------------------
        # 1.Verbosely list the documents
        # ----------------------------------------
        for file_index, document in enumerate(documents):
            file_link = format_document_url(document, host_url=self.be_host_url)
            yield json.dumps({"response": f"📌 Document {file_index + 1}: {file_link}\n"})
            await asyncio.sleep(0.25)
        
        yield json.dumps({"response": f"\n\n### 🤖 Start the reading process... \n\n\n"})
        knowledge_context = ""
        # ---------------------------------------
        # 2. Iterate through each document...
        # ----------------------------------------
        for file_index, document in enumerate(documents):
            file_link = format_document_url(document, host_url=self.be_host_url)
            if len(knowledge_context) >= self.max_context_tokens_length: 
                break
            try:
                file_context = read_file_content(document["content"])
            except Exception as e:
                print(f"Error reading file: {file_link}, {str(e)}")
                yield json.dumps({"response": f"\n\n ❌ Error reading file: {file_link} 👀 - File: **{file_index + 1}**/**{len(documents)}**\n\n"})
                continue
            
            try:
                original_paragraphs = ExtractMarkdownHeadersAndContent(file_context)
                yield json.dumps({"response": f"\n\n 📖 Reading file: {file_link} 👀 - File: **{file_index + 1}**/**{len(documents)}** - Found **{len(original_paragraphs)}** paragraphs...\n\n"})

                paragraphs_to_validate = convert_paragraphs_for_validation(original_paragraphs)
                paragraphs_validation_string = "\n\n".join([f"{header}: {content}" for header, content in paragraphs_to_validate])

                validation_result = ""
            except Exception as e:
                print(f"Error extracting file: {file_link}, {str(e)}")
                yield json.dumps({"response": f"❌ Error in extracting file: {file_link}, {str(e)}"})
                continue
            
            await asyncio.sleep(1)

            try:
                async for blob_extractor in self.code_block_extractor.stream(question, paragraphs_validation_string):
                    if (len(blob_extractor) > 1000):
                        continue
                    validation_result += json.loads(blob_extractor)["response"]
                    yield blob_extractor
            
            except Exception as e:
                print(f"Error in calling validation method: {str(e)}")
                yield json.dumps({"response": f"❌ Error in calling validation method: {str(e)}"})
                continue

            try:
                validated_headers = [
                    header.split(":", 1)[0].strip()
                    for header in validation_result.split("\n")
                    if ":" in header
                ]

                for validated_header in validated_headers:
                    header1 = RemoveSpecialCharacters(validated_header).replace(" ", "").lower()
                    for original_header, paragraph_content in original_paragraphs:
                        header2 = RemoveSpecialCharacters(original_header).replace(" ", "").lower()
                        if header1 != header2:
                            continue
                        knowledge_context += f"\n{file_link}:\n{original_header.strip()}: {paragraph_content}\n\n"
                        yield json.dumps({"response": f"\n- Learned ✅ **{original_header.strip()}** into **Memory**: {len(knowledge_context)}/{self.max_context_tokens_length} tokens ... \n\n"})
                        await asyncio.sleep(2)
                        break

                if len(knowledge_context) >= self.max_context_tokens_length:
                    break

            except Exception as e:
                print(f"Error in combining headers: {str(e)}")
                yield json.dumps({"response": f"❌ Error in combining headers: {str(e)}"})
                continue

        await asyncio.sleep(1)
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

        # ---------------------------------------
        # 6. Stream final explanation for the question
        # ----------------------------------------
        yield json.dumps({"response": f"\n ✨ Total relevant tokens: {len(knowledge_context)}/{self.max_context_tokens_length} 👀 \n\n"})
        await asyncio.sleep(1)
        yield json.dumps({"response": f"\n### 🎯 Lets have one final revise for the question: ...\n\n"})
        await asyncio.sleep(1)
        
        async with httpx.AsyncClient() as client:
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
