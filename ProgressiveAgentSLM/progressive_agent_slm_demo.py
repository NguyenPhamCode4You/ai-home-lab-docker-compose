"""progressive_agent_slm_demo.py — entry point for ProgressiveAgentSLM.

Loads the canonical config (JSONC) → builds the recursive agent tree → serves
via create_chat_backend on port 8001.

Run:
    python progressive_agent_slm_demo.py
Then POST to http://localhost:8001/api/answer/stream with
{"messages": [{"role": "user", "content": "..."}]}
"""
from __future__ import annotations

import os

import uvicorn
from dotenv import load_dotenv

from src.framework.config.load import load_agent
from src.host.ChatBackend import create_chat_backend

load_dotenv()


def main() -> None:
    """Build the agent tree from the canonical config and serve it."""
    config_path = os.getenv(
        "PROGRESSIVE_AGENT_CONFIG",
        "src/framework/example-revised.json",
    )
    agent = load_agent(config_path)
    app = create_chat_backend(agent)
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)


if __name__ == "__main__":
    main()