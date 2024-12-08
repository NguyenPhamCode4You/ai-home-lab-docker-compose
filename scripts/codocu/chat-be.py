import os
from typing import Generator, List, Optional
from pydantic import BaseModel


from agents.CodeDocumentor import CodeDocumentor
from agents.RagKnowledgeBase import RagKnowledgeBase
from agents.AssistantOrchestra import AssistantOrchestra

from jobs.CodeBlockExtractor import CodeBlockExtractor

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL = "http://10.13.13.4:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"

DOCU_TABLE_NAME = "n8n_documents_net_micro"
DPCU_FUNCTION = "match_n8n_documents_net_micro_neo"

BVMS_TABLE_NAME = "n8n_documents_bbc_bvms"
BVMS_FUNCTION = "match_n8n_documents_bbc_bvms"

documentor_vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, DOCU_TABLE_NAME, DPCU_FUNCTION)
bvms_vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, BVMS_TABLE_NAME, BVMS_FUNCTION)

with open(os.path.join(os.path.dirname(__file__), "prompts/Document-Prompt.txt"), "r", encoding="utf-8") as file:
    documentor_prompt = file.read()

with open(os.path.join(os.path.dirname(__file__), "prompts/BVMS-Prompt.txt"), "r", encoding="utf-8") as file:
    bvms_prompt = file.read()

embedder = CreateEmbedding(url=f'http://10.13.13.4:11434/api/embed', model='nomic-embed-text:137m-v1.5-fp16')
codeBlockExtractor = CodeBlockExtractor(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')

documentor = CodeDocumentor(url=f'http://10.13.13.4:11434/api/generate', model='qwen2.5-coder:14b-instruct-q6_K')
documentor.set_embedder(embedder)
documentor.set_vector_store(documentor_vector_store)
documentor.set_base_prompt(documentor_prompt)
documentor.set_code_block_extractor(codeBlockExtractor)
documentor.set_be_host_url("http://10.13.13.2:8000")
documentor.set_max_context_tokens_length(5600)
documentor.set_max_history_tokens_length(10)
documentor.set_match_count(15)

bvms_answer = RagKnowledgeBase(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')
bvms_answer.set_embedder(embedder)
bvms_answer.set_vector_store(bvms_vector_store)
bvms_answer.set_base_prompt(bvms_prompt)
bvms_answer.set_max_context_tokens_length(5600)
bvms_answer.set_max_history_tokens_length(10)
bvms_answer.set_match_count(200)

orchesrea = AssistantOrchestra(url=f'http://10.13.13.4:11434/api/generate', model='gemma2:9b-instruct-q8_0')
orchesrea.set_max_history_tokens_length(5000)
orchesrea.add_agent("BVMS KnowledgeBase", """
This agent can answer general questions about business knowledge of BVMS, which is a maritime software that handle cargo, shipments and estimate profit and loss for voyages. 
It also contains some api informations about Sedna & DA Desk.
It knows about the business logics of cargo planner software.
""", bvms_answer)

orchesrea.add_agent("BVMS Code Document", """
This agent can provide code snippets and documentations about BVMS Backend source code, which is built using .NET
However, it should not be used for debugging or fixing code issues, or writing new code.
""", documentor)

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import markdown

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

# Serve the 'Coducu result' directory at '/public'
app.mount("/public", StaticFiles(directory="codocu_results"), name="public")

@app.get("/markdown-viewer", response_class=HTMLResponse)
async def render_markdown(
    path: str = Query(..., description="Path to the markdown file"),
    highlight: str = Query(None, description="Text to highlight in the markdown")
):
    
    # Check if the file exists and is a Markdown file
    if not os.path.exists(path) or not path.endswith(".md"):
        raise HTTPException(status_code=404, detail="Markdown file not found or invalid file type")

    # Read and convert the Markdown file to HTML
    try:
        with open('markdown-html.txt', "r", encoding="utf-8") as file:
            markdown_html = file.read()
        
        with open(path, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()

        html_content = markdown.markdown(markdown_content)

        # Basic HTML template
        html_template = markdown_html.replace("{html_content}", html_content).replace("{highlight}", highlight or "")
        return HTMLResponse(content=html_template)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering file: {e}")


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
