import requests

class ExecutionStrategy:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at validating whether a document contains complex reasoning steps to answer for user question.
        1. If document contains information to answer the question, simply return "VNLPAGL\n"
        2. If document contains reasoning steps to answer the question, then for each reasoning step, combine the steps with the user question to create a new question. Seperate each reasoning step by "VNLPAGL\n".
        
        Example:
        User QUestion: What is the factors that is included in ETS calculation?
        Document:
        ## EU ETS Calculation - Factors & Rules
        The factors and rules that should be included in ETS calculation:
        ## EU ETS - Basic Calculation:
        - ETS = Total Emission * ETS Price - Derogation Factors
        - Emission = Emission at Port + Emission at Sea
        - Emission At Sea = Sum of (Bunker Consumption at Sea of each Bunker Type * Emission Factor of the Bunker Type)
        - Emission At Port = Sum of (Bunker Consumption at Port of each Bunker Type * Emission Factor of the Bunker Type)
        - Bunker Consumption at Sea = Bunker Consumption Rate at Sea Per day * Total Sea Days

        Output: VNLPAGL\n

        Example:
        User Question: What is the ETS factors for one vessel traveling from Lisbon to Funchal?
        Document:
        ## EU ETS Calculation Logics
        Step 1. From the ports list determine the two consecutive pair of load or discharge ports (Can be load - discharge, load - load, discharge - load or discharge - discharge).
        Step 2. For each pair of load - discharge ports: determine the ports in between from the port list.
        Step 3. For each pair of load - discharge ports: looking at their country codes to see if they are from EU.
        Step 4. If both load - discharge ports are not from EU: then both of them and all middle ports have ETS factor = 0.

        Output:
        VNLPAGL\nWhat are the two consecutive pair of load or discharge ports?
        VNLPAGL\nFor each pair of load - discharge ports: determine the ports in between from the port list.
        VNLPAGL\nDetermine the country codes of the load - discharge ports.
        VNLPAGL\nIs each pair of load - discharge ports from EU? If Yes, then calculate the ETS factor, If No, then ETS factor = 0.
        
        Important:
        - Return only the questions and seperated by "VNLPAGL\n"
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, generate reasoning steps for the user question and document.
        Document: {document}
        User Question: {question}
        """

    def run(self, document: str, question: str) -> str:
        # Send the request to the Ollama API
        prompt = self.base_prompt.replace("{document}", document).replace("{question}", question)
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