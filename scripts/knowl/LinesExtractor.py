import requests

class LinesExtractor:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        Your task is to extract important lines of text from the given paragraph. Seperate each line by "VNLPAGL\n".

        1. Sentences in one line should be related to each other.
        2. Each line should not exceed 250 characters.
        3. Exception for code blocks, api urls, json object, xml, put them as is, in one line.

        4. Sometimes bullet points or numbered lists are also included in oneline, seperate them by "VNLPAGL\n".
        Example:
        - This is a bullet point. - This is another bullet point. - This is the last bullet point.

        Output:
        VNLPAGL\nThis is a bullet point.
        VNLPAGL\nThis is another bullet point.
        VNLPAGL\nThis is the last bullet point.

        Important:
        - Return only the formatted text.
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, please extract the important lines from the following paragraph: 
        """

    def run(self, message: str) -> str:
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": self.base_prompt + str(message), "stream": False}
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