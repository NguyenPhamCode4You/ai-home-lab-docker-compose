import requests

ollama_instruct_url = "http://10.13.13.4:11434/api/generate"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"

class SentenceSummarizer:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        Your task is to produce 01 summarize to the text below.

        Sumarize: 
        - Should be concise, clear, and informative, less than 100 characters.
        - Should mention the main topic, keyword of the text.
        - Sumarize should be a complete sentence, shorter than the original text.

        Important:
        - Return only the formatted text.
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, please summarize the following text: 
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