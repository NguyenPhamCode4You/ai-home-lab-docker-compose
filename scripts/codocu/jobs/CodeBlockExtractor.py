import httpx
import requests

class CodeBlockExtractor:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an experienced software developer that can skim through a code document and identify the relevant code blocks based on a given question.
        Important: 
        - Relevant code blocks usually have the markdown header that is highly related to the question or topic of the question.
        - All relevant code blocks should be combined into one single final code block, returned as is, not wrapped in a code block, just plain text.
        - Do not include any additional information, no explaination needed.
        - If the entire file does not have any relevant code blocks, return "No relevant code found."

        Code To Analyze:
        {document}
        Question: {question}
        Your answer:

        """

    async def stream(self, question: str, document: str):
        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def run(self, question: str, document: str) -> str:
        prompt = self.base_prompt.format(document=document, question=question)
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": str(prompt), "stream": False}
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