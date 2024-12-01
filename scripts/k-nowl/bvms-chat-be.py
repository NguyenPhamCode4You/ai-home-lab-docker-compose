from typing import Generator, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from AssistantAnswer import AssistantAnswer

from CreateEmbedding import CreateEmbedding
from SupabaseVectorStore import SupabaseVectorStore
from AssistantAnswer import AssistantAnswer

OLLAMA_URL = "http://10.13.13.4:11434"
SUPABASE_URL = "http://10.13.13.4:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_bbc_bvms"
vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)

embedder = CreateEmbedding(url=f'{OLLAMA_URL}/api/embed')
assistant = AssistantAnswer(url=f'{OLLAMA_URL}/api/generate')
assistant.set_embedder(embedder)
assistant.set_vector_store(vector_store)

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

@app.post("/api/retrieve")
async def get_documents_from_question(request: CompletionRequest):
    try:
        user_question = get_last_user_question(request.messages)
        documents = assistant.retrieve_documents(user_question)
        return JSONResponse(
            content={
                "documents": documents,
                "done": True,
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/answer")
async def get_answer_for_question(request: CompletionRequest):
    try:
        user_question = get_last_user_question(request.messages)
        history = [message for message in request.messages or []]
        # Remove last user question from history
        history = history[:-1]
        response = assistant.run(user_question, history)
        # Return the response
        return JSONResponse(
            content={
                "answer": response,
                "done": True,
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/answer/stream")
async def get_answer_for_question_stream(request: CompletionRequest):
    try:
        user_question = get_last_user_question(request.messages)
        history = [message for message in request.messages or []]
        history = history[:-1]  # Remove the last user question from history

        # Define a generator for streaming response
        def response_generator() -> Generator[str, None, None]:
            try:
                # Use a regular generator to stream responses
                for chunk in assistant.stream(user_question, history):
                    yield chunk
            except Exception as e:
                # Log the error and yield an error message
                print(f"Error during stream generation: {e}")
                yield f"Error: {str(e)}"

        # Return a StreamingResponse with the generator
        return StreamingResponse(
            response_generator(),
            media_type="text/plain",
        )

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
