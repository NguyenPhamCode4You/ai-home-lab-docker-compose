from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend

bvms_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    max_context_tokens=6500)

app = create_chat_backend(bvms_rag_assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)