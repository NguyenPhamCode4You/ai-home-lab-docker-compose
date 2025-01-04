from src.ApiCallerAssistant import ApiCallerAssistant
from src.DiagramAssistant import DiagramAssistant
from src.ChartAssistant import ChartAssistant
from src.AssistantOrchestra import AssistantOrchestra
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.MathplotCodeWriter import MathplotCodeWriter
from src.agents.JSONSummarizer import JSONSummarizer
from src.agents.models.ChatGpt import ChatGpt
from src.ChatBackend import create_chat_backend

from dotenv import load_dotenv
import os
load_dotenv()

api_assistant = ApiCallerAssistant(
    base_url="https://bvms-voyage-api-test.azurewebsites.net",
    bearer_token=os.getenv("BVMS_API_TOKEN"),
    api_instructions=[
        "/Estimates/UUID - Method: GET - Description: Get the estimate by its UUID. The UUID is a unique identifier for an estimate."
    ],
    allowed_fields=[
        "result", "items", "vesselName", "estimateCode",  
        "profitAndLost",  "freightValue", "miscRevenuesValue", "bunkerExpenseValue", "canalTollsValue", "cargoExpenseValue", "emissionExpenseValue", "externalCommissionValue", "internalCommissionValue", "miscExpenseValue", "portExpenseValue", "vesselHireValue",
        "iteneraryItems", "portName", "cargoQuantity", "shipmentName", "countryCode", "timeOfArrival", "timeOfDeparture", "reasonForVisit"
    ],
    llm_json_summarizer=JSONSummarizer(
        max_context_tokens=15000,
        user_instruction="""
        Nonetheless, provide insights about the following:
        - A comprehensive breakdown of profit and loss object (using bullet points)
        - A table to display the itinerary items with their respective:
            + Port names (1st column) - format: Port Name - Country Code
            + Arrival (2nd column), format: `YYYY-MM-DD` at `HH:MM`
            + Departure (3rd column), format: `YYYY-MM-DD` at `HH:MM`
            + Shipment name (4th column), format: Shipment Name - Cargo Quantity
            + Reason for visit (5th column)
        """,
    ),
)
diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
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