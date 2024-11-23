import requests

class SentenceSummarizer:
    def __init__(self, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.base_prompt = """
        Your task is to summarize the given markdown text with 1-3 sentences.

        Sumarize: 
        - Should be concise, clear, and informative, less than 300 words.
        - Should mention the main header of the text, with topic and subtopic if available.
        - Sumarize should contain complete sentences, and should be shorter than the original text.

        Example:
        ## Bunker Planning - Formular:
        - Bunker ROB at Arrival = Bunker ROB at Departure - Bunker Consumption at Sea
        - Bunker Consumption at Sea = Bunker Consumption Rate at Sea Per day * Total Sea Days
        - Total Sea Days = Distance : Speed + Extra Sea Days
        - Bunker ROB at Departure = Bunker ROB at Arrival - Bunker Consumption at Port + Bunker Received
        - Bunker Consumption at Port = Bunker Consumption (Idle) + Bunker Consumption (Working) + Bunker Consumption (Intra Port)

        Sumarize: This text describe the bunker planning formular for a ship. It includes the calculation for Bunker ROB at Arrival, Bunker Consumption at Sea, Total Sea Days, Bunker ROB at Departure, and Bunker Consumption at Port.

        Important:
        - Return only the formatted summarize text.
        - Do not include the base prompt in the response.
        - Do not include the input text in the response.
        - Do not include any additional information.

        Now, please summarize the following text: 
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