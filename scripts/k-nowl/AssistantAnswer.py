import requests
from typing import List, Optional

# Load default base prompt
with open("./prompts/BVMS-Rag-Prompt.txt", "r", encoding="utf-8") as file:
    base_prompt_default = file.read()

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
        self.base_prompt = base_prompt_default
        self.match_count = 100
        self.max_context_tokens_length = 5500   # 5500 is the best length for the context tokens, for typescript & PL questions
        self.max_history_tokens_length = 500    # 6000 is the maximum length, thus 6000 - 5500 = 500 for the history tokens

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

    def set_evaluator(self, evaluator):
        self.evaluator = evaluator
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

    # Run the assistant to answer the question
    def run(self, question: str, messages: List[Message] = None) -> str:
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
        
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        
        return self._clean_json_response(response.json())

    # Clean the API response
    def _clean_json_response(self, response_data: dict) -> str:
        return response_data.get("response", "")
