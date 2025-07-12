from src.agents.models.Ollama import Ollama
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend
from src.agents.DocumentRanking import DocumentRanking

bvms_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    llm_document_ranking=DocumentRanking(
        llm_model=Ollama(),
    ),
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(num_ctx=28000),
        max_context_tokens=32000,
        instruction_template="""
        You are an intelligent assistant that can provide detailed answers about a software named BVMS (BBC Voyager Management System).
        First, analyze carefully the below knowledge base to base your answer on.
        {context}
        Here is the user question: {question}
        Try your best to assist the user with their question. Be as detailed and accurate as possible.
        """
    ))

app = create_chat_backend(bvms_rag_assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)