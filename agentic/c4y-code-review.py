from src.GitlabCodeReviewer import GitlabCodeReviewer
from src.agents.CodeReviewer import CodeReviewer
from src.agents.models.Ollama import Ollama
from src.ChatBackend import create_chat_backend

assistant = GitlabCodeReviewer(
    llm_code_reviewer=CodeReviewer(
        llm_model=Ollama(model="qwen2.5-coder:32b"),
        max_context_tokens=32000,
    ))

app = create_chat_backend(assistant)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)