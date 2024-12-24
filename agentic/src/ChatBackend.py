from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

class Message(BaseModel):
    role: str  # e.g., "user", "assistant"
    content: str  # Message text
# Define a model for the expected request body
class CompletionRequest(BaseModel):
    messages: List[Message]

def get_last_user_question(messages):
    return [message.content for message in messages if message.role == "user"][-1]

def create_chat_backend(assistant):
    app = FastAPI()
    @app.post("/api/answer/stream")
    async def get_answer_for_question_stream(request: CompletionRequest):
        try:
            user_question = get_last_user_question(request.messages)
            history = [message for message in request.messages or []]
            return StreamingResponse(assistant.stream(user_question, history), media_type="application/json")

        except Exception as e:
            print(f"Error handling request: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    return app