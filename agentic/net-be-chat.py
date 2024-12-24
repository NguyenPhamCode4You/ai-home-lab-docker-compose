from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.agents.models.Ollama import Ollama
from src.agents.constants import OLLAMA_CODE_MODEL

net_be_assistant = RagAssistant(
    query_function_name="match_n8n_documents_net_micro_neo",
    max_context_tokens=12000,
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(
            model=OLLAMA_CODE_MODEL,
        ),
        context_chunk_size=5500,
        allow_reflection=True
    ))

app = create_chat_backend(net_be_assistant)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)