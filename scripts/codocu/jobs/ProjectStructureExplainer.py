import requests

class ProjectStructureExplainer:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and you are asked to explain a folder structure.
        Follow the following template:
        1. Explain should outline the folder structure in a clear and concise manner, can be in diagram or text format.
        2. Explain should explain the source pattern and architecture of the project.
        3. Explain should explain the purpose of each folder and the relationship between them.
        
        Now, let's start:
        {document}
        Your answer:
        """

    def run(self, message: str) -> str:
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": self.base_prompt + str(message), "stream": False}
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