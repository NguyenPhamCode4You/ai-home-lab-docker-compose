import requests

ollama_instruct_url = "http://10.13.13.4:11434/api/generate"
ollama_instruct_model = "gemma2:9b-instruct-q8_0"

class KeywordExtraction:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        Your task is to extract important keywords from the text below.
        1. Keywords should be the main entities that text is about, or refering to
        2. Should not have more than 10 keywords per text, ordered by importance
        3. Sometime keywords can be verbs, adjectives, or adverbs

        Example:
        How to Calculate P&L Summaries (v1.0): I. Calculation Rules & Factors: Item: Voyage Revenues, Sub-Item: Freight, Calculation Rule & Factor: Freight Rate (L) + Freight Rate (F) x Quantity.

        Output:
        Calculate, P&L Summaries, Calculation Rules & Factors, Voyage Revenues, Freight, Calculation Rule, Factor, Freight Rate, Quantity

        3. For code, use the name of functions, classes, or variables as keywords.
        4. For documents, use the title, author, or main subject as keywords.
        5. For emails, use the subject, sender, or main topic as keywords.
        6. For URLs, use the domain, path, or main topic as keywords.
        7. For json objects, xml, or html, use the main keys, tags, or attributes as keywords.

        Important:
        - Return only the keywords, separated by commas.
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, please extract the keywords from the following text:
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