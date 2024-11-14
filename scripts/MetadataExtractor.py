import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class MetadataExtractor:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in analyzing markdown documents and extracting key purposes that convey essential topic of discussion of the paragraph or sentences.
        When receiving the paragraph or sentences, follow the guidelines below to extract the key purposes:

        1. Split sentences: Split the paragraph or sentences into groups of related sentences.

        Then, for each group of sentences:
        2. Analyze the Purpose: Identify the main idea or purpose the sentences.
        3. Then, Output the following Format: 
          - [k]: Commas separated keywords mentioned in the paragraph or sentences.
          - [a]: Verbs or adjectives that describe properties or actions in the paragraph or sentences.
          - [s]: A brief summary of the main idea or purpose, less than 100 characters.

        4. For each group of sentences, use "VNLPAGL" to separate the groups.

        Here is an example of how to format your output:

        Example -----------------------------------------------------
        # Introduction
        Markdown is a lightweight markup language with plain-text formatting syntax. 

        ## Features
        Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.

        ## Example Code
        ```python
        def hello_world():
            print("Hello, world!")
        ```
        End of example.----------------------------------------------

        Output:
        VNLPAGL[k]: Markdown [a]: lightweight [s]: Markdown is a lightweight markup language with plain-text formatting syntax, supports headers, lists, emphasis, links, images.
        VNLPAGL[k]: python, code, hello_world, [a]: code [s]: Example code that prints "Hello, world!".

        5. For table, put the table name in the [k] section, column names in the [a] section and summarize the purpose of table in the [s] section.
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
        VNLPAGL[k]: Product Comparison [a]: Price, Rating, Description [s]: Comparing products based on price, rating, and description for Product A, Product B, and Product C.

        6. For Code block, put the function name or the main idea of the code block in the [k] section, important variables or parameters in the [a] section and summarize the purpose of the code block in the [s] section.

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
        VNLPAGL[k]: process_data, code [a]: cleaned_data, transformed_data [s]: This function processes data by cleaning and transforming it using python.

        Again, Important Notes:
        - Always use "VNLPAGL" to separate key sentences.
        - Always include [k], [a], and [s] in the output.
        - [k] should contain keywords, [a] should contain verbs or adjectives, and [s] should contain a brief summary, less than 100 characters.
        
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