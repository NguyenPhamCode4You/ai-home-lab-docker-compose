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
# from src.agents.models.Gemini import Gemini
from src.agents.constants import OLLAMA_CODE_MODEL

from dotenv import load_dotenv
import os
load_dotenv()

api_assistant = ApiCallerAssistant(
    base_url="https://bvms-master-api-test.azurewebsites.net",
    bearer_token=os.getenv("BVMS_API_TOKEN"),
    api_instructions=[
        "/Vessels/Search - Method: POST - Description: Search for vessels using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL.",
        "/Ports/Search - Method: POST - Description: Search for ports using keywords, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL.",
    ]
)
chart_assistant = ChartAssistant()
diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        # llm_model=Gemini(),
        max_context_tokens=10000,
    )
)
research_assistant = ResearchAssistant(topics_count=3)
bvms_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    llm_rag_answer=GeneralRagAnswer(
        # llm_model=Gemini(),
        max_context_tokens=9000,
        context_chunk_size=5500,
        instruction_template="""
        You are an intelligent assistant that can provide detailed responses about a software named BVMS.
        First, analyze carefully the below knowledge base to base your answer on.
        {context}
        Here is the user question: {question}
        Try your best to assist the user with their question.
        """
    )
)
be_code_assistant = RagAssistant(
    query_function_name="match_n8n_documents_net_micro_neo",
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(model=OLLAMA_CODE_MODEL),
        max_context_tokens=18000,
        context_chunk_size=10000,
        allow_reflection=True,
        instruction_template="""
        You are an intelligent coding assistants that can provide code explanations and code writing.
        First, analyze carefully the code below to base your answer on.
        {context}
        Here is the user question: {question}
        Try your best to assist the user with their coding question.
        """
    ))

assistant = AssistantOrchestra()
assistant.agents = {
    "API Assistant": {"agent": api_assistant, "context_awareness": True, "description": "This agent can get information about Vessels and Ports"},
    "Chart Assistant": {"agent": chart_assistant, "context_awareness": True, "description": "This agent can generate data charts based on a given data"},
    "Diagram Assistant": {"agent": diagram_assistant, "context_awareness": True, "description": "This agent can generate diagrams and workflows based on a given context"},
    "Research Assistant": {"agent": research_assistant, "context_awareness": False, "description": "This agent can generate detailed web-research on complex topics"},
    "RAG Assistant": {"agent": bvms_rag_assistant, "context_awareness": False, "description": "This agent can generate detailed responses about a software named BVMS"},
    "Code Assistant": {"agent": be_code_assistant, "context_awareness": False, "description": "This agent can provide code explanations and code writing about BVMS software"}
}

app = create_chat_backend(assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)