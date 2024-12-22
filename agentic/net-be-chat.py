from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from src.RagAssistant import RagAssistant
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.agents.models.Ollama import Ollama
from src.agents.constants import OLLAMA_CODE_MODEL

net_be_assistant = RagAssistant(
    query_function_name="match_n8n_documents_net_micro_neo",
    llm_rag_answer=GeneralRagAnswer(
        llm_model=Ollama(
            model=OLLAMA_CODE_MODEL
        ),
    ),
    max_context_tokens=11000,
    max_histories_tokens=200)

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
        return StreamingResponse(net_be_assistant.stream(user_question, history), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
def get_last_user_question(messages):
    return [message.content for message in messages if message.role == "user"][-1]
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)