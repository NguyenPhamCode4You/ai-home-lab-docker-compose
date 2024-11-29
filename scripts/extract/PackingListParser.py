import json
import requests

class PackingListParser:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at converting the text into list of packing items.
        Each packing item have json structure of { item_name, quantity, width, height, length, weight, volume }.
        Return only the json structure, no additional information, no triple quotes, no formatting, no explanations.
        Wrap the json structure in <json> tags.
        Example output: <json>[{"item_name": "apple", "quantity": 5, "width": 2, "height": 3, "length": 4, "weight": 1, "volume": 24}]</json>
        Text: 
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
        response = response.replace("<json>", "").replace("</json>", "")
        print(f"Extracted JSON: {response}")
        try:
            return json.loads(response)
        except Exception as e:
            print(f"Failed to parse chunk {response}")
            return []