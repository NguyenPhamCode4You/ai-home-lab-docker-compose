from src.ChatBackend import create_chat_backend
from src.ChartAssistant import ChartAssistant
from src.agents.models.ChatGpt import ChatGpt
from src.agents.MathplotCodeWriter import MathplotCodeWriter

from dotenv import load_dotenv
import os
load_dotenv()

chart_assistant = ChartAssistant(
    llm_mathplot_code_writer=MathplotCodeWriter(
        llm_model=ChatGpt(),
        max_context_tokens=10000,
    )
)

app = create_chat_backend(chart_assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)