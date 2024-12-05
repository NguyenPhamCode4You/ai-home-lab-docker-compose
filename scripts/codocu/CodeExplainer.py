import httpx
import requests

class CodeExplainer:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and your main task is to explain the main business logic of a given code block.
        1. Go straight to the codes and explain how these are used to handle the user question in terms of business
        2. No need to describe code structure, general purpose or summary.
        2. Explain should also mentions the original code, which conform to a user question or business logic.
        3. Explain should be clear and concise, but detailed enough to be understood by a junior developer.
        Explain the code block below:
        {document}
        User Question: {question}
        Your Explanation:
        
        """

    def run(self, question: str, document: str):
        prompt = self.base_prompt.format(document=document, question=question)
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
    
    async def stream(self, question: str, document: str):
        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response