import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class ProcessMarkdownHeader:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        Your task is to process markdown headers.

        1. Recognize the markdown headers and their levels.
        2. Put the parent header as prefix to the child header, seperated bt "/", revert to using only "#" for the header.
        3. Then, add a marker character 'VNLPAGL' before each header.

        Example:
        # Header 1
        Content 1, content 1, content 1.
        ## Header 2
        Content 2, content 2, content 2.
        ### Header 3
        Content 3, content 3, content 3.

        Output:
        VNLPAGL# Header 1
        Content 1, content 1, content 1.
        VNLPAGL# Header 1/Header 2
        Content 2, content 2, content 2.
        VNLPAGL# Header 1/Header 2/Header 3
        Content 3, content 3, content 3.

        The rest of the text should be kept as is.
        
        Important:
        - Return only the formatted result.
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