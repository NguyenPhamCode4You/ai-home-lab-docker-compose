import httpx
import requests

class CodeBlockExtractor:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are a specialized agent that can identity if a given header is related to a user question.
        Criteria for relevance:
        1. If the header contains words related to the topic of the question, then it is relevant.
        2. If main topic of question can be found in the header, then it is relevant.
        3. If the header is too generic, then it is not relevant.
        4. Otherwise, it is not relevant.
        5. If no headers are relevant, then return "No relevant information found."

        Return the list of headers that are relevant to the question, seperated by a newline character, follow this pattern:
        [Numbering]. [header1]: [explaination why this header is selected, maximum 50 words]

        Important: 
        - DO NOT modify the headers, return them as is, do not wrap them in code block.
        - DO NOT include any additional information.

        Now, let's start:
        Here are the list of headers:
        {document}
        User Question: {question}
        Your answer:

        """

        # self.base_prompt = """
        # You are an experienced software developer that can extract code block useful for answering a question.
        
        # Each code block in the document follow the pattern:
        # ## [Business purpose in 5 words max]
        # [code_block]
        # [Explaination]

        # If the header mentions words related to topic of question, then include the code block in your final answer.
        # All relevant code blocks should be combined into one single final code block, returned as is, not wrapped in a code block, just return plain text.
        
        # Important:
        # - Do not include any additional information, no explaination needed, code block should be returned as is, no wrapping in code block.
        # - If the entire document does not have any header that is relevant to the question, return "No relevant code found."
        # - Dont include the summary and keywords section of the document.

        # Document To Analyze:
        # {document}
        # Question: {question}
        # Your answer:

        # """

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