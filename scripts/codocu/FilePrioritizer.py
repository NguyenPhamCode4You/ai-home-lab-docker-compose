import requests

class FilePrioritizer:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at analyzing a list of files and their description and re-ordering them based on their important to a given question.
        Important:
        - File that have the exact name or keywords mentioned in the question should be most important, and the shorter the file name, the more important it is.
        - File that have name similar to the keywords mentioned in the question should be less important.
        - File that have name contains terms related to the question should be lesser important.
        - Do not include any additional information, no explaination needed, do not wrap the file names in code block.
        - File names should be returned as is, as plain text, seperated by a newline character.

        Example:
        Files:
        EstimateShipmentPriceBasic.py
        EstimateShipmentPriceAdvanced.py
        EstimateShipmentPrice.py
        EstimateCostOfTravelOfShipment.py
        Question: How to estimate the cost of a shipment?

        Result:
        EstimateShipmentPrice.py
        EstimateShipmentPriceBasic.py
        EstimateShipmentPriceAdvanced.py
        EstimateCostOfTravelOfShipment.py


        Now for this list of Files:
        {document}
        Question: {question}
        Return the list of files in the most relevant order.
        """

    def run(self, question: str, document: str) -> str:
        prompt = self.base_prompt.format(document=document, question=question)
        # Send the request to the Ollama API
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