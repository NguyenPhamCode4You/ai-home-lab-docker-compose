import json
import os
from typing import Generator, List, Optional
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from agents.CodeDocumentor import CodeDocumentor
from agents.RagKnowledgeBase import RagKnowledgeBase
from agents.AssistantOrchestra import AssistantOrchestra
from agents.SwaggerApiCaller import SwaggerApiCaller
from agents.ChartVisualizer import ChartVisualizer

from jobs.CodeBlockExtractor import CodeBlockExtractor

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL    = "http://10.13.13.4:8000"
SUPABASE_TOKEN  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"

DOCU_TABLE_NAME = "n8n_documents_net_micro"
DPCU_FUNCTION   = "match_n8n_documents_net_micro_neo"

BVMS_TABLE_NAME = "n8n_documents_bbc_bvms"
BVMS_FUNCTION   = "match_n8n_documents_bbc_bvms"

# OLLAMA_URL      = "http://10.13.13.5:11434"
# CODE_MODEL      = "gemma2:27b-instruct-q5_1"
# GENERAL_MODEL   = "gemma2:27b-instruct-q5_1"

OLLAMA_URL      = "http://10.13.13.4:11434"
CODE_MODEL      = "qwen2.5-coder:14b-instruct-q6_K"
GENERAL_MODEL   = "gemma2:9b-instruct-q8_0"

EMBEDING_MODEL  = "nomic-embed-text:137m-v1.5-fp16"
HOSTING_URL     = "http://10.13.13.2:8000"

documentor_vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, DOCU_TABLE_NAME, DPCU_FUNCTION)
bvms_vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, BVMS_TABLE_NAME, BVMS_FUNCTION)

with open(os.path.join(os.path.dirname(__file__), "prompts/Document-Prompt.txt"), "r", encoding="utf-8") as file:
    documentor_prompt = file.read()

with open(os.path.join(os.path.dirname(__file__), "prompts/BVMS-Prompt.txt"), "r", encoding="utf-8") as file:
    bvms_prompt = file.read()

embedder = CreateEmbedding(url=f'{OLLAMA_URL}/api/embed', model=EMBEDING_MODEL)
codeBlockExtractor = CodeBlockExtractor(url=f'{OLLAMA_URL}/api/generate', model=GENERAL_MODEL)

documentor = CodeDocumentor(url=f'{OLLAMA_URL}/api/generate', model=CODE_MODEL)
documentor.set_embedder(embedder)
documentor.set_vector_store(documentor_vector_store)
documentor.set_base_prompt(documentor_prompt)
documentor.set_code_block_extractor(codeBlockExtractor)
documentor.set_be_host_url(HOSTING_URL)
documentor.set_max_context_tokens_length(12000)
documentor.set_max_history_tokens_length(10)
documentor.set_match_count(15)

bvms_answer = RagKnowledgeBase(url=f'{OLLAMA_URL}/api/generate', model=GENERAL_MODEL)
bvms_answer.set_embedder(embedder)
bvms_answer.set_vector_store(bvms_vector_store)
bvms_answer.set_base_prompt(bvms_prompt)
bvms_answer.set_max_context_tokens_length(8000)
bvms_answer.set_max_history_tokens_length(10)
bvms_answer.set_match_count(200)

vessel_master = SwaggerApiCaller(url=f'{OLLAMA_URL}/api/generate', model=CODE_MODEL)
vessel_master.set_api_url("https://bvms-master-api-test.azurewebsites.net")
vessel_master.set_bearer_token(os.getenv("API_TOKEN"))
vessel_master.set_allowed_api_paths([
    ("/Vessels/Search", "Method: POST, Description: Search for vessels using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL."),
    ("/Vessels/{vesselId}", "Method: GET, Description: Get vessel details by vessel GUID. This include information about where the vessel is currently located, its current speed, and its current heading"),
    ("/Vessels/{vesselId}/ConsumptionRates/Search", "Method: POST, Description: Search for vessel bunker or fuel consumption rate using vessel GUID. Body = {pageSize} with pageSize default = 3, max = 5. No query in the URL."),
])
vessel_master.set_instructions("""
1a. If user asks for vessel bunker or fuel consumption:
- First call /Vessels/Search to get the vessel GUID 
- Then replace the vessel ID inside this API call /Vessels/{vesselId}/ConsumptionRates/Search to get the vessel bunker details.
1b. Otherwise, always call /Vessels/Search.
""")

port_master = SwaggerApiCaller(url=f'{OLLAMA_URL}/api/generate', model=CODE_MODEL)
port_master.set_api_url("https://bvms-master-api-test.azurewebsites.net")
port_master.set_bearer_token(os.getenv("API_TOKEN"))
port_master.set_allowed_api_paths([
    ("/Ports/Search", "Method: POST, Description: Search for ports using keywords, but cannot search for ID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL."),
])

voyage_data = SwaggerApiCaller(url=f'{OLLAMA_URL}/api/generate', model=CODE_MODEL)
voyage_data.set_api_url("https://bvms-voyage-api-test.azurewebsites.net")
voyage_data.set_bearer_token(os.getenv("API_TOKEN"))
voyage_data.set_allowed_api_paths([
    ("/Estimates/Search", "Method: POST, Description: Search for estimates using keywords, but cannot search for ID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL."),
    ("/Shipments/Search", "Method: POST, Description: Search for shipments using keywords, but cannot search for ID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL.")
])

charter = ChartVisualizer(url=f'{OLLAMA_URL}/api/generate', model=CODE_MODEL)
charter.set_temp_file_path(os.path.join(os.path.dirname(__file__), "codocu_results"))
charter.set_host_url(f"{HOSTING_URL}/public")

orchesrea = AssistantOrchestra(url=f'{OLLAMA_URL}/api/generate', model=GENERAL_MODEL)
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

orchesrea.add_agent("Vessel Master", """
This agent can provide detailed information about Vessels of BBC by making API calls.
""", vessel_master)

orchesrea.add_agent("Estimate Master", """
This agent can provide detailed information about BVMS Estimates of Shipments (Order request) by making API calls.
""", voyage_data)

orchesrea.add_agent("Port Master", """
This agent can provide detailed information about Marinetime Ports, by making API calls.
""", port_master)

orchesrea.add_agent("Chart Visualizer", """
This agent can help user create simple charts basing on a given data. Supported chart types are: line, bar, pie.
""", charter)

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import markdown

# Initialize FastAPI
app = FastAPI()
# Serve the 'Coducu result' directory at '/public'
app.mount("/public", StaticFiles(directory="codocu_results"), name="public")

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
        # history = history[:-1]  # Remove the last user question from history
        return StreamingResponse(orchesrea.stream(user_question, history), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
    
# import asyncio

# question = """
# I need you to write an analysis on how BVMS calculate EU ETS. To do that, follow the below steps:
# 1. Ask BVMS KnowledgeBase to explain the business logics of how BVMS calculate Bunker consumption.
# 2. Ask BVMS Code Document to provide code implementation and explanation for the topic of Bunker consumption.
# 3. Ask BVMS KnowledgeBase to explain the business logics of how BVMS calculate EU ETS.
# 4. Ask BVMS Code Document to provide code implementation and explanation for calculate EU ETS.
# Basing on the information you gather, write an analysis on how BVMS calculate EU ETS.
# Be prefessional and detailed in your analysis, provide code snippets and documentations as needed.
# """
# orchesrea.set_log_file(os.path.join(os.path.dirname(__file__), "task-log.md"))
# asyncio.run(orchesrea.write_analysis(question))


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)
