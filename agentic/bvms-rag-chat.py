from src.agents.models import Ollama
from src.agents import GeneralRagAnswer
from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend

bvms_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    llm_rag_answer=GeneralRagAnswer(
        max_context_tokens=12000,
        llm_model=Ollama(num_ctx=15200)
    )
)

app = create_chat_backend(bvms_rag_assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)