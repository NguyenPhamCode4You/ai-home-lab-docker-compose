import requests

class SentenceSummarizer:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
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

        Sumarize: Formular for bunker planning. It includes the calculation for Bunker ROB at Arrival, Bunker Consumption at Sea, Total Sea Days, Bunker ROB at Departure, and Bunker Consumption at Port.

        Example:
        ## Event Stream API End Point
        ```
        Get basic event metadata $atts = $data['attributes']; $time = $atts['time']; $eventType = $atts['eventType']; //Only deal with incoming messages using the below //if ($eventType <> 'event. message. received') continue; //Get the message subject $msg\_id = $data['relationships']['message']['data']['id']; $msg = $this->get\_message($msg\_id); $subject = $msg['data']['attributes']['subject']; echo "$time $eventType $id $subject "; } $last\_id = $id; $url = $r['links']['next']; sleep($loop\_wait); } while (true); }
        ``` 

        Sumarize: Code example of Event Stream API End Point. It includes the code snippet for getting basic event metadata and the message subject.

        Example:
        ## Vessels Information
        1. Vessel Type: 14K-800A, Purpose: General Cargo, Dead weight (tons): 14360, Build year: 2010, Hire cost (USD/day): 12000
        2. Vessel Type: 24K-200A, Purpose: Multipurpose Tweendecker, Dead weight (tons): 24964, Build year: 2012, Hire cost (USD/day): 12000

        Sumarize: Vessels Information including details of two vessels with Vessel Type, Purpose, Dead weight, Build year, and Hire cost.

        Example:
        ## Logics for calculate ETS factor
        1. From the ports list, determining the two consecutive loading/discharging ports
        2. For each pair of load/discharge port: determine the middle ports
        3. For each pair of load/discharge port: looking at their country codes to see if they are from EU
        4. If both are not from EU: then both of them and all middle ports have factor = 0

        Sumarize: Logical steps for calculating the ETS factor. Steps include determining the consecutive loading/discharging ports, middle ports, and country codes to see if they are from EU.

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