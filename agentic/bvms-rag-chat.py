from src.agents.models.Ollama import Ollama
from src.DiagramAssistant import DiagramAssistant
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend
from src.agents.DocumentRanking import DocumentRanking
from src.AssistantOrchestra import AssistantOrchestra

bvms_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    llm_document_ranking=DocumentRanking(
        llm_model=Ollama(),
    ),
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(num_ctx=28000),
        max_context_tokens=32000,
        instruction_template="""
        You are an intelligent coding assistants that can provide code explanations and code writing.
        First, analyze carefully the code below to base your answer on.
        {context}
        Here is the user question: {question}
        Try your best to assist the user with their coding question.
        """
    ))

diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        llm_model=Ollama(num_ctx=28000),
        max_context_tokens=32000,
    )
)

assistant = AssistantOrchestra()
assistant.agents = {
    "Diagram Assistant": {"agent": diagram_assistant, "context_awareness": True, "description": "This agent can generate diagrams and workflows based on a given context"},
    "BVMS Knowledge Assistant": {"agent": bvms_rag_assistant, "context_awareness": False, "description": "This agent can generate detailed responses about a software named BVMS"},
}

app = create_chat_backend(bvms_rag_assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)