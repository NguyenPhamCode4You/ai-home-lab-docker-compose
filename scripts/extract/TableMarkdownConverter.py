import json
import requests
from Helper import RecursiveSplitSentences

class TableMarkdownConverter:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at re-formatting markdown table and bullet points into csv format.

        1. For tables:
        - Remove all table formatting, keep only the content and column headers.
        Example:
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |

        Output:
        Product, Price, Rating, Description
        Product A, $10, 4.5, Affordable and high-quality.
        Product B, $20, 4.8, Premium quality with extra features.
        Product C, $15, 4.2, Good value for the price.

        2. For bullet points:
        - Convert bullet points to comma separated values.
        Example:
        - Product A:
            + Price: $10
            + Rating: 4.5
            + Description: Affordable and high-quality.
        - Product B:
            + Price: $20
            + Rating: 4.8
            + Description: Premium quality with extra features.
        
        Output:
        Product A, Price: $10, Rating: 4.5, Description: Affordable and high-quality.
        Product B, Price: $20, Rating: 4.8, Description: Premium quality with extra features.

        3. For other markdown content: ignore and return empty string.

        Important:
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, re-format the markdown content into csv format: 
        """

    def run(self, message: str) -> str:
        chunks = RecursiveSplitSentences(message, limit=4000, overlap=0)
        chunks = [chunk for chunk in chunks if len(chunk) > 0]
        current = 1
        total = len(chunks)
        result = ""

        for chunk in chunks:
            # Send the request to the Ollama API
            response = requests.post(
                url=self.url,
                json={"model": self.model, "prompt": self.base_prompt + str(chunk), "stream": False}
            )
        
            # Check if the response is successful
            if response.status_code != 200:
                print(f"Failed to convert chunk {current}/{total}.")
                continue
        
            # Clean and format the JSON response
            response = self._clean_json_response(response.json())
            result += response + "\n"
            current += 1

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response