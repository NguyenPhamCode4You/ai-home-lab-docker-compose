import os
from typing import List
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from jobs.RelevantDocumentExtractor import RelevantDocumentExtractor
from jobs.UrlSummarizer import UrlSummarizer

from agents.CodeDocumentor import CodeDocumentor
from agents.RagKnowledgeBase import RagKnowledgeBase
from agents.AssistantOrchestra import AssistantOrchestra
from agents.SwaggerApiCaller import SwaggerApiCaller
from agents.ChartVisualizer import ChartVisualizer
from agents.WebSearchAgent import WebSearchAgent
from agents.PerflexityAgent import PerflexityAgent

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL    = "http://10.13.13.4:8000"
SUPABASE_TOKEN  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"

OLLAMA_URL      = "http://10.13.13.5:11434"
CODE_MODEL      = "qwen2.5-coder:32b"
GENERAL_MODEL   = "gemma2:27b-instruct-q5_1"

# OLLAMA_URL      = "http://10.13.13.4:11434"
# CODE_MODEL      = "qwen2.5-coder:14b-instruct-q6_K"
# GENERAL_MODEL   = "gemma2:9b-instruct-q8_0"

EMBEDING_MODEL  = "nomic-embed-text:137m-v1.5-fp16"
HOSTING_URL     = "http://10.13.13.2:8000"

embedder = CreateEmbedding(
    url=OLLAMA_URL,
    model=EMBEDING_MODEL
)
perflexity_knowledge = PerflexityAgent(
    api_key=os.getenv("PERFLEXITY_API_KEY"),
    log_folder=os.path.join(os.path.dirname(__file__), "web_search_results")
)
web_searcher = WebSearchAgent(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    serp_api_key=os.getenv("SERP_API_KEY"),
    url_summarizer=UrlSummarizer(
        url=OLLAMA_URL,
        model=GENERAL_MODEL,
        fire_craw_api_key=os.getenv("FIRE_CRAW_API_KEY"),
        log_folder=os.path.join(os.path.dirname(__file__), "web_search_results")
    ),
    match_count=3,
    log_folder=os.path.join(os.path.dirname(__file__), "web_search_results")
)
bvms_answer = RagKnowledgeBase(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    embedder=embedder,
    vector_store=SupabaseVectorStore(
        url=SUPABASE_URL,
        token=SUPABASE_TOKEN,
        table_name="n8n_documents_bbc_bvms",
        function_name="match_n8n_documents_bbc_bvms"
    ),
    match_count=200,
    max_context_tokens_length=5600,
    max_history_tokens_length=10,
    base_prompt="""
    You are an intelligent RAG AI agent for the BVMS (BBC Voyage Management System) to assist users with their questions.
    Here is the user question: {question}

    Before answering, first, analyze carefully the knowledge below to base your answer on. Consider only the relevant information to the question besing asked.
    {context}

    Then, generate a WELL-STRUCTURED, BULLET-POINT, CONCISE, ACCURATE but DETAILED answer to the question!
    Important:
    - Always base your answer on the retrieved knowledge.
    - You may enhance your response with factual support when possible.
    - If the query goes beyond retrieved knowledge, just answer that you dont have information about this topics. Dont make up information.

    Here are the previous questions and answers that you can use to base your answer on:
    {histories}

    Now, answer with confidence.
    """
)

be_documentor = CodeDocumentor(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    hosting_url=HOSTING_URL,
    embedder=embedder,
    vector_store=SupabaseVectorStore(
        url=SUPABASE_URL,
        token=SUPABASE_TOKEN,
        table_name="n8n_documents_net_micro",
        function_name="match_n8n_documents_net_micro_neo"
    ),
    document_extractor=RelevantDocumentExtractor(
        url=OLLAMA_URL,
        model=GENERAL_MODEL
    ),
    match_count=15,
    max_history_tokens_length = 10,
    max_context_tokens_length = 5800,
    base_prompt="""
    You are an experienced software developer and your task is reading a code document to answer user questions.
    Here is the code document you need to read:
    {context}
    User Question: {question}
    Try your very best to assist the user with their question.
    """
)
ai_documentor = CodeDocumentor(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    hosting_url=HOSTING_URL,
    embedder=embedder,
    vector_store=SupabaseVectorStore(
        url=SUPABASE_URL,
        token=SUPABASE_TOKEN,
        table_name="n8n_documents_ebook",
        function_name="match_n8n_documents_ebook_neo"
    ),
    document_extractor=RelevantDocumentExtractor(
        url=OLLAMA_URL,
        model=GENERAL_MODEL
    ),
    match_count=15,
    max_history_tokens_length = 10,
    max_context_tokens_length = 5800,
    base_prompt="""
    You are an experienced software developer and your task is reading a code document to answer user questions.
    Here is the code document you need to read:
    {context}
    User Question: {question}
    Try your very best to assist the user with their question.
    """
)

vessel_master = SwaggerApiCaller(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    api_url="https://bvms-master-api-test.azurewebsites.net",
    bearer_token=os.getenv("API_TOKEN"),
    allowed_api_paths=[
        ("/Vessels/Search", "Method: POST, Description: Search for vessels using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL."),
        ("/Vessels/{vesselId}/ConsumptionRates/Search", "Method: POST, Description: Search for vessel bunker or fuel consumption rate using vessel GUID. Body = {pageSize} with pageSize default = 3, max = 5. No query in the URL."),
    ],
    user_instructions="""
    """
)

outermost_master = SwaggerApiCaller(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    api_url="https://bvms-master-api-test.azurewebsites.net",
    bearer_token=os.getenv("API_TOKEN"),
    allowed_api_paths=[
        ("/Ports/Search", "Method: POST, Description: Search for ports using keywords, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL."),
    ],
    user_instructions="""
    Your task is to determine if a given marine time port name is an outermost port or not.
    First, ask the port master agent to get the "Country Code" and "UNLOCODE" of the given port name.
    Then, Check if its country code in [MF, GF, GP, MQ, YT, RE]. If yes, then its an outermost port of france.
    - If not, then get combination of country code + UNLOCDE and check if it is in [PTHOR, PTPDL, PTPRG, PTPRV, PTTER, PTFNC, ESSCT, ESLPA, ESFUE, ESSSG, ESLES, ESSPC, ESACE]
    - If yes, then its an outermost port of EU.
    Else, its not an outermost port.
    Important: Always provide Country Code and UNLOCODE of the port in your response.
    """
)

port_master = SwaggerApiCaller(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    api_url="https://bvms-master-api-test.azurewebsites.net",
    bearer_token=os.getenv("API_TOKEN"),
    allowed_api_paths=[
        ("/Ports/Search", "Method: POST, Description: Search for ports using keywords, but cannot search for ID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL."),
    ],
)

voyage_data = SwaggerApiCaller(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    api_url="https://bvms-voyage-api-test.azurewebsites.net",
    bearer_token=os.getenv("API_TOKEN"),
    allowed_api_paths=[
        ("/Estimates/Search", "Method: POST, Description: Search for estimates using keywords, but cannot search for ID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL."),
        ("/Shipments/Search", "Method: POST, Description: Search for shipments using keywords, but cannot search for ID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL.")
    ]
)

charter = ChartVisualizer(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    hosting_url=f"{HOSTING_URL}/public",
    max_history_tokens_length = 5000,
    temp_file_path = os.path.join(os.path.dirname(__file__), "codocu_results")
)

ets_port_factor = AssistantOrchestra(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    max_history_tokens_length = 5000,
    user_instructions="""
    Your task is to determine if the ETS port factor for a pair of ports.
    First, ask 2 questions separately to get the "Country Code", "UNLOCODE" and "OUTERMOST" of the given port names.
    Then, follow the below steps:
    Step 1: Check country codes of each port to see if they are from EU: [BE, BG, HR, CY, DK, EE, FI, FR, DE, GR, GP, IS, IE, IT, LV, LT, MT, MQ, NL, NO, PL, PT, RE, RO, ES, SE, MF, GF, YT, SI]
    - If both are not from EU, then the ETS port factor for each is 0%.
    - If one is from EU, then the ETS port factor for the EU port is 100% and the non-EU port is 0%.
    - If both are from EU, continue to step 2.    
    Step 2: Check weather are they coming from same country or not.
    - If they are NOT from same country, then the ETS port factor for each is 100%.
    - If they are from same country, continue to step 3.
    Step 3: Check if one of them is an outermost port.
    - If AT LEAST one of them is an outermost port, then the ETS port factor for BOTH is 0%.
    - If none of them is an outermost port, then the ETS port factor for each is 100%.
    """
)

ets_port_factor.add_agent(
    name="Outermost Master",
    description='Given a port name, this agent can provide "Country Code", "UNLOCODE" and wether it is an "OUTERMOST" port',
    agent=outermost_master
)

master_mind = AssistantOrchestra(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    max_history_tokens_length = 5000
)
master_mind.add_agent(
    name="Backend Documentor",
    description="This agent can provide code snippets and documentations about BVMS Backend source code, which is built using .NET",
    agent=be_documentor,
)
master_mind.add_agent(
    name="AI Documentor",
    description="This agent can provide code snippets and documentations about BVMS AI Agents implementation, which is built using python",
    agent=ai_documentor,
)
master_mind.add_agent(
    name="BVMS KnowledgeBase",
    description="This agent can answer general questions about business knowledge of BVMS, which is a maritime software that handle cargo, shipments and estimate profit and loss for voyages. It also contains some api informations about Sedna & DA Desk. It knows about the business logics of cargo planner software.",
    agent=bvms_answer,
)
master_mind.add_agent(
    name="Vessel Master",
    description="This agent can provide detailed information about Vessels of BBC by making API calls.",
    agent=vessel_master,
    context_awareness=True
)
master_mind.add_agent(
    name="Shipment Master",
    description="This agent can provide detailed information about BVMS Shipments and estimated voyages by making API calls.",
    agent=voyage_data,
    context_awareness=True
)
master_mind.add_agent(
    name="Port Master",
    description="This agent can provide detailed information about Marine time Ports, by making API calls.",
    agent=port_master,
    context_awareness=True
)
master_mind.add_agent(
    name="Port Factor for ETS calculation",
    description="This agent can determine the port factor for ETS calculation for a pair of ports. Should NOT be used for business related questions.",
    agent=ets_port_factor,
    context_awareness=True
)
master_mind.add_agent(
    name="Chart Visualizer",
    description="This agent can help user create simple charts basing on a given data. Supported chart types are: line, bar, pie.",
    agent=charter,
    context_awareness=True
)
master_mind.add_agent(
    name="Web Searcher",
    description="This agent can search the web for relevant information based on user's question.",
    agent=web_searcher
)
master_mind.add_agent(
    name="Perflexity Knowledge",
    description="This agent can provide detailed information about a wide range of topics outside of BVMS.",
    agent=perflexity_knowledge
)

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import markdown

# Initialize FastAPI
app = FastAPI()
# Serve the 'Codocu result' directory at '/public'
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
        return StreamingResponse(master_mind.stream(user_question, history), media_type="application/json")

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
# Be professional and detailed in your analysis, provide code snippets and documentations as needed.
# """
# log_file_path = os.path.join(os.path.dirname(__file__), "task-log.md")
# asyncio.run(master_mind.write_analysis(question, log_file_path))


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)
