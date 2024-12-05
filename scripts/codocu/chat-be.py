import os
from typing import Generator, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.BackendDocumentor import BackendDocumentor
from agents.BvmsKnowledgeBase import BvmsKnowledgeBase
from agents.AssistantOrchestra import AssistantOrchestra

from jobs.RelevantCodeBlockFinder import RelevantCodeBlockFinder
from jobs.FilePrioritizer import FilePrioritizer
from jobs.CodeExplainer import CodeExplainer

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL = "http://10.13.13.4:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"

DOCU_TABLE_NAME = "n8n_documents_ebook"
DPCU_FUNCTION = "match_n8n_documents_ebook_neo"

BVMS_TABLE_NAME = "n8n_documents_bbc_bvms"
BVMS_FUNCTION = "match_n8n_documents_bbc_bvms"

documentor_vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, DOCU_TABLE_NAME, DPCU_FUNCTION)
bvms_vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, BVMS_TABLE_NAME, BVMS_FUNCTION)

with open(os.path.join(os.path.dirname(__file__), "prompts/Document-Prompt.txt"), "r", encoding="utf-8") as file:
    documentor_prompt = file.read()

with open(os.path.join(os.path.dirname(__file__), "prompts/BVMS-Prompt.txt"), "r", encoding="utf-8") as file:
    bvms_prompt = file.read()

embedder = CreateEmbedding(url=f'http://10.13.13.4:11434/api/embed', model='nomic-embed-text:137m-v1.5-fp16')
filePrioritizer = FilePrioritizer(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')
codeExplainer = CodeExplainer(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')
codeBlockFinder = RelevantCodeBlockFinder(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')

documentor = BackendDocumentor(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')
documentor.set_embedder(embedder)
documentor.set_vector_store(documentor_vector_store)
documentor.set_base_prompt(documentor_prompt)
documentor.set_code_block_finder(codeBlockFinder)
documentor.set_file_prioritizer(filePrioritizer)
documentor.set_code_explainer(codeExplainer)
documentor.set_max_context_tokens_length(6000)
documentor.set_max_history_tokens_length(10)
documentor.set_match_count(20)

bvms_answer = BvmsKnowledgeBase(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')
bvms_answer.set_embedder(embedder)
bvms_answer.set_vector_store(bvms_vector_store)
bvms_answer.set_base_prompt(bvms_prompt)
bvms_answer.set_max_context_tokens_length(6000)
bvms_answer.set_max_history_tokens_length(100)
documentor.set_match_count(200)

orchesrea = AssistantOrchestra(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')
orchesrea.add_agent("Code Documentor", "This agent can answer codes related questions about BVMS Backend software, which is built using .NET", documentor)
orchesrea.add_agent("BVMS General", "This agent can answer general questions about business knowledge of BVMS, which is a maritime software that handle cargo, shipments and estimate profit and loss for voyages. It also contains some api informations about sedna.", bvms_answer)

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
        return StreamingResponse(orchesrea.stream(user_question, history), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
