import requests

class CodeBlockExtractor:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and you are asked to extract code blocks from a document.
        1. Extracted code blocks should be separated by "VNLPAGL\n"
        2. Each code block should contains at least 3 lines of code, but no more than 5 lines.
        3. Code lines should be related to each other, total length of code block should not exceed 500 characters.
        Important: Just return code blocks seperated by "VNLPAGL\n", do not include any additional information, no explaination, no prompt.
        Extract the code blocks from the document.
        Document:

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