import httpx
import requests

class RelevantCodeBlockFinder:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        # self.base_prompt = """
        # You are an experienced software developer and you are asked to extract the main code block from a given code.
        # 1. Main code block should not inlcude library imports or initialization code.
        # 2. Main code block should includes lines of codes containing main logic of the entire file or the important business logics.
        # 3. Main block should contains at least 10 lines of code, but should not exceed 1500 characters.
        # Important: 
        # - Do not explain code, no formatting, no wrapping, just return code as is.
        # Now extract the main code block from the this code file:
        # {document}
        # """

        # self.base_prompt = """
        # You are an experienced software developer that can analyze and identity most important code lines from a given code file.
        # Important: 
        # - Important code lines usually holds the key logic or the main functionality of the entire code file, or having important business logic.
        # - Important code lines need to be between 3 to 10 lines of code.
        # - Code should be returned as is, wrapped in a code block of the programming language.
        # - Do not include any additional information, no explaination needed.
        # - If the entire code file is completely irrelevant or unimportant, return "No relevant code found."
        # - ALWAYS Seperate code lines using "VNLPAGL\n"

        # Code To Analyze:
        # {document}
        # Now return the most important code lines.
        # """

        # self.base_prompt = """
        # You are an experienced software developer that can analyze and identity most important code blocks from a given code file.
        # Important: 
        # - Important code block usually holds the key logic or the main functionality of the entire code file, or having important business logic.
        # - Code block should be returned as is, each has no more than 10 lines of code, wrapped in a code block of the programming language.
        # - Do not include any additional information, no explaination needed.
        # - If the entire code file is completely irrelevant or unimportant, return "No relevant code found."
        # - ALWAYS Seperate code blocks using "VNLPAGL\n"

        # Code To Analyze:
        # {document}
        # Now return the most important code blocks.
        # """

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