import httpx
import requests

class CodeBlockExtractor:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        Given this CONVERSATION:
        ----------------------
        {question}
        ----------------------

        Your task is to extract headers of pagraphs that are relevance to the above conversation.
        Here is the DOCUMENT to extract headers from:
        ----------------------
        {document}
        ----------------------

        Return the selected relevant headers in the following format, seperated by new lines.
        - [Relevant header]: [Explanation why it is relevant, in 50 words max]

        DO return ONLY headers in the given document.
        DO NOT return ANY headers in the CONVERSATION. DO NOT make up new headers. 
        IF NO relevant headers found in the document, just return "- No relevant headers found."

        """

    async def stream(self, question: str, document: str):
        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
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