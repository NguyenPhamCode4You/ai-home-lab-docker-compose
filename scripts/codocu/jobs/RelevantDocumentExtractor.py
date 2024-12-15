import httpx
import requests

class RelevantDocumentExtractor:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        Given this CONVERSATION:
        {question}

        First, anaylyze the topics and keywords of the conversation to understand the context.
        Then, extract the headers from the following paragraphs that are relevant to the topics and keywords of the conversation:
        {document}

        **If user enquired for reading the entire file, then all the headers are relevant.**

        Return the headers of the relevant paragraphs in the following format:
        - [Relevant header]: [Explanation why it is relevant to the topics and keywords of the conversation, in 65 words max]
        
        **Since tokens is limited, DO NOT explain in details! 65 words max for each headers selected.**
        
        Important:
        - DO NOT return headers in the CONVERSATION unless it is mentioned in the paragraphs. DO NOT make up new headers.
        - DO NOT modified the headers. Return them as they are since they are being used to search for the relevant paragraphs later.
        - IF NO relevant information can be found, just return "- No relevant headers found."

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