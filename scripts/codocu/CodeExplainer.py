import requests

class CodeExplainer:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and you are asked to explain a code block.
        1. Explain should include the purpose of the code block and how it works.
        2. Should be clear and concise, but detailed enough to be understood by a junior developer.
        3. Total explanation should be no longer than 250 characters.
        Important: Just return the explanation, do not include any additional information, no code, no prompt.
        Explain the code block.
        Code Block:

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