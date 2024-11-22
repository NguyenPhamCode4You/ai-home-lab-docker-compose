import requests

with open("./prompts/BVMS-Rag-Prompt.txt", "r", encoding="utf-8") as file:
    base_prompt_default = file.read()

class AssistantAnswer:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.embedder = None
        self.vector_store = None
        self.base_prompt = base_prompt_default

    def set_embedder(self, embedder):
        self.embedder = embedder
        return self

    def set_base_prompt(self, base_prompt: str):
        self.base_prompt = base_prompt
        return self
    
    def set_vector_store(self, vector_store):
        self.vector_store = vector_store
        return self

    def run(self, question: str) -> str:
        question_embedding = self.embedder.run(question)
        documents = self.vector_store.query_documents(query_embedding=question_embedding, match_count=32)
        titles = [f"{document['content']}".split(":")[0] for document in documents]
        unique_titles = list(set(titles))

        context = ""
        for title in unique_titles:
            context += f"# {title}:\n"
            # Filter and process documents matching the title
            docs = [
                f"\n-{document["content"].replace(title, "").replace(":", "").strip()}"
                for document in documents
                if document["content"].split(":")[0] == title
            ]
            # Join the processed docs with newline and "-" separator
            context += "".join(docs) + "\n"

        print(f"Context: {context}")

        prompt = self.base_prompt.replace("{context}", context).replace("{question}", question)
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
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