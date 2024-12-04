import requests

class RelevantCodeBlockFinder:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an experienced software developer and you are asked to extract code blocks that contains important business logics.
        Important: 
        1. Dont inlcude library imports or setup code, only include code that contains business logic.
        2. Each code block should contains at least 3 lines of code, but no more than 10 lines, total length from 300 to 1000 characters.
        3. Extracted code blocks should be separated by "VNLPAGL\n".
        4. Do not include any additional information, no explaination, just return the code blocks as plain text.

        Now extract business related code blocks from the below document.
        Remeber to return code blocks as is, no modification, no explaination, separated by "VNLPAGL\n".
        {document}
        """

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

        # self.base_prompt = """
        # You are an experienced software developer that can analyze and identity relevant code blocks that can help answer the question.
        # Important: 
        # - Relevant code block usually contains the answer to the question, or having keyword mentioned in the question.
        # - Code block should be returned as is, each has no more than 10 lines of code, wrapped in a code block of the programming language.
        # - Do not include any additional information, no explaination needed.
        # - If the entire code file is completely irrelevant, return "No relevant code found."
        # - ALWAYS Seperate code blocks using "VNLPAGL\n"

        # Code To Analyze:
        # {document}
        # Question: {question}
        # Now return the relevant code blocks.
        # """

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