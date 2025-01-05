from src.ApiCallerAssistant import ApiCallerAssistant
from src.DiagramAssistant import DiagramAssistant
from src.ChartAssistant import ChartAssistant
from src.AssistantOrchestra import AssistantOrchestra
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.MathplotCodeWriter import MathplotCodeWriter
from src.agents.QuestionForwarder import QuestionForwarder
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
        2. If user ask for expense breakdown, provide a pie chart follow the below template:
        (Remember not to include the "Total Profit" and "Freight Value" in the pie chart)
        ```mermaid
        pie
            title Expenses Breakdown
            "Bunker Expense": [Bunker Expense Value]
            ...
        ```
        3. If user ask for profit margin, provide a pie chart follow the below template:
        ```mermaid
        pie
            title Profit Margin
            "Freight Value": [Freight Value]
            "Total Profit Value": [Total Profit Value]
        ```
        """,
    ),
)
chart_assistant = ChartAssistant(
    show_code_stream=False,
    llm_mathplot_code_writer=MathplotCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
        user_instruction="""
        1. If user ask for cost breakdown analysis, make 2 pie charts in the same figure:
        - Pie Chart 1: Expenses Breakdown:
            + Break down all the expenses structure of the estimate
            + Use "#EF5350" color for "Bunker Expense"
            + Use "#7E57C2" color for "Emission Expense"
            + Use "#8D6E63" color for "External Commission"
            + Use "#2196F3" color for "Internal Commission"
            + Use "#EC407A" color for "Misc Expense"
            + Use "#FFC107" color for "Cargo Expense"
            + Use "#FF9800" color for "Port Expense" and "Canal Tolls"
            + Use "#78909C" color for "Vessel Hire"
        - Pie Chart 2: Profit Margin chart
            + Display the percentage of "Total Profit" over the "Freight Value"
            + Use "#2196F3" color for "Freight Value"
            + Use "#4CAF50" color for "Total Profit Value" if it is positive, otherwise use "#EF5350" color
        - Make figure background color "#171717", Label and Title color "#FFFFFF"
        - Remember to add some offsetting pie slices
        """
    ),
)
estimate_specialist = AssistantOrchestra(
    agents={
        "API Assistant": {"agent": api_assistant, "description": "This agent can get information about Estimates of BVMS", "context_awareness": True},
        "Chart Assistant": {"agent": chart_assistant, "description": "This agent can generate data charts based on a given data", "context_awareness": True},
        "Diagram Assistant": {"agent": diagram_assistant, "description": "This agent can generate diagrams and workflows based on a given context", "context_awareness": True},
    },
    # llm_question_forwarder=QuestionForwarder(
    #     user_instruction="""
    #     For every question, always provide the following as default:
    #     1. Ask the API Assistant to provide details of the estimate with the given UUID
    #     2. Ask the Diagram Assistant to provide a timeline diagram of the itenerary items
    #     3. Ask the Diagram Assistant to provide an expense breakdown
    #     4. Ask the Diagram Assistant to provide a profit margin chart
    #     5. Ask the Chart Assistant to provide a cost breakdown analysis of the estimate
    #     Then produce more questions to the agents according to the user's requirements.
    #     """
    # )
)
if __name__ == "__main__":
    import uvicorn
    app = create_chat_backend(estimate_specialist)
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)