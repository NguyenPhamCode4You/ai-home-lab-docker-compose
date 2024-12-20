import json
import os
from agents.CodeDocumentor import CodeDocumentor
from agents.CodeSnippetProvider import CodeSnippetProvider

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL    = "http://10.13.13.4:8000"
SUPABASE_TOKEN  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"

# OLLAMA_URL      = "http://10.13.13.4:11434"
# CODE_MODEL      = "qwen2.5-coder:14b-instruct-q6_K"
# GENERAL_MODEL   = "gemma2:9b-instruct-q8_0"

OLLAMA_URL      = "http://10.13.13.5:11434"
CODE_MODEL      = "qwen2.5-coder:32b"
GENERAL_MODEL   = "gemma2:27b-instruct-q5_1"

EMBEDING_MODEL  = "nomic-embed-text:137m-v1.5-fp16"

from jobs.KeywordExtractor import KeywordExtractor
code_snippet_provider = CodeSnippetProvider(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    max_context_tokens_length=9000,
    embedder=CreateEmbedding(
        url=OLLAMA_URL,
        model=EMBEDING_MODEL
    ),
    vector_store=SupabaseVectorStore(
        url=SUPABASE_URL,
        token=SUPABASE_TOKEN,
        table_name="n8n_documents_net_micro",
        function_name="match_n8n_documents_net_micro_neo"
    )
)

async def learn():
    code_document_folder_path = os.path.join(os.getcwd(), "codocu_results", "code-documentation")
    bvms_document_path = os.path.join(code_document_folder_path, "bbc-bvms-net-back-end-modular")
    await code_snippet_provider.learn(
        folder_path=bvms_document_path,
        keyword_extractor=KeywordExtractor(
            url=OLLAMA_URL,
            model=GENERAL_MODEL
        ),
    )


import asyncio
# asyncio.run(learn())

def get_last_user_question(messages):
    return [message.content for message in messages if message.role == "user"][-1]

from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

# Define a model for the input specific to /api/chat
class Message(BaseModel):
    role: str  # e.g., "user", "assistant"
    content: str  # Message text
# Define a model for the expected request body
class CompletionRequest(BaseModel):
    messages: List[Message]

app = FastAPI()
@app.post("/api/answer/stream")
async def get_answer_for_question_stream(request: CompletionRequest):
    try:
        user_question = get_last_user_question(request.messages)
        history = [message for message in request.messages or []]
        return StreamingResponse(code_snippet_provider.stream(user_question, history), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)
