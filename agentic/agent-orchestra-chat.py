from src.RagAssistant import RagAssistant
from src.ApiCallerAssistant import ApiCallerAssistant
from src.ChatBackend import create_chat_backend
from src.ChartAssistant import ChartAssistant
from src.ResearchAssistant import ResearchAssistant
from src.AssistantOrchestra import AssistantOrchestra
from src.DiagramAssistant import DiagramAssistant
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.models.Ollama import Ollama
from src.agents.models.ChatGpt import ChatGpt
from src.agents.constants import OLLAMA_CODE_MODEL
from src.agents.DocumentRanking import DocumentRanking
from src.agents.MathplotCodeWriter import MathplotCodeWriter
from src.agents.JSONSummarizer import JSONSummarizer
from src.agents.DocumentRanking import DocumentRanking
from src.agents.ApiConfigWritter import ApiConfigWritter
from src.ImageProviderAssistant import ImageProviderAssistant

from dotenv import load_dotenv
import os
load_dotenv()

api_assistant = ApiCallerAssistant(
    base_url="https://bvms-master-api-test.azurewebsites.net",
    llm_api_config_writter=ApiConfigWritter(
        llm_model=ChatGpt(),
    ),
    llm_json_summarizer=JSONSummarizer(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
    ),
    bearer_token=os.getenv("BVMS_API_TOKEN"),
    api_instructions=[
        "/Vessels/Search - Method: POST - Description: Search for vessels using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3. No query in the URL.",
        "/Ports/Search - Method: POST - Description: Search for ports using keywords, Body = {keySearch, pageSize} with pageSize default = 3. No query in the URL.",
    ]
)

shipment_assistant = ApiCallerAssistant(
    base_url="https://bvms-voyage-api-test.azurewebsites.net",
    llm_api_config_writter=ApiConfigWritter(
        llm_model=ChatGpt(),
    ),
    llm_json_summarizer=JSONSummarizer(
        llm_model=ChatGpt(),
        max_context_tokens=15000,
    ),
    bearer_token=os.getenv("BVMS_API_TOKEN"),
    api_instructions=[
        "/Shipments/Search - Method: POST - Description: Search for shipments using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3. No query in the URL."
        "/Shipments/shipmentId?shipmentId=UUID - Method: GET - Description: Get a shipment by its UUID. The UUID is a unique identifier for a shipment."
    ]
)

chart_assistant = ChartAssistant(
    llm_mathplot_code_writer=MathplotCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=10000,
    )
)
diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=10000,
    )
)
image_assistant = ImageProviderAssistant(
    llm_model=Ollama(),
)
research_assistant = ResearchAssistant(topics_count=3)
bvms_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    llm_document_ranking=DocumentRanking(
        llm_model=Ollama(),
    ),
    llm_rag_answer=GeneralRagAnswer(
        max_context_tokens=6000,
        llm_model=Ollama(),
        instruction_template="""
        You are an intelligent assistant that can provide detailed answers about a software named BVMS (BBC Voyager Management System).
        First, analyze carefully the below knowledge base to base your answer on.
        {context}
        Here is the user question: {question}
        Try your best to assist the user with their question. Be as detailed and accurate as possible.
        """
    )
)
be_code_assistant = RagAssistant(
    query_function_name="match_n8n_documents_net_micro_neo",
    llm_document_ranking=DocumentRanking(
        llm_model=ChatGpt(model="o1-mini"),
    ),
    llm_rag_answer=GeneralRagAnswer(
        llm_model=ChatGpt(model="o1-mini"),
        max_context_tokens=12000,
        instruction_template="""
        You are an intelligent coding assistants that can provide code explanations and code writing.
        First, analyze carefully the code below to base your answer on.
        {context}
        Here is the user question: {question}
        Try your best to assist the user with their coding question.
        """
    ))

from EstimateSpecialist import estimate_specialist

assistant = AssistantOrchestra()
assistant.agents = {
    "API Assistant": {"agent": api_assistant, "context_awareness": True, "description": "This agent can get information about Vessels and Ports"},
    "Shipment Assistant": {"agent": shipment_assistant, "context_awareness": True, "description": "This agent can get information about BVMS Shipments"},
    "Chart Assistant": {"agent": chart_assistant, "context_awareness": True, "description": "This agent can generate data charts based on a given data"},
    "Diagram Assistant": {"agent": diagram_assistant, "context_awareness": True, "description": "This agent can generate diagrams and workflows based on a given context"},
    "Image Assistant": {"agent": image_assistant, "context_awareness": True, "description": "This agent can provide images search based on a given context"},
    "Research Assistant": {"agent": research_assistant, "context_awareness": False, "description": "This agent can generate detailed web-research on complex topics"},
    "RAG Assistant": {"agent": bvms_rag_assistant, "context_awareness": False, "description": "This agent can generate detailed responses about a software named BVMS"},
    "Code Assistant": {"agent": be_code_assistant, "context_awareness": False, "description": "This agent can provide code explanations and code writing about BVMS software"},
    "Estimate Specialist": {"agent": estimate_specialist, "context_awareness": False, "description": "This agent can provide detailed analysis of BVMS Estimates"}
}

app = create_chat_backend(assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)