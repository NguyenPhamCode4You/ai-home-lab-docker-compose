import asyncio
import json
import httpx
import requests
from typing import List, Optional

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class AssistantAnswer:
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
    
    def set_code_block_finder(self, code_block_finder):
        self.code_block_finder = code_block_finder
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
    
    async def stream_answer_from_files(self, question: str, messages: List[Message] = None):
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
            return f"**[{file_name}]({file_url})**"
        
        current_file_index = 1
        
        async with httpx.AsyncClient() as client:
            if self.file_prioritizer:
                # Extract file names from the documents
                file_names = [doc["metadata"]["f"] for doc in documents]
                yield json.dumps({"response": f"📚 Relevant files: {', '.join(file_names[:10])}...\n\n"})
                yield json.dumps({"response": f"📚 Prioritizing those files based on relevance...\n\n"})

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
                                summarize = doc["summarize"]
                                file_path = doc["content"]
                                if file_name_index < 10:
                                    yield json.dumps({"response": f"📌 Rank {file_name_index + 1}: {format_file_name(prioritized_name, file_path)}\n"})
                                break

                    # Update the original documents list
                    documents = reordered_documents

            yield json.dumps({"response": f"\n\n## 🤖 Start learning... \n\n\n"})
            context = ""
            for index, document in enumerate(documents):
                if current_file_index > self.match_count:
                    break
                if len(context) > self.max_context_tokens_length:
                    break
                try:
                    file_path = document["content"]
                    file_name = document["metadata"]["f"]
                    file_name = f"__{file_name}__"
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        relevant_contents = []
                        if self.code_block_finder and len(content) > 1000:
                            yield json.dumps({"response": f"\n🕑 Mem: {len(context)}/{self.max_context_tokens_length} tokens - Iterations: {current_file_index}.{self.match_count}.L{index + 1}. Reading file: {file_name} 👀 \n\n"})

                            code_blocks = await asyncio.to_thread(self.code_block_finder.run, question, content)
                            code_blocks = [code_block.strip() for code_block in code_blocks.split("VNLPAGL") if len(code_block) > 20]

                            for code_block_index, code_block in enumerate(code_blocks):
                                if "No relevant code" in code_block:
                                    yield json.dumps({"response": f"\n⛔️ {file_name} - Part: {code_block_index + 1}/{len(code_blocks)}. No relevant context found.\n"})
                                else:
                                    relevant_contents.append(code_block)
                                    yield json.dumps({"response": f"\n✅ {file_name} - Part: {code_block_index + 1}/{len(code_blocks)}. Found relevant {len(code_block)} context tokens \n\n"})
                                    if "```" not in code_block:
                                        code_block = f"\n\n```csharp\n{code_block}\n```\n\n"
                                    yield json.dumps({"response": f"\n{code_block}\n"})
                                    print(f"ooooooooooooooooooooooooo relevant ooooooooooooooooooooooooo")
                        else:
                            relevant_contents.append(content)
                            yield json.dumps({"response": f"\n✅ Read all {len(content)} codes in file {file_name}\n\n"})
                            if "```" not in content:
                                content = f"\n```csharp\n{content}\n```\n\n"
                            yield json.dumps({"response": f"\n{content}\n"})
                            print(f"Code Block: {content}")
                            print(f"ooooooooooooooooooooooooo ADDED RAW ooooooooooooooooooooooooo")

                        if len(relevant_contents) == 0:
                            continue
                        
                        context_new_part = f"\n{file_name}:\n{'\n'.join(relevant_contents)}"
                        print(f"{context_new_part}")
                        max_token_length_per_file = 4000
                        if len(context_new_part) > max_token_length_per_file:
                            context_new_part = context_new_part[:max_token_length_per_file]
                        context += context_new_part
                        current_file_index += 1

                except Exception as e:
                    yield json.dumps({"response": f"\n⛔️ Error reading file: {file_name}, {str(e)}"})
                    continue

            context = context[:self.max_context_tokens_length]

            histories = ""
            if messages and len(messages) > 0:
                histories = "\n".join([f"{message.role}: {message.content}" for message in messages or []])
                histories = histories[-self.max_history_tokens_length:]

            prompt = (
                self.base_prompt
                .replace("{context}", context)
                .replace("{question}", question)
                .replace("{histories}", histories)
            )
            
            yield json.dumps({"response": f"\n ✨ Total relevant tokens: {len(context)}/{self.max_context_tokens_length} 👀 \n\n"})
            yield json.dumps({"response": "\n## 🎯 Generating final response...\n\n"})
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
    
    async def stream(self, question: str, messages: List[Message] = None):
        prompt = self.get_final_prompt(question, messages)
        
        async with httpx.AsyncClient() as client:
        # Send streaming request to Ollama
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
    
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
