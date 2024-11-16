import requests

class CreateEmbedding:
    def __init__(self, model: str = 'nomic-embed-text:137m-v1.5-fp16', url: str = 'http://localhost:11434/api/embed'):
        self.model = model
        self.url = url
    
    def run(self, message: str) -> list:
        # Send the request to the Ollama API
        response = requests.post(
            self.url,
            json={"model": self.model, "input": str(message)}
        )
        
        # Check if the response is successful
        response_data = response.json()
        
        # Extract embeddings from the response data, assuming it's stored under a key called "embeddings"
        embeddings = response_data.get("embeddings")
        if embeddings is None:
            raise ValueError("No embeddings found in the response.")
        
        # Return the embeddings
        return embeddings[0]