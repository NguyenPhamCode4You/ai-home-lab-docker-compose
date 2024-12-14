import httpx
import requests

class FilePrioritizer:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        You are an expert at analyzing a list of files and their description and re-ordering them based on their important to a given question.
        Important:
        - File that have name contains the exact keywords mentioned in the question should be most important.
        - File that have description have keywords mentioned in the question to the question should also be important.
        - File that have description contains terms related to the question should be lesser important.
        - Return only file names without any modification, as plain text, seperated by a newline character, dont wrap the file names in code block.
        - Do not include any additional information, no explaination needed, do not wrap the file names in code block.

        Example:
        Files:
        EstimateShipmentPriceBasic.py: This code contains the basic logic to estimate the price of a shipment.
        EstimateShipmentPriceAdvanced.py: This code contains the advanced logic to estimate the price of a shipment.
        EstimateShipmentPrice.py: This code contains the fundamental logic to estimate the price of a shipment.
        EstimateCostOfTravelOfShipment.py: This code contains the logic to estimate the cost of travel of a shipment.
        Question: How to estimate the cost of a shipment?

        Result:
        EstimateShipmentPrice.py
        EstimateShipmentPriceBasic.py
        EstimateShipmentPriceAdvanced.py
        EstimateCostOfTravelOfShipment.py

        Most important: always return back the full list of files with the most important file at the top and the least important at the bottom.

        Now for this list of Files:
        {document}
        Question: {question}
        Return the list of files in the most relevant order.
        """

    async def stream(self, question: str, document: str):
        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

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