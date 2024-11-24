import requests

class QuestionRewrite:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at breaking down a complex question into simpler questions for better understanding.
        Follow these steps to generate simpler questions for the user question:

        1. Analyze the user question and determine if it can be broken down into simpler questions.
        2. If the user question can be simplified, create maximum 3 simpler questions, separated by "VNLPAGL\n".
        3. If the user question is already simple, then simply return "VNLPAGL\n".

        Here is an example of a complex question that requires simplification:
        User Question: How does the EU ETS calculation work?

        Output:
        VNLPAGL\nWhat is the formula for calculating ETS?
        VNLPAGL\nWhat are the factors included in ETS calculation?
        VNLPAGL\nWhat is the purpose of ETS in the EU?

        Important:
        - Return only the simpler questions separated by "VNLPAGL\n"
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, generate simpler questions for this user question: {question} 
        """

    def run(self, question: str) -> str:
        prompt = self.base_prompt.replace("{question}", question)
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": str(prompt), "stream": False}
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