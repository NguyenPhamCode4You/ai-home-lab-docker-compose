"""
explore_csharp.py — Live C# codebase Q&A server (no RAG, no pre-indexing).

Accepts user questions via POST /api/answer/stream, selects the most relevant
.cs files from CIA_CODEBASE_PATH, and streams answers from Claude Sonnet.

Usage:
  python explore_csharp.py

Required env vars:
  CIA_CODEBASE_PATH      — absolute path to the C# project root
  OPENROUTER_API_KEY     — OpenRouter API key

Optional env vars:
  CIA_EXPLORER_MODEL         — model to use (default: anthropic/claude-sonnet-4.6)
  CIA_EXPLORER_MAX_FILES     — max files sent per request (default: 20)
  CIA_EXPLORER_MAX_FILE_CHARS — chars read per file before truncation (default: 15000)
  CIA_IGNORE_FILES           — comma-separated glob patterns to skip (inherits from pipeline)
"""

from src.CSharpSourceExplorer import CSharpSourceExplorer
from src.ChatBackend import create_chat_backend
from dotenv import load_dotenv

load_dotenv()

assistant = CSharpSourceExplorer()

app = create_chat_backend(assistant)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)
