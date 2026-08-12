"""Model clients for ProgressiveAgentSLM.

All clients expose an async ``stream(prompt) -> AsyncGenerator[str, None]``
interface so the framework can route jobs across the ``models_ladder``.
Local-first (Ollama / LM Studio) with cloud (OpenRouter) fallback.
"""
