from src.ChatBackend import create_chat_backend
from src.AssistantOrchestra import AssistantOrchestra
from src.DiagramAssistant import DiagramAssistant
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.models.Ollama import Ollama
from rag_chat_bvms import bvms_rag_assistant
# from rag_chat_imos import imos_rag_assistant
from src.RagAssistant import RagAssistant
from src.agents.DocumentRanking import DocumentRanking
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.agents.QuestionForwarder import QuestionForwarder
from src.agents.FinalThoughtSummarizer import FinalThoughtSummarizer

from dotenv import load_dotenv
load_dotenv()

diagram_assistant = DiagramAssistant(
    llm_mermaid_code_writter=MermaidCodeWriter(
        llm_model=Ollama(num_ctx=32000),
        max_context_tokens=32000,
    )
)

bvms_code_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_neo",
    llm_document_ranking=DocumentRanking(
        llm_model=Ollama(model="gemma3:4b"),
    ),
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(model="qwen3.5:9b", num_ctx=24000),
        max_context_tokens=36000,
        instruction_template="""
        You are an intelligient assistant that can provide code snippet and explaination for a software named BVMS (BBC Voyager Management System).
        First, analyze carefully the below knowledge base to base your answer on.
        {context}
        Here is the user question: {question}
        Only focus on the relevant information related to the user question from the knowledge base to provide a detailed answer. 
        Try your best to assist the user with their question. Be as detailed and accurate as possible.
        """
    ))

assistant = AssistantOrchestra(
    llm_question_forwarder=QuestionForwarder(
        llm_model=Ollama(model="gemma3:12b"),
     ),
     llm_final_thought_summarizer=FinalThoughtSummarizer(
        llm_model=Ollama(model="gemma3:12b"),
     )
)
assistant.agents = {
    "Diagram Assistant": {"agent": diagram_assistant, "context_awareness": True, "description": "This agent can generate diagrams and workflows based on a given context"},
    "BVMS-General Assistant": {"agent": bvms_rag_assistant, "context_awareness": True, "description": "This agent can generate detailed responses about a software named BVMS (BBC Voyager Management System)"},
    "BVMS-Code Assistant": {"agent": bvms_code_assistant, "context_awareness": True, "description": "This agent can provide code snippet and code explaination for a software named BVMS (BBC Voyager Management System)"},
}

if __name__ == "__main__":
    import uvicorn
    app = create_chat_backend(assistant)
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)