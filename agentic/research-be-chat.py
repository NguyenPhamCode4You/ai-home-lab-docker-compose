from src.ChatBackend import create_chat_backend
from src.ResearchAssistant import ResearchAssistant

research_assistant = ResearchAssistant(
    topics_count=3,
)

app = create_chat_backend(research_assistant)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)