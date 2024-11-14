import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class CreateEmbedding:
    def __init__(self, message: str):
        self.message = str(message)
    
    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            ollama_embeding_url,
            json={"model": ollama_embeding_model, "input": self.message}
        )
        
        # Check if the response is successful
        response_data = response.json()
        
        # Extract embeddings from the response data, assuming it's stored under a key called "embeddings"
        embeddings = response_data.get("embeddings")
        if embeddings is None:
            raise ValueError("No embeddings found in the response.")
        
        # Return the embeddings
        return embeddings[0]