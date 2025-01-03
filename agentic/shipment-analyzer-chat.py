from src.ApiCallerAssistant import ApiCallerAssistant
from src.ChartAssistant import ChartAssistant
from src.AssistantOrchestra import AssistantOrchestra
from src.DiagramAssistant import DiagramAssistant
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.models.ChatGpt import ChatGpt
from src.agents.MathplotCodeWriter import MathplotCodeWriter
from src.agents.JSONSummarizer import JSONSummarizer
from src.agents.ApiConfigWritter import ApiConfigWritter
from src.agents.QuestionForwarder import QuestionForwarder
from src.ChatBackend import create_chat_backend

from dotenv import load_dotenv
import os
load_dotenv()

api_assistant = ApiCallerAssistant(
    base_url="https://bvms-voyage-api-test.azurewebsites.net",
    llm_api_config_writter=ApiConfigWritter(
        llm_model=ChatGpt(),
    ),
    llm_json_summarizer=JSONSummarizer(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
    ),
    bearer_token=os.getenv("BVMS_API_TOKEN"),
    allowed_fields=["result", "items", "freightTotalInUsds", "freightRatePerCargoInUsds", "estimateCode", "portCalls", "portName", "vesselHireCostPerDayInUsds", "vesselName", "shipments", "commenceDate", "profitAndLost.*", "iteneraryItems", "vesselName", "cargoQuantity", "cargoType", "laycanFromDate", "laycanToDate", "ports", "portName", "reasonForVisit", "profitAndLossItems", "totalValueInUsds", "type", "shipmentName", "cargoOperationTimeInDays", "countryCode", "portName", "timeOfArrival", "timeOfDeparture"],
    api_instructions=[
        "/Shipments/Search - Method: POST - Description: Search for shipments using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3. No query in the URL."
        "/Shipments/shipmentId?shipmentId=UUID - Method: GET - Description: Get a shipment by its UUID. The UUID is a unique identifier for a shipment."
        "/Estimates/UUID - Method: GET - Description: Get the estimate by its UUID. The UUID is a unique identifier for an estimate."
    ]
)

chart_assistant = ChartAssistant(
    llm_mathplot_code_writer=MathplotCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
    )
)
diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
    )
)
shipment_question_forwarder = QuestionForwarder(
    max_context_tokens=15000,
)
shipment_question_forwarder.set_additional_instruction("""
For every question, compose these questions to the agents:
1. Ask the API Assistant to Search for insights about the shipment, including laycanFrom, laycanTo, ports of load, discharge, total freight, profit and loss items. Ask the agents to break down the profit and loss items accurately for further analysis.
2. Ask the Chart Assistant to Make a pie chart to compare the total freight and total expenses of the shipment.
3. Ask the Chart Assistant to create useful charts to display the profit and loss items.
4. Ask the Diagram Assistant to create a gantt chart to show the timeline of the shipment.
""")
shipment_analyzer = AssistantOrchestra(
    llm_question_forwarder=shipment_question_forwarder,
)
shipment_analyzer.agents = {
    "API Assistant": {"agent": api_assistant, "context_awareness": True, "description": "This agent can get information about Shipments of BVMS"},
    "Chart Assistant": {"agent": chart_assistant, "context_awareness": True, "description": "This agent can generate data charts based on a given data"},
    "Diagram Assistant": {"agent": diagram_assistant, "context_awareness": True, "description": "This agent can generate diagrams and workflows based on a given context"},
}

estimate_question_forwarder = QuestionForwarder(
    max_context_tokens=15000,
)

estimate_question_forwarder.set_additional_instruction("""
For every question, compose these questions to the agents:
1. Ask the API Assistant to Search for insights about the estimate, including laycanFrom, laycanTo, profit and loss and itenerary items. Ask the agents to break down the profit and loss items accurately and each iteneray item should have name and time of arrival and time of departure.
2. Ask the Chart Assistant to create useful charts to display the profit and loss items.
3. Ask the Diagram Assistant to create a gantt chart to show the timeline of the estimate, focusing on the itenerary items.
""")

estimate_analyzer = AssistantOrchestra(
    llm_question_forwarder=estimate_question_forwarder,
)

estimate_analyzer.agents = {
    "API Assistant": {"agent": api_assistant, "context_awareness": True, "description": "This agent can get information about Estimates of BVMS"},
    "Chart Assistant": {"agent": chart_assistant, "context_awareness": True, "description": "This agent can generate data charts based on a given data"},
    "Diagram Assistant": {"agent": diagram_assistant, "context_awareness": True, "description": "This agent can generate diagrams and workflows based on a given context"},
}

orchestra = AssistantOrchestra()
orchestra.agents = {
    "Shipment Analyzer": {"agent": shipment_analyzer, "context_awareness": True, "description": "This agent can analyze Shipments of BVMS"},
    "Estimate Analyzer": {"agent": estimate_analyzer, "context_awareness": True, "description": "This agent can analyze Estimates of BVMS"},
}
app = create_chat_backend(orchestra)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)