import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class DataPreProcessing:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert at re-formatting markdown text for further processing.
        1. For tables:
        - Remove table formating
        - Convert each table rows into lines with "comma" joined [column name]: [value]
        - Put "----------\n" at the start and end of the extracted table.
        Example:
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |

        Output:
        ----------\n
        ## Product Comparison
        Product: Product A, Price: $10, Rating: 4.5, Description: Affordable and high-quality.
        Product: Product B, Price: $20, Rating: 4.8, Description: Premium quality with extra features.
        Product: Product C, Price: $15, Rating: 4.2, Description: Good value for the price.
        ----------\n

        2. For code blocks, api urls:
        - Keep them untouched, but put in same line.
        - Put "----------\n" at the start and end of the extracted code block.
        Example:
        ```python
        def hello_world():
            print("Hello, world!")
        ```
        Output:
        ----------\n
        ```python def hello_world(): print("Hello, world!")```
        ----------\n

        3. For sentences or lines with length < 10 chars:
        - Combine them into a single line.
        - Put "----------\n" at the start and end of the extracted lines.
        Example:
        ---
        VOYAGE MANAGEMENT SYSTEM

        High Level Database Design Document

        15-Nov-2023

        Version: 1.0

        Document Control

        Document Information
        ---

        Output:
        ----------\n
        VOYAGE MANAGEMENT SYSTEM, High Level Database Design Document, 15-Nov-2023, Version: 1.0, Document Control, Document Information
        ----------\n

        4. For repeated lines or tables:
        - Remove the repeated values, make the unique values comma separated.
        - Remove numbers, special characters, formatting.
        - Put "----------\n" at the start and end of the extracted lines.

        Example:
        | Voyage Revenues      | Voyage Revenues      | Voyage Revenues      | 1.345.150      |
        |----------------------|----------------------|----------------------|----------------|
        | Freight              | Freight              | Freight              | 1.200.000      |
        | Misc. Revenue        | Misc. Revenue        | Misc. Revenue        | 150            |
        | Demurrage            | Demurrage            | Demurrage            | 26.000         |
        | Despatch             | Despatch             | Despatch             | 21.500         |

        Output:
        ----------\n
        Voyage Revenues: Freight, Misc. Revenue, Demurrage, Despatch
        ----------\n

        The rest of the text should be kept as is.
        
        Important:
        - Return only the formatted text.
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, please re-format the following text: 
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