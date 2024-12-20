from models.Ollama import Ollama
from tools.Job import Job

ollama = Ollama()
file_path = "C:\\Users\\niche\\ai-home-lab-docker-compose\\agentic\\logs\\crawler\\2024-12-20\\firecraw-2024-12-20-httpsenwikipediaorgwikiPythonprogramminglanguage.md"
with open(file_path, "r", encoding="utf-8") as file:
    url_content = file.read()

agent=Job(
    name="PythonProgrammingAnswer",
    model=ollama,
    instruction="""
    Given the context {context}
    Answer the following questions: {question}
    Provide the answer in a clear, well-structured bullet point format.
    """
)

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
        return StreamingResponse(agent.stream(user_question, url_content), media_type="application/json")

    except Exception as e:
        print(f"Error handling request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)