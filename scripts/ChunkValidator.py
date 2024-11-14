import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class ChunkValidator:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in analyzing markdown documents. Your task is to evaluate the usefulness of paragraphs or sentences based on the criteria below. Respond with "Yes" if useful, or "No" if not.

        Guidelines:
        When to return "No":

        1. Length & Content: The text is too short, empty, or contains random words, titles, or characters.
        2. Structure: Contains incomplete sentences or fragments that lack clear context.
        3. Symbols: Consists primarily of special characters, symbols, or placeholders.
        4. Names Only: Contains only names or attributions without additional content.
        
        When to return "Yes":
        - Substantial Content: The paragraph or sentence is descriptive, complete, and informative.
        - Code Blocks & Tables: Any text containing a code block or a table should always return "Yes," regardless of other factors.
        
        Examples of Useful and Non-Useful Information
        
        Example -----------------------------------------------------
        # Introduction
        Markdown is a lightweight markup language with plain-text formatting syntax. Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.
        End of example.----------------------------------------------

        Output:
        Yes

        Example -----------------------------------------------------
        <!-- image -->## Integration Support
        End of example.----------------------------------------------

        Output:
        No

        Example -----------------------------------------------------
        ** Important Note: ** Caculation
        End of example.----------------------------------------------

        Output:
        No

        Example -----------------------------------------------------
        # Data Processing Code
        ```python
        def process_data(data):
            # This function processes data by cleaning and transforming it
            cleaned_data = [item.strip().lower() for item in data if isinstance(item, str)]
            transformed_data = [int(item) for item in cleaned_data if item.isdigit()]
            return transformed_data
        ```
        End of example.----------------------------------------------

        Output:
        Yes

        Example -----------------------------------------------------
        | jr-f7 | attribute s| || Information | Description |
        End of example.----------------------------------------------

        Output:
        No

        5. If the paragraph just show the name of some persion, also return "No".
        Example -----------------------------------------------------
         | 01/04/2024 - @(Lexie) Trang Nguyen Ha(Unlicensed) - Messages| A| Add messages - 1.2 |
        End of example.----------------------------------------------

        Output:
        No

        ### Important Notes:
        - Respond with only 01 time of "Yes" or "No", as plain text.
        - Do not add extra explanations, comments, or additional information.

        ---

        **Text to Validate:**

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