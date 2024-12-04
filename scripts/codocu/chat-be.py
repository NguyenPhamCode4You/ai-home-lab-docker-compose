from typing import Generator, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .RelevantCodeBlockFinder import RelevantCodeBlockFinder
from .CodeBlockExtractor import CodeBlockExtractor
from .FilePrioritizer import FilePrioritizer

from ..knowl.AssistantAnswer import AssistantAnswer
from ..knowl.CreateEmbedding import CreateEmbedding
from ..knowl.SupabaseVectorStore import SupabaseVectorStore
from ..knowl.AssistantAnswer import AssistantAnswer
import os

SUPABASE_URL = "http://10.13.13.4:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_ebook"
FUNCTION = "match_n8n_documents_ebook_neo"
vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME, FUNCTION)

OLLAMA_URL = "http://10.13.13.4:11434"
# OLLAMA_MODEL = "qwen2.5-coder:14b-instruct-q6_K"
OLLAMA_MODEL = "gemma2:9b-instruct-q8_0"

prompt_path = os.path.join(os.path.dirname(__file__), "Rag-Prompt.txt")
with open(prompt_path, "r", encoding="utf-8") as file:
    base_prompt_default = file.read()

embedder = CreateEmbedding(url=f'{OLLAMA_URL}/api/embed')
assistant = AssistantAnswer(url=f'{OLLAMA_URL}/api/generate', model=OLLAMA_MODEL)
codeBlockFinder = RelevantCodeBlockFinder(url=f'{OLLAMA_URL}/api/generate', model=OLLAMA_MODEL)
codeBlockExtractor = CodeBlockExtractor(url=f'{OLLAMA_URL}/api/generate', model=OLLAMA_MODEL)
filePrioritizer = FilePrioritizer(url=f'{OLLAMA_URL}/api/generate', model=OLLAMA_MODEL)

assistant.set_embedder(embedder)
assistant.set_vector_store(vector_store)
assistant.set_base_prompt(base_prompt_default)
assistant.set_code_block_finder(codeBlockFinder)
assistant.set_code_block_extractor(codeBlockExtractor)
assistant.set_file_prioritizer(filePrioritizer)
assistant.set_max_context_tokens_length(5000)
assistant.set_max_history_tokens_length(200)
assistant.set_match_count(20)

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

# Initialize FastAPI
app = FastAPI()

# Define a model for the input specific to /api/chat
class Message(BaseModel):
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Define a model for the expected request body
class CompletionRequest(BaseModel):
    messages: List[Message]

def get_last_user_question(messages):
    return [message.content for message in messages if message.role == "user"][-1]
    
@app.post("/api/answer/stream")
async def get_answer_for_question_stream(request: CompletionRequest):
    try:
        user_question = get_last_user_question(request.messages)
        history = [message for message in request.messages or []]
        history = history[:-1]  # Remove the last user question from history
        return StreamingResponse(assistant.stream_answer_from_files(user_question, history), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
