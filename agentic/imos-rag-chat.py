from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.agents.FinalThoughtSummarizer import FinalThoughtSummarizer
from src.agents.models.Ollama import Ollama
from src.agents.models.ChatGpt import ChatGpt
from src.agents.models.Gemini import Gemini
from src.agents.models.Perplexity import Perplexity
from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend
from src.agents.Task import Task

imos_simple_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_ops_neo",
    max_context_tokens=11000,
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(),
        context_chunk_size=5600,
        allow_reflection=True
    ))

imos_detailed_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_ops_neo",
    max_context_tokens=15000,
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(),
        context_chunk_size=5600,
    ),
    llm_context_enricher=Task(
        task_name="imos-rag-context-enricher",
        llm_model=Perplexity(),
        instruction_template="{question}",
    ),
    llm_final_summarizer=FinalThoughtSummarizer(
        llm_model=Gemini(),
        context_chunk_size=15000
    ))

app = create_chat_backend(imos_simple_rag_assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)