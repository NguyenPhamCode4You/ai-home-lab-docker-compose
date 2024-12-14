import os
import re
import httpx
import requests
from typing import List

class Message():
    role: str 
    content: str

def read_files_from(folderPath: str):
    return [file for _, _, files in os.walk(folderPath) for file in files]

# Main assistant class
class RagKnowledgeBase:
    def __init__(
        self,
        url: str = "http://localhost:11434",
        model: str = "gemma2:9b-instruct-q8_0",
        embedder = None,
        vector_store = None,
        base_prompt: str = None,
        match_count: int = 100,
        max_context_tokens_length: int = 5500,
        max_history_tokens_length: int = 500,
    ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.embedder = embedder
        self.vector_store = vector_store
        self.base_prompt = base_prompt
        self.match_count = match_count
        self.max_context_tokens_length = max_context_tokens_length
        self.max_history_tokens_length = max_history_tokens_length
    
    def organize_documents(self, documents: List[dict]) -> List[dict]:
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
        prompt = self.get_final_prompt(question, messages)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    async def formatting(self, original_folder_path: str, formatted_folder_path: str, chunk_size = 600, markdown_processor = None):
        if not markdown_processor:
            raise ValueError("Markdown processor must be set before formatting.")
        
        if not os.path.exists(formatted_folder_path):
            os.makedirs(formatted_folder_path)

        file_index = 1
        section_index = 1
        
        for root, _, files in os.walk(original_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                filename = os.path.splitext(file)[0]
                try:
                    with open(file_path, 'r', encoding="utf-8") as file:
                        document = file.read()
                except Exception as e:
                    print(f"Error: {e}")
                    continue

                formatted_chunks = []
                sections = SplitByMarkdownHeader(document)
                
                for section in sections:
                    section = RemoveExcessiveSpacing(section)
                    section_parts = [section]
                    header = False

                    if len(section) > chunk_size:
                        header, section = ExtractMarkdownHeadersAndContent(section)[0]
                        section_parts = RecursiveSplitSentences(section, chunk_size)

                    for section in section_parts:
                        if len(section) == 0:
                            continue
                        if header:
                            section = "##  " + header + "\n\n" + section
                        try:
                            section = RemoveExcessiveSpacing(section)
                            section = markdown_processor.run(section)
                            print(section)
                            formatted_chunks.append(section)
                            print(f"oooooooooooooooooooo File {file_index}/{len(files)} - Section {section_index}/{len(sections)} - {file_path} oooooooooooooooooooo \n\n\n\n\n")
                        except Exception as e:
                            print(f"Error: {e}")

                    section_index += 1

                formatted_file_path = os.path.join(formatted_folder_path, f"{filename}.md")
                try:
                    with open(formatted_file_path, 'w') as f:
                        f.write('\n'.join(formatted_chunks))
                except Exception as e:
                    print(f"Error: {e}")
                    
                file_index += 1

    async def learn(self, folder_path: str, line_extractor = None, keyword_extractor = None, sentence_summarizer = None) -> str:
        if not line_extractor or not sentence_summarizer or not keyword_extractor:
            raise ValueError("Line extractor and sentence summarizer must be set before learning.")
        if not self.embedder or not self.vector_store:
            raise ValueError("Embedder and vector store must be set before learning.")
        
        file_index = 1
        line_index = 1

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
                    lines = ""
                    try:
                        header, content = ExtractMarkdownHeadersAndContent(section)[0]
                        lines = line_extractor.run(content)
                    except Exception as e:
                        print(f"Error: {e}")
                        header, content = "", section

                    for line in [line for line in lines.split("VNLPAGL\n") if len(line) > 0]:
                        try:
                            keyword = keyword_extractor.run(line)
                            metadata = {"f": filename, "k": keyword, "h": header}
                            print(f"\nEmbedding1: {metadata}")
                            summarize = sentence_summarizer.run(line)
                            print(f"\nEmbedding2: {summarize}")
                            embedding = self.embedder.run(metadata)
                            embedding2 = self.embedder.run(summarize)
                            content = f"{header}: {line}"
                            print(f"\nContent: {content}")
                            self.vector_store.insert_document({"content": content, "embedding": embedding, "embedding2": embedding2, "metadata": metadata, "summarize": summarize})
                            print(f"\noooooooooooooooooooo File {file_index}/{len(files)} - Line {line_index} - Section {section_index}/{len(sections)} - {file_path} oooooooooooooooooooo")
                        except Exception as e:
                            print(f"Error: {e}")
                        line_index += 1
                    section_index += 1
                file_index += 1

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
    
    def run(self, question: str, messages: List[Message] = None) -> str:
        prompt = self.get_final_prompt(question, messages)
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        return self._clean_json_response(response.json())
    
    def _clean_json_response(self, response_data: dict) -> str:
        return response_data.get("response", "")
    

# Define the regex pattern to identify Markdown headers
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
    """
    Extracts Markdown headers and their associated content from a given text.

    Args:
        text (str): The input text containing Markdown.

    Returns:
        list of tuples: A list where each tuple contains a header and its associated content.
    """
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

def CleanText(text):
  # Remove newlines, tabs, and extra spaces
  cleaned_text = text.strip().replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ")
  cleaned_text = cleaned_text.replace("|||", "").replace("| |", "")
  cleaned_text = cleaned_text.replace(" | ", "-")
  cleaned_text = cleaned_text.replace("**", "").replace("--", "")
  cleaned_text = cleaned_text.replace("-", " ")

  return cleaned_text

def RemoveExcessiveSpacing(text):
    while "  " in text:
        text = text.replace("  ", " ")
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    while "...." in text:
        text = text.replace("....", "")
    while "----" in text:
        text = text.replace("----", "")
    return text

def RecursiveSplitSentences(document: str, limit: int = 1000):
    # Split the document into sentences
    sentences = document.split(".")
    
    # Recursively split long sentences
    paragraphs = []
    paragraph = ""
    while len(sentences) > 0:
        sentence = sentences.pop(0)
        if len(paragraph) + len(sentence) < limit:
            paragraph += f"{sentence}. "
        else:
            paragraphs.append(paragraph)
            paragraph = f"{sentence}. "

    # Add the last paragraph
    if len(paragraph) > 0:
        paragraphs.append(paragraph)

    return paragraphs
