import httpx
import requests

class CodeExplainer:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and your main focus is helping user complete a task.
        1. First, go straight to the codes and explain how it works and why it is useful to the user task. Dont need to provide overview and summary.
        2. Explain should also mention the original code, which conform to the user task, give one explanation for a block of codes, line by line not needed.
        3. Explain should be clear and concise, but detailed enough to be understood by a junior developer.
        4. Then advise the user on how to use the code to complete the task, be consise, accurate. Dont need to give examples.
        Here is the code:
        {document}
        User: {question}
        Your work:
        
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