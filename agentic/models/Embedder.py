import os
from dotenv import load_dotenv
import requests
load_dotenv()

class Embedder:
    def __init__(self, url: str = None, model: str = None):
        self.name = "Embedder"
        self.url = url or os.getenv("OLLAMA_URL") or None
        self.model = model or os.getenv("OLLAMA_EMBEDDING_MODEL") or None

    def run(self, message: str) -> list:
        response = requests.post(
            f"{self.url}/api/embed",
            json={"model": self.model, "input": str(message)}
        )
        response_data = response.json()
        embeddings = response_data.get("embeddings")
        if embeddings is None:
            raise ValueError("No embeddings found in the response.")
        return embeddings[0]

# Example usage
if __name__ == "__main__":
    import asyncio
    async def main():
        model = Embedder()
        print(model.run("Who is the president of the United States?"))
    asyncio.run(main())