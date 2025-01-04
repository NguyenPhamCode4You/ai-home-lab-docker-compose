from src.ApiCallerAssistant import ApiCallerAssistant
from src.DiagramAssistant import DiagramAssistant
from src.ChartAssistant import ChartAssistant
from src.AssistantOrchestra import AssistantOrchestra
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.MathplotCodeWriter import MathplotCodeWriter
from src.agents.JSONSummarizer import JSONSummarizer
from src.agents.models.ChatGpt import ChatGpt
from src.ChatBackend import create_chat_backend
from src.agents.models.Gemini import Gemini

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
        "profitAndLost",  "freightValue", "totalProfitValue", "miscRevenuesValue", "bunkerExpenseValue", "canalTollsValue", "cargoExpenseValue", "emissionExpenseValue", "externalCommissionValue", "internalCommissionValue", "miscExpenseValue", "portExpenseValue", "vesselHireValue",
        "iteneraryItems", "portName", "totalTimeAtPortInDays", "cargoQuantity", "shipmentName", "timeOfArrival", "timeOfDeparture", "reasonForVisit"
    ],
    llm_json_summarizer=JSONSummarizer(
        max_context_tokens=15000,
        user_instruction="""
        Nonetheless, do the following:
        1. Start with [Estimate code - Vessel name] as header
        2. Bullet point of Total freight (freightValue) and Total profit (totalProfitValue)
        3. Next, display the itenerary items in a table format:
            + Column Port name, Value = portName
            + Column Arrival Time, Value = timeOfArrival (format DD-MM-YYYY)
            + Column Departure Time, Value = timeOfDeparture (format DD-MM-YYYY)
            + Column Port Days, Value = totalTimeAtPortInDays)
            + Column Shipment, Value = shipmentName
            + Column Reason, Value = reasonForVisit + cargoQuantity, eg: "Discharge 1000 Coal"
        4. Finally, Provide a comprehensive breakdown of expense in the profit and loss object (using bullet points)
        """,
    ),
)
diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        max_context_tokens=15000,
        user_instruction="""
        1. If user ask for timeline diagram, follow the below template:
        ```mermaid
        gantt
            title [Vessel Name] Timeline
            dateFormat  DD-MM-YYYY
            section [Port Name]
            Arrive [Port Name]: [Time of Arrival], 0d
            [Reason + (Shipment)]: [Arrival Time], [Port Days]d
            Depart [Port Name]: [Time of Departure], 0d
        ```
        """,
    ),
)
chart_assistant = ChartAssistant(
    show_code_stream=False,
    llm_mathplot_code_writer=MathplotCodeWriter(
        llm_model=Gemini(),
        max_context_tokens=15000,
        user_instruction="""
        1. If user ask for cost breakdown analysis, make 2 pie charts in the same figure:
        - Pie Chart 1: Expenses Breakdown:
            + Break down all the expenses structure of the estimate.
            + Use "#FF5722" color for "Bunker Expense Value".
            + Use "#AB47BC" color for "Canal Tolls Value".
            + Use "#BCAAA4" color for "Emission Expense Value".
            + Use "#9E9E9E" color for "External Commission Value".
            + Use "#757575" color for "Internal Commission Value".
            + Use "#CDDC39" color for "Misc Expense Value".
            + Use "#FFC107" color for "Cargo Expense Value".
            + Use "#FF9800" color for "Port Expense Value".
            + Use "#607D8B" color for "Vessel Hire Value".
        - Pie Chart 2: Profit Margin chart
            + Display the percentage of "Total Profit Value" over the "Freight Value".
            + Use "#2196F3" color for "Freight Value".
            + Use "#4CAF50" color for "Total Profit Value" if it is positive, otherwise use "#EF5350" color.
        """
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