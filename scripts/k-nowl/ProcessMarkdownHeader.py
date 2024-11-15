import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class ProcessMarkdownHeader:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        Your task is to process markdown headers. Markdown headers are denoted by "#" symbols at the beginning of a line. 
        The number of "#" symbols indicates the level of the header. For example, "# Header 1" is a level 1 header, "## Header 2" is a level 2 header, and so on.

        Now do the following steps:
        1. Recognize the markdown headers and their levels.
        2. Put the parent header as prefix to the child header, seperated bt "/" to get a new header.
        3. Replace the original header with the new header.
        4. Then, add a marker character 'VNLPAGL' before the header.
        5. The content under the header should remain unchanged.

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