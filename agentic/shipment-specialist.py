from src.ApiCallerAssistant import ApiCallerAssistant
from src.ChartAssistant import ChartAssistant
from src.AssistantOrchestra import AssistantOrchestra
from src.DiagramAssistant import DiagramAssistant
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.models.ChatGpt import ChatGpt
from src.agents.MathplotCodeWriter import MathplotCodeWriter
from src.agents.JSONSummarizer import JSONSummarizer
from src.ChatBackend import create_chat_backend

from dotenv import load_dotenv
import os
load_dotenv()

api_assistant = ApiCallerAssistant(
    base_url="https://bvms-voyage-api-test.azurewebsites.net",
    bearer_token=os.getenv("BVMS_API_TOKEN"),
    api_instructions=[
        "/Shipments/Search - Method: POST - Description: Search for shipments using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3. No query in the URL."
        "/Shipments/shipmentId?shipmentId=UUID - Method: GET - Description: Get a shipment by its UUID. The UUID is a unique identifier for a shipment."
        "/Estimates/UUID - Method: GET - Description: Get the estimate by its UUID. The UUID is a unique identifier for an estimate."
    ],
    allowed_fields=["result", "items", "freightTotalInUsds", "freightRatePerCargoInUsds", "estimateCode", "portCalls", "portName", "vesselHireCostPerDayInUsds", "vesselName", "shipments", "commenceDate", "profitAndLost.*", "iteneraryItems", "vesselName", "cargoQuantity", "cargoType", "laycanFromDate", "laycanToDate", "ports", "portName", "reasonForVisit", "profitAndLossItems", "totalValueInUsds", "type", "shipmentName", "cargoOperationTimeInDays", "countryCode", "portName", "timeOfArrival", "timeOfDeparture"],
    llm_json_summarizer=JSONSummarizer(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
        user_instruction="""
        Provide insights about the following:
        - The total freight of all shipments in the estimate
        - A comprehensive breakdown of profit and loss object
        - A list of itinerary items with their 
            + Port names
            + Times of arrival
            + Times of departure
            + Shipment name 
            + Reason for visit
        """,
    ),
)
diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
        user_instruction="""
        Example of a good timeline diagram:
        ```mermaid
        gantt
            title Timeline
            dateFormat  YYYY-MM-DD
            section Hamburg
            Arrival  :a1, 2024-11-29, 0d
            Departure: d1, 2024-12-02, 0d
            section Lisbon
            Arrival  :a2, 2024-12-07, 0d
            Departure: d2, 2024-12-08, 0d
        ```
        """,
    ),
)
chart_assistant = ChartAssistant(
    llm_mathplot_code_writer=MathplotCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
    ),
)
estimate_analyzer = AssistantOrchestra(
    agents={
        "API Assistant": {"agent": api_assistant, "description": "This agent can get information about Estimates of BVMS", "context_awareness": True},
        "Chart Assistant": {"agent": chart_assistant, "description": "This agent can generate data charts based on a given data", "context_awareness": True},
        "Diagram Assistant": {"agent": diagram_assistant, "description": "This agent can generate diagrams and workflows based on a given context", "context_awareness": True},
    }
)
app = create_chat_backend(estimate_analyzer)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)