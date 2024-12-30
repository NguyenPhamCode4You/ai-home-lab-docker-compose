import json
import os


from agents.RagKnowledgeBase import RagKnowledgeBase

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL    = "http://10.13.13.4:8000"
SUPABASE_TOKEN  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_ops"
FUNCTION   = "match_n8n_documents_ops_neo"

# OLLAMA_URL      = "http://10.13.13.4:11434"
# CODE_MODEL      = "qwen2.5-coder:14b-instruct-q6_K"
# GENERAL_MODEL   = "gemma2:9b-instruct-q8_0"

OLLAMA_URL      = "http://10.13.13.5:11434"
CODE_MODEL      = "qwen2.5-coder:32b"
GENERAL_MODEL   = "gemma2:27b-instruct-q5_1"
# GENERAL_MODEL   = "qwen2.5:32b"

EMBEDING_MODEL  = "nomic-embed-text:137m-v1.5-fp16"

embedder = CreateEmbedding(
    url=OLLAMA_URL,
    model=EMBEDING_MODEL
)
vector_store = SupabaseVectorStore(
    url=SUPABASE_URL,
    token=SUPABASE_TOKEN,
    table_name=TABLE_NAME,
    function_name=FUNCTION
)
knowledge_base = RagKnowledgeBase(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    embedder=embedder,
    vector_store=vector_store,
    max_context_tokens_length=8900,
    max_history_tokens_length=10,
    base_prompt="""
    You are an intelligent RAG AI agent that can restructure a given complex knowledge of a software named IMOS to help users understand it better.

    Here is the given knowledge about IMOS software:
    {context}
    -----------------------------------

    Here is the user question: {question}
    Consider the relevant information to the user question, then generate a WELL-STRUCTURED, BULLET-POINT, ACCURATE and DETAILED answer!
    Always explain in great details, enrich with your knowledge, and provide examples where necessary, unless instructued otherwise.

    Now, answer with confidence.
    """
)

from jobs.KeywordExtractor import KeywordExtractor
from jobs.SentenceSummarizer import SentenceSummarizer
from jobs.MarkdownProcessor import MarkdownProcessor

# async def learn():
    # await knowledge_base.formatting(
    #     original_folder_path=".\operation-scape-logs",
    #     formatted_folder_path=".\operation-scape-logs-formated",
    #     markdown_processor=MarkdownProcessor(
    #         url=OLLAMA_URL,
    #         model=GENERAL_MODEL
    #     ),
    #     chunk_size=600
    # )
    # await knowledge_base.learn(
    #     folder_path=".\operation-scape-logs-formated",
    #     keyword_extractor=KeywordExtractor(
    #         url=OLLAMA_URL,
    #         model=GENERAL_MODEL
    #     ),
    #     sentence_summarizer=SentenceSummarizer(
    #         url=OLLAMA_URL,
    #         model=GENERAL_MODEL
    #     )
    # )
    # async for agent_chunk in knowledge_base.stream("Can you tell me how BVMS calculate EU ETS?", []):
    #     if (len(agent_chunk) > 1000):
    #         continue
    #     agent_response = json.loads(agent_chunk)["response"]
    #     print(agent_response, end="", flush=True)  # Real-time console output


# import asyncio
# asyncio.run(example2())
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
        return StreamingResponse(knowledge_base.stream(user_question, history), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)
