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

        Important:
            - Avoid adding any extra spaces, symbols, or labels such as "Chunk 1" or "Key Sentence."
            - Use only "VNLPAGL" as the chunk separator.

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