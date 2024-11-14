import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "codegemma:7b-instruct-v1.1-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class TextSpliter:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert in analyzing and spliting paragraphs into meaningful chunks. Follow the guidelines below to split the text into chunks:

        1. Splited chunk should not be longer than 250 charracters each.
        2. Each chunk should contains complete sentences (Sentences should be split at the end of a sentence, not in the middle).
        3. Always use "VNLPAGL" as the separator between chunks.
        4. If paragraph is too short, empty, or contains random words, titles, or characters, do not split it.
        5. If paragraph too long, split it into multiple chunks, however, each child chunk should have the title of the parent paragraph at the beginning.

        Example -----------------------------------------------------
        Purpose: The purpose of the database in BVMS is to store and manage all relevant data related to cargo overview & voyage estimation, voyage management, voyage accounting and master data. The database serves as a central repository for storing and retrieving voyage-related information and facilitating efficient order processing.
        Scope: The database encompasses the following key functionalities: 
        - Cargo Overview & Voyage Estimation: storing and managing cargo, quote, estimation, shipment , fleet…
        - Voyage Management: storing and managing vessel scheduling, voyage operation..
        - Voyage Accounting: storing and managing invoice, payment, statement...
        - Master data: storing and managing user roles & permission, port list, vessel information...
        End of example.----------------------------------------------

        Output:
        Purpose: The purpose of the database in BVMS is to store and manage all relevant data related to cargo overview & voyage estimation, voyage management, voyage accounting and master data. 
        VNLPAGL
        Purpose: The database serves as a central repository for storing and retrieving voyage-related information and facilitating efficient order processing. 
        VNLPAGL
        Scope: The database encompasses the following key functionalities: - Cargo Overview & Voyage Estimation: storing and managing cargo, quote, estimation, shipment , fleet… 
        VNLPAGL
        Scope: - Voyage Management: storing and managing vessel scheduling, voyage operation.. - Voyage Accounting: storing and managing invoice, payment, statement... 
        VNLPAGL
        Scope: - Master data: storing and managing user roles & permission, port list, vessel information...

        Important Note:
        - Always use "VNLPAGL" as the separator between chunks, not any other special characters.
        - Dont ever use Chunk 1, Chunk 2, Key Sentences or any other special characters to separate the chunks. Only use "VNLPAGL".
        - Dont add any extra spaces or special characters to any of the chunks.

        Now, please split the following text into meaningful chunks: 
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