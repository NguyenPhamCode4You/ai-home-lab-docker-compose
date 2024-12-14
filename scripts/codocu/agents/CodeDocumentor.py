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
class CodeDocumentor:
    def __init__(
        self,
        url: str = "http://localhost:11434",
        model: str = "gemma2:9b-instruct-q8_0",
        embedder = None,
        vector_store = None,
        base_prompt: str = None,
        document_extractor = None,
        max_context_tokens_length: int = 5500,
        max_history_tokens_length: int = 500,
        hosting_url: str = "http://localhost:11434",
        match_count: int = 100,
    ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.embedder = embedder                    
        self.vector_store = vector_store                
        self.base_prompt = base_prompt
        self.be_host_url = hosting_url
        self.match_count = match_count
        self.max_context_tokens_length = max_context_tokens_length   
        self.max_history_tokens_length = max_history_tokens_length
        self.document_extractor = document_extractor
    
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
    
    async def analyze(self, original_folder_path: str, result_folder_path: str, allowed_file_extensions: List[str] = [], ignored_file_pattern: List[str] = [], document_writter = None, summarizer = None, keyword_extractor = None):
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
                async for blob_extractor in self.document_extractor.stream(question, paragraphs_validation_string):
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
                    try:
                        header1 = RemoveSpecialCharacters(validated_header).replace(" ", "").lower()
                        for original_header, paragraph_content in original_paragraphs:
                            header2 = RemoveSpecialCharacters(original_header).replace(" ", "").lower()
                            if header1 != header2:
                                continue
                            knowledge_context += f"\n{file_link}:\n{original_header.strip()}: {paragraph_content}\n\n"
                            header_name_display = RemoveSpecialCharacters(original_header)
                            header_document = {"content": document["content"], "metadata": {"f": header_name_display}}
                            header_link = format_document_url(header_document, highlight=header_name_display, host_url=self.be_host_url)
                            yield json.dumps({"response": f"\n- Learned ✅ **{header_link}** into **Memory**: {len(knowledge_context)}/{self.max_context_tokens_length} tokens ... \n\n"})
                            await asyncio.sleep(2)
                            break
                    
                    except Exception as e:
                        print(f"Error in combining headers: {str(e)}")
                        yield json.dumps({"response": f"❌ Error in combining headers: {e}"})
                        continue

                if len(knowledge_context) >= self.max_context_tokens_length:
                    break

            except Exception as e:
                print(f"Error in combining headers: {str(e)}")
                yield json.dumps({"response": f"❌ Error in validating documents headers: {e}"})
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
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk


def add_query_param(base_url, param_name, param_value):
    """
    Add a query parameter to a URL.

    :param base_url: The base URL (string).
    :param param_name: The name of the query parameter (string).
    :param param_value: The value of the query parameter (string).
    :return: The full URL with the query parameter (string).
    """
    # Encode the query parameter
    query = {param_name: param_value}
    encoded_query = urlencode(query)
    
    # Join the base URL and the encoded query parameter
    if "?" in base_url:
        # If there are already query parameters, append using '&'
        return f"{base_url}&{encoded_query}"
    else:
        # Otherwise, add the '?' and the parameter
        return f"{base_url}?{encoded_query}"

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
        highlight = highlight.replace("(", "").replace(")", "")
        document_url = add_query_param(document_url, "highlight", highlight)
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

def is_allowed_file(file_path, allowed_file_extensions: List[str], ignored_file_pattern: List[str]):
    if not any(file_path.endswith(ext) for ext in allowed_file_extensions):
        return False
    
    if not is_allowed_path(file_path, ignored_file_pattern):
        return False
    
    return True

def is_allowed_path(file_path, ignored_file_pattern: List[str]):
    if any(pattern in file_path for pattern in ignored_file_pattern):
        return False
    
    return True

def RecursiveSplitLines(document: str, limit: int = 1000):
    lines = document.split("\n")
    paragraphs = []
    paragraph = ""
    for line in lines:
        if len(paragraph) + len(line) < limit:
            paragraph += f"{line}\n"
        else:
            paragraphs.append(paragraph)
            paragraph = f"{line}\n"

    if len(paragraph) > 0:
        paragraphs.append(paragraph)

    return paragraphs