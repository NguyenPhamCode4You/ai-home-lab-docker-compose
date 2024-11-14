import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class TextSpliter:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in segmenting text into concise, meaningful chunks. Follow these guidelines to split the provided text:

        1. Chunk Length: Each chunk should be no longer than 250 characters.
        2. Sentence Integrity: Split only at sentence boundaries, ensuring each chunk ends with a complete sentence.
        3. Separator: Use "VNLPAGL" exclusively to separate each chunk.
        4. Exceptions:
            - If the paragraph is too short, empty, or contains only random words, titles, or isolated characters, do not split it.
            - For longer paragraphs, split into multiple chunks, with each chunk starting with the title of the paragraph where applicable.
        5. Consistency:
            - Avoid adding any extra spaces, symbols, or labels such as "Chunk 1" or "Key Sentence."
            - Use only "VNLPAGL" as the chunk separator.
        
        Example Input: Purpose: The purpose of the database in BVMS is to store and manage all relevant data related to cargo overview & voyage estimation, voyage management, voyage accounting, and master data. The database serves as a central repository for storing and retrieving voyage-related information and facilitating efficient order processing.
        
        Example Output:
        VNLPAGL Purpose: The purpose of the database in BVMS is to store and manage all relevant data related to cargo overview & voyage estimation, voyage management, voyage accounting, and master data.
        VNLPAGL Purpose: The database serves as a central repository for storing and retrieving voyage-related information and facilitating efficient order processing.

        6. If you encounter code blocks or other structured content, keep them together in a single chunk.
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
        VNLPAGL Data Processing Code: def process_data(data): cleaned_data = [item.strip().lower() for item in data if isinstance(item, str)] transformed_data = [int(item) for item in cleaned_data if item.isdigit()] return transformed_data.
        
        7. If you encounter a table, split the content line by line:
            7.1. Structure: Write each value of each column on a new line.
            7.2. Format: Include the column name before each entry, with no special characters, punctuation, or separators. Use the following order:
                - Column Name: First, write the name of each column followed by the entry for that cell.
            7.3. New Entries: For each row, start with the first column's name and continue listing values until all columns are completed, moving to the next row without extra line breaks.
            7.4. Examples and Special Cases:
                - Do not include dividers, symbols, or other characters like "|", "---", or bullet points.
        
        Example -----------------------------------------------------
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |
        End of example.----------------------------------------------

        Output:
        VNLPAGL Product Comparison: Product: Product A, Price: $10, Rating: 4.5, Description: Affordable and high-quality.
        VNLPAGL Product Comparison: Product: Product B, Price: $20, Rating: 4.8, Description: Premium quality with extra features.
        VNLPAGL Product Comparison: Product: Product C, Price: $15, Rating: 4.2, Description: Good value for the price.

        Important:
            - Avoid adding any extra spaces, symbols, or labels such as "Chunk 1" or "Key Sentence."
            - Use only "VNLPAGL" as the chunk separator.
            - Only return the text content without any additional explanations or comments.

        Now, apply these guidelines to split the following text into chunks: 
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