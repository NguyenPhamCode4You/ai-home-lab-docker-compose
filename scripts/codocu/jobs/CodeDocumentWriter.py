import httpx
import requests

class CodeDocumentWriter:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and task is to write a document for a junior developer to understand the code.
        First, write a general description using the following template:
        ## General purpose
        [Describe the general purpose of the code, quickly explain what it does and the business value it provides]

        Then, separate the codes into important blocks or functions and explain what each block does using the following template
        ## [Business purpose in 10 words max]
        [code_block]
        **Explanation:**

        Each Explanation should be:
        + Clear, consise but with good details in a Well-structured bullet points.
        + Supportive information with your own knowledge is possible.
        + Easy to understand even for a junior developer.

        Important:
        - Avoid insert full credentials, like api tokens, in code blocks.

        Now, let's start with the document:
        {document}
        Your work:

        """

    def run(self, document: str) -> str:
        prompt = self.base_prompt.format(document=document)
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
    
    async def stream(self, document: str):
        prompt = self.base_prompt.format(document=document)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response