from src.agents.models.Ollama import Ollama
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend
from src.agents.DocumentRanking import DocumentRanking
from dotenv import load_dotenv
from src.agents.models.OpenRouter import OpenRouter

load_dotenv()

default_model = Ollama()
# default_model = OpenRouter(model='qwen/qwen3.6-35b-a3b')

bvms_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    llm_document_ranking=DocumentRanking(
        llm_model=Ollama(model="gemma3:4b"),
    ),
    llm_rag_answer=GeneralRagAnswer(
        llm_model=default_model,
        instruction_template="""
        You are an intelligent assistant that can provide detailed answers about a software named BVMS (BBC Voyager Management System).
        First, analyze carefully the below knowledge base to base your answer on.
        {context}
        Here is the user question: {question}
        Only focus on the relevant information related to the user question from the knowledge base to provide a detailed answer. 
        Try your best to assist the user with their question. Be as detailed and accurate as possible.
        """
    ))

if __name__ == "__main__":
    import uvicorn
    app = create_chat_backend(bvms_rag_assistant)
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)