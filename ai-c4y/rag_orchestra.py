from src.ChatBackend import create_chat_backend
from src.AssistantOrchestra import AssistantOrchestra
from src.DiagramAssistant import DiagramAssistant
from src.agents.MermaidCodeWriter import MermaidCodeWriter
from src.agents.models.Ollama import Ollama
from src.agents.models.Gemini import Gemini
from rag_chat_bvms import bvms_rag_assistant
from rag_chat_bvms_code import bvms_code_rag_assistant
from src.RagAssistant import RagAssistant
from src.agents.DocumentRanking import DocumentRanking
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.agents.QuestionForwarder import QuestionForwarder
from src.agents.FinalThoughtSummarizer import FinalThoughtSummarizer
from src.agents.AnswerEvaluator import AnswerEvaluator
from src.agents.IterationSummarizer import IterationSummarizer
from src.agents.models.OpenRouter import OpenRouter

from dotenv import load_dotenv
load_dotenv()

default_model = Ollama()
# default_model = OpenRouter()

assistant = AssistantOrchestra(
    llm_question_forwarder=QuestionForwarder(
        llm_model=default_model,
    ),
    llm_final_thought_summarizer=FinalThoughtSummarizer(
        llm_model=default_model,
    ),
    llm_answer_evaluator=AnswerEvaluator(
        llm_model=default_model,
    ),
    llm_iteration_summarizer=IterationSummarizer(
        llm_model=default_model,
    ),
    max_iterations=3,
)
assistant.agents = {
    "BVMS-General Assistant": {"agent": bvms_rag_assistant, "context_awareness": True, "description": "This agent can generate detailed responses about general information about a software named BVMS (BBC Voyager Management System), and also provide good understanding about it business domain."},
    "BVMS-Code Assistant": {"agent": bvms_code_rag_assistant, "context_awareness": True, "description": "This agent is expert in answering code / features / deep technical aspect of the software named BVMS (BBC Voyager Management System), and can provide detailed code snippets, technical explanations, and insights about the codebase."},
}

if __name__ == "__main__":
    import uvicorn
    app = create_chat_backend(assistant)
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)