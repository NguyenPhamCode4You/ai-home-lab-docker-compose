import httpx
import requests

class CodeSummarizer:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and you are asked to explain a code block.
        1. Explain should include the purpose of the code block and how it works, mention any important details.
        2. Should be clear and concise, but detailed enough to be understood by a junior developer.
        3. Total explanation should be no longer than 200 characters.
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
    
    async def stream(self, message: str):
        prompt = self.base_prompt + str(message)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response