import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "codegemma:7b-instruct-v1.1-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class TextChunker:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in analyzing markdown documents and put a break between the key sentences. Follow the guidelines below:

        1. Use "VNLPAGL" to separate between key sentences.
        2. Length Restriction: Limit the length of each key sentence to less than 200 characters.
        
        Here is an example:

        Example -----------------------------------------------------
        # Introduction
        Markdown is a lightweight markup language with plain-text formatting syntax.
        Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.

        ## Example Code
        ```python
        def hello_world():
            print("Hello, world!")
        ```
        End of example.----------------------------------------------

        Output:
        # Introduction
        Markdown is a lightweight markup language with plain-text formatting syntax.
        Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.
        VNLPAGL
        ## Example Code
        ```python
        def hello_world():
            print("Hello, world!")
        ```

        4. For table, put the column name before the value, also dont forget the Markdown Titles as Keyword!
        Here is the example of a table:

        Example -----------------------------------------------------
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |
        End of example.----------------------------------------------

        Output:
        [Product Comparison]
        Product: Product A, Price: 10, Rating: 4.5, Description: Affordable and high-quality. Product: Product B, Price: 20, Rating: 4.8, Description: Premium quality with extra features.
        VNLPAGL
        [Product Comparison] Product: Product C, Price: 15, Rating: 4.2, Description: Good value for the price.

        7. For Code block, always try to put them together as one key sentence.
        8. If Code blocks are too long, seperated rows should also contain the function name at the beginning!

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

        Output
        [Data Processing Code] 
        ```python
        def process_data(data):
            # This function processes data by cleaning and transforming it
            cleaned_data = [item.strip().lower() for item in data if isinstance(item, str)]
            ...
        ```
        VNLPAGL
        [Data Processing Code] 
        ```python
        def process_data(data):
            ...
            transformed_data = [int(item) for item in cleaned_data if item.isdigit()]
            return transformed_data
        ```

        Again, Important Notes:
        - Always use "VNLPAGL" to separate key sentences.
        - Always put the title of the markdown section in square brackets.
        - For code blocks, try to keep them as one key sentence. If they are too long, put the function name at the beginning of the next part.
        
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