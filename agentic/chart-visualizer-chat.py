from src.ChatBackend import create_chat_backend
from src.ChartAssistant import ChartAssistant

assistant = ChartAssistant()

app = create_chat_backend(assistant)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)