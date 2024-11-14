import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "codegemma:7b-instruct-v1.1-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class TextFormater:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in analyzing markdown documents and fixing formatting issues.

        1. If you see markdown titles, put the children items in the same line. Remove unnecessary spaces and special characters.
        Here is an example:

        Example -----------------------------------------------------
        # Introduction

        Markdown is a lightweight markup language with plain-text formatting syntax.

        Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.
        End of example.----------------------------------------------

        Output:
        Introduction: Markdown is a lightweight markup language with plain-text formatting syntax. Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.
        
        2. If you see code blocks, put the whole function in the same line. Remove unnecessary spaces and special characters.
        Example -----------------------------------------------------
        ## Example Code
        ```python
        def hello_world():
            print("Hello, world!")
        ```
        End of example.----------------------------------------------

        Output:
        Example Code: def hello_world(): print("Hello, world!")

        3. For table, write the table content line by line, without any special characters, for each value of each column.
        Example -----------------------------------------------------
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |
        End of example.----------------------------------------------

        Output:
        Product Comparison: Product: Product A, Price: $10, Rating: 4.5, Description: Affordable and high-quality. Product: Product B, Price: $20, Rating: 4.8, Description: Premium quality with extra features. Product: Product C, Price: $15, Rating: 4.2, Description: Good value for the price.
        
        Now, please extract the key sentences from the following text: 
        """

    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            ollama_instruct_url,
            json={"model": ollama_instruct_model, "prompt": self.base_prompt + self.message, "stream": False}
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