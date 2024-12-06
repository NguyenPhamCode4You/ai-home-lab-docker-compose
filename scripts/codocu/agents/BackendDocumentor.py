import asyncio
import json
import httpx
import requests
from typing import List, Optional

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class BackendDocumentor:
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

    def set_base_prompt(self, base_prompt: str):
        self.base_prompt = base_prompt
        return self

    def set_vector_store(self, vector_store):
        self.vector_store = vector_store
        return self
    
    def set_code_block_extractor(self, code_block_extractor):
        self.code_block_extractor = code_block_extractor
        return self
    
    def set_file_prioritizer(self, file_prioritizer):
        self.file_prioritizer = file_prioritizer
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
            print(f"""Title: {section["title"]}, Counts: {section["counts"]}""")
            context += f"""\n# {section["title"]}:\n{section['context']}"""
        return context
    
    async def stream(self, question: str, messages: List[Message] = None):
        if not self.embedder or not self.vector_store:
            raise ValueError("Embedder and vector store must be set before retrieving documents.")
        
        question_embedding = self.embedder.run(question)
        documents = self.vector_store.query_documents(query_embedding=question_embedding, match_count=20)
        if len(documents) == 0:
            yield json.dumps({"error": "No files found or smart file picker not set."})
            return
        
        import urllib.parse

        def format_file_name(file_name: str, path: str) -> str:
            # Strip any leading/trailing spaces from file_name and path
            file_name = file_name.strip()
            path = path.strip()

            # Replace backslashes with forward slashes to make it URL-compatible
            file_url = f"file:///{path.replace('\\', '/')}"

            # Encode the URL to handle any special characters
            file_url = urllib.parse.quote(file_url, safe=':/')

            # Return the correctly formatted Markdown link
            return f"[{file_name}]({file_url})"
        
        def RecursiveSplitCodeLines(document: str, limit: int = 4000):
            # Split the document into sentences
            lines = document.split("\n")
            
            # Recursively split long sentences
            paragraphs = []
            paragraph = ""
            while len(lines) > 0:
                line = lines.pop(0)
                if len(paragraph) + len(line) < limit:
                    paragraph += f"{line}\n"
                else:
                    paragraphs.append(paragraph)
                    paragraph = f"{line}\n"

            # Add the last paragraph
            if len(paragraph) > 0:
                paragraphs.append(paragraph)

            return paragraphs
        
        current_file_index = 1
        
        async with httpx.AsyncClient() as client:
            yield json.dumps({"response": f"📚 Ranking {len(documents)} documents basing on relevance level ...\n\n"})

            # Use file_prioritizer to prioritize files
            documents_to_analyze = [f"{doc["metadata"]["f"]}: {doc["summarize"][:200]}" for doc in documents]
            prioritized_file_names = await asyncio.to_thread(self.file_prioritizer.run, question, '\n'.join(documents_to_analyze))
            prioritized_file_names = [
                name for name in prioritized_file_names.split("\n") if name.strip()
            ]

            # Reorder documents based on the prioritized list
            if len(prioritized_file_names) > 0:
                reordered_documents = []
                for file_name_index, prioritized_name in enumerate(prioritized_file_names):
                    for doc in documents:
                        if doc["metadata"]["f"] in prioritized_name:
                            reordered_documents.append(doc)
                            file_path = doc["content"]
                            if file_name_index < 10:
                                yield json.dumps({"response": f"📌 Rank {file_name_index + 1}: {format_file_name(prioritized_name, file_path)}\n"})
                            break

                # Update the original documents list
                documents = reordered_documents

            yield json.dumps({"response": f"\n\n### 🤖 Start the learning process... \n\n\n"})
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
                summarize = document["summarize"]
                # yield json.dumps({"response": f"\n🕑 **Mem**: {len(knowledge_context)}/{self.max_context_tokens_length} tokens - Iterations: {current_file_index}.{self.match_count}.L{index + 1}. Reading file: {file_name} 👀 \n\n"})
                yield json.dumps({"response": f"\n✏️ Start Reading file: {file_name} 👀 \n\n"})
                await asyncio.sleep(2)
                try:
                    # yield json.dumps({"response": f"\n\n**Summary**: {summarize}\n\n"})
                    await asyncio.sleep(len(summarize) / 200)
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                        if len(content) == 0 or len(content) > 20000:
                            continue

                        chunks = [content]
                        if len(content) > 6000:
                            chunks = RecursiveSplitCodeLines(content, 5000)

                        for chunk_index, content in enumerate(chunks):
                            
                            yield json.dumps({"response": f"\n🔍 Analyzing Chunk: {chunk_index + 1}/{len(chunks)} of {file_name} for relevant codes 👀 - **Mem**: {len(knowledge_context)}/{self.max_context_tokens_length} tokens ... \n\n"} )
                            await asyncio.sleep(2)
                            code_blocks_string = "\n\n```csharp\n"
                            async for code_block in self.code_block_extractor.stream(question, content):
                                try:
                                    code_blocks_string += json.loads(code_block)["response"]
                                    yield code_block
                                except Exception as e:
                                    yield ""
                                    continue

                            code_blocks_string += "\n```\n\n"

                            if "No relevant code" in code_blocks_string:
                                continue

                            knowledge_context += f"\n{file_name}:\n{code_blocks_string}"
                            await asyncio.sleep(2)

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
            print(f"knowledge_context: {knowledge_context}\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>") 
            await asyncio.sleep(2)
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

        print(f"Prompt: {prompt}")

        return prompt
    
    # Clean the API response
    def _clean_json_response(self, response_data: dict) -> str:
        return response_data.get("response", "")
