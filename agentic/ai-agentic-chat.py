from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend
from src.agents.models.Ollama import Ollama
from src.agents.constants import OLLAMA_CODE_MODEL

assistant = RagAssistant(
    query_function_name="match_n8n_documents_agentic_neo",
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(model=OLLAMA_CODE_MODEL),
        max_context_tokens=10000,
        instruction_template="""
        You are an intelligent coding assistants that can provide code explainations and code writing.
        First, analyze carefully the code below to base your answer on.
        {context}
        Here is the user question: {question}
        Try your best to assist the user with their coding question.
        """
    ))

app = create_chat_backend(assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)