import requests

class ExecutionStrategy:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at validating a complex document and break it down into separated execution steps for answering a user question.
        Follow these steps to generate reasoning steps for the user question and document:
        
        1. Analyze the document and user question, determine if the user question requires reasoning steps to answer.
        2. If no reasoning steps are required, then simply return "VNLPAGL\n".
        3. If document contains reasoning steps to answer the question, create maximum 3 reasoning steps as questions, separated by "VNLPAGL\n".
        
        Here is an example of question and document that requires NO reasoning steps:
        Document:
        ## EU ETS Calculation - Factors & Rules
        The factors and rules that should be included in ETS calculation:
        ## EU ETS - Basic Calculation:
        - ETS = Total Emission * ETS Price - Derogation Factors
        - Emission At Sea = Sum of (Bunker Consumption at Sea of each Bunker Type * Emission Factor of the Bunker Type)
        - Bunker Consumption at Sea = Bunker Consumption Rate at Sea Per day * Total Sea Days
        User Question: What is the factors that is included in ETS calculation?
        Output: VNLPAGL\n

        However, this document and question requires reasoning steps:
        Document:
        ## Sedna API Endpoints
        The following are the endpoints available in Sedna API: - /api/v1/messages
        - /api/v1/messages/{message_id}
        - /api/v1/messages/{message_id}/attachments
        User Question: According to Sedna API, how to get new message id?

        Output:
        VNLPAGL\nWhat is the endpoint to get message details in Sedna API?
        VNLPAGL\nWhat is the data structure of the JSON object returned by the API?
        
        Important:
        - Return only the reasoning questions separated by "VNLPAGL\n"
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