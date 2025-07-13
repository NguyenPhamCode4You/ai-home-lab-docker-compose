from src.ChatBackend import create_chat_backend
from src.AssistantOrchestra import AssistantOrchestra
from src.DiagramAssistant import DiagramAssistant
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.models.Ollama import Ollama
from rag_chat_bvms import bvms_rag_assistant
from rag_chat_imos import imos_rag_assistant

from dotenv import load_dotenv
load_dotenv()

diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        llm_model=Ollama(model='qwen2.5-coder:14b', num_ctx=22000),
        max_context_tokens=22000,
    )
)

assistant = AssistantOrchestra()
assistant.agents = {
    "Diagram Assistant": {"agent": diagram_assistant, "context_awareness": True, "description": "This agent can generate diagrams and workflows based on a given context"},
    "BVMS Rag Assistant": {"agent": bvms_rag_assistant, "context_awareness": False, "description": "This agent can generate detailed responses about a software named BVMS (BBC Voyager Management System)"},
    "IMOS Rag Assistant": {"agent": imos_rag_assistant, "context_awareness": False, "description": "This agent can generate detailed responses about a software named IMOS from Vesson"},
}

if __name__ == "__main__":
    import uvicorn
    app = create_chat_backend(assistant)
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)