"""ModelRegistry — maps role names to ordered model fallback chains.

Local/SLM-first: defaults to small Ollama models for every role.
Any role can be escalated to a cloud model (OpenRouter) by extending its chain.

Usage::

    # All defaults (reads FRAMEWORK_*_MODEL env vars, falls back to hardcoded names)
    registry = ModelRegistry()

    # Override the reasoning role with a local→cloud chain
    registry = ModelRegistry(
        reasoning=[Ollama(model="qwen3.6:27b"), OpenRouter(model="anthropic/claude-3.5-sonnet")],
    )

    # Stream from a role (falls through to next model on pre-stream error)
    async for chunk in registry.stream("reasoning", prompt):
        ...
"""
from __future__ import annotations

import os
from typing import Any, AsyncGenerator, Dict, List

from dotenv import load_dotenv

load_dotenv()

_DEFAULT_CHAT_MODEL = os.getenv("FRAMEWORK_CHAT_MODEL", "gemma4:e4b")
_DEFAULT_REFLECTION_MODEL = os.getenv("FRAMEWORK_REFLECTION_MODEL", "gpt-oss:20b")
_DEFAULT_REASONING_MODEL = os.getenv("FRAMEWORK_REASONING_MODEL", "qwen3.6:27b")


class ModelRegistry:
    """
    Maps role → ordered fallback chain of model clients.

    Falls through to the next model in the chain on timeout / HTTP error,
    *before* any chunks are yielded.  Once streaming starts the model is
    committed for that call.
    """

    def __init__(self, **role_chains: List | Any) -> None:
        # Lazy import avoids circular dependencies at module load time
        from src.agents.models.Ollama import Ollama

        self._chains: Dict[str, List] = {
            "chat": [Ollama(model=_DEFAULT_CHAT_MODEL)],
            "reflection": [Ollama(model=_DEFAULT_REFLECTION_MODEL)],
            "reasoning": [Ollama(model=_DEFAULT_REASONING_MODEL)],
        }
        for role, chain in role_chains.items():
            self._chains[role] = chain if isinstance(chain, list) else [chain]

    def get(self, role: str) -> Any:
        """Return the *first* model in the chain for *role* (falls back to chat)."""
        chain = self._chains.get(role) or self._chains.get("chat", [])
        if not chain:
            raise RuntimeError(f"[ModelRegistry] No model configured for role '{role}'")
        return chain[0]

    def get_chain(self, role: str) -> List:
        return self._chains.get(role) or self._chains.get("chat", [])

    async def stream(self, role: str, prompt: str) -> AsyncGenerator[str, None]:
        """
        Stream from the first available model in the chain for *role*.

        If a model raises an exception *before* yielding any chunk it is
        skipped and the next model is tried.  Once chunks start arriving
        the stream is committed to that model.
        """
        chain = self.get_chain(role)
        if not chain:
            raise RuntimeError(f"[ModelRegistry] No model configured for role '{role}'")

        for idx, model in enumerate(chain):
            chunks_yielded = False
            try:
                async for chunk in model.stream(prompt):
                    chunks_yielded = True
                    yield chunk
                return  # finished successfully
            except Exception as exc:
                if chunks_yielded:
                    raise  # mid-stream failure — cannot recover
                remaining = len(chain) - idx - 1
                if remaining:
                    print(
                        f"[ModelRegistry] role='{role}' chain[{idx}] failed ({exc}); "
                        f"trying next ({remaining} left).",
                        flush=True,
                    )
                    continue
                raise
