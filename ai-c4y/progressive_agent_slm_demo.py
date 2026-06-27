"""progressive_agent_slm_demo.py — minimal entry point for ProgressiveAgentSLM.

Wires a bare ProgressiveAgentSLM (no sub-agents) into create_chat_backend
and serves it on port 8001.  Extend by calling agent.add_agent() / agent.add_tool()
below to register delegates.

Run:
    python progressive_agent_slm_demo.py
Then POST to http://localhost:8001/api/answer/stream with {"messages": [{"role": "user", "content": "..."}]}
"""
import uvicorn

from dotenv import load_dotenv

from src.framework.AgentConfig import AgentConfig, ReflectionConfig
from src.framework.ModelRegistry import ModelRegistry
from src.framework.ProgressiveAgentSLM import ProgressiveAgentSLM
from src.framework.tools.ReadFileTool import ReadFileTool
from src.agents.models.Ollama import Ollama
from src.ChatBackend import create_chat_backend

load_dotenv()

# ── Model registry (local/SLM-first) ──────────────────────────────────────
# Swap any role to OpenRouter by adding it to the chain, e.g.:
#   from src.agents.models.OpenRouter import OpenRouter
#   reasoning=[Ollama(model="qwen3.6:27b"), OpenRouter(model="anthropic/claude-3.5-sonnet")]
models = ModelRegistry(
    chat=[Ollama(model="gemma4:e4b")],
    reflection=[Ollama(model="gpt-oss:20b")],
    reasoning=[Ollama(model="qwen3.6:27b")],
)

# ── Agent config ───────────────────────────────────────────────────────────
config = AgentConfig(
    goal="Answer the user's question accurately, using available delegates when helpful.",
    reflection=ReflectionConfig(enabled=True, every_step=True),
    max_steps=4,
    compact_threshold_tokens=24000,
    runs_dir="runs",
)

# ── Build agent ────────────────────────────────────────────────────────────
agent = ProgressiveAgentSLM(config=config, model_registry=models)

# Register built-in tools
agent.add_tool(ReadFileTool())

# ── Register sub-agents here ───────────────────────────────────────────────
# Example (uncomment after importing your assistants):
#
# from rag_chat_bvms import bvms_rag_assistant
# from rag_chat_bvms_code import bvms_code_rag_assistant
# agent.add_agent(
#     "BVMS-General",
#     "Business workflow & domain knowledge about BVMS.",
#     bvms_rag_assistant,
#     context_awareness=True,
# )
# agent.add_agent(
#     "BVMS-Code",
#     "Deep technical/code aspects of BVMS.",
#     bvms_code_rag_assistant,
#     context_awareness=True,
# )

# ── Serve ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        create_chat_backend(agent),
        host="0.0.0.0",
        port=8001,
        timeout_keep_alive=300,
    )
