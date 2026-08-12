"""host/create_chat_backend — minimal FastAPI streaming backend for the demo.

Provides an OpenAI-compatible ``POST /api/answer/stream`` (and a stub
``/api/v1/chat/completions``) that streams the agent's ``.stream()`` output.
Kept intentionally small — a full AssistantMode FastAPI server lands in Phase 3.
"""
from __future__ import annotations

import asyncio
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


class ChatRequest(BaseModel):
    messages: list[dict] = []  # [{"role": "user", "content": "..."}]


def _latest_question(messages: list[dict]) -> str:
    for m in reversed(messages or []):
        if m.get("role") == "user":
            return str(m.get("content", ""))
    return ""


def create_chat_backend(agent: Any) -> FastAPI:
    """Build a FastAPI app that streams answers from *agent* (has .stream())."""
    app = FastAPI(title="ProgressiveAgentSLM")

    @app.post("/api/answer/stream")
    async def answer_stream(req: ChatRequest) -> StreamingResponse:
        question = _latest_question(req.messages)
        if not question:
            return StreamingResponse(iter([""]))

        async def _gen() -> AsyncGenerator[str, None]:
            async for chunk in agent.stream(question):
                yield chunk

        return StreamingResponse(_gen(), media_type="text/plain")

    @app.get("/api/v1/models")
    async def models():
        names = [f"{e.platform}/{e.name}" for e in getattr(agent.config, "models_ladder", [])]
        return {"models": names}

    return app