from src.ChatBackend import create_chat_backend
from agentic.src.ChartAssistant import ChartAssistant

assistant = ChartAssistant()

app = create_chat_backend(assistant)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)