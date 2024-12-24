from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from src.ResearchAssistant import ResearchAssistant
from src.agents.models.Ollama import Ollama
from src.agents.models.Gemini import Gemini
from src.agents.ContextSummarizer import ContextSummarizer

research_assistant = ResearchAssistant(
    topics_count=3,
    # llm_context_summarizer=ContextSummarizer(
    #     llm_model=Gemini(),
    #     max_char=4000,
    #     context_chunk_size=200000
    # ),
)

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
        return StreamingResponse(research_assistant.stream(user_question, history), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
def get_last_user_question(messages):
    return [message.content for message in messages if message.role == "user"][-1]
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)