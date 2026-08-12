"""src.agents — model clients and tool wrappers (local/SLM-first)."""

from .models.Ollama import Ollama
from .models.OpenRouter import OpenRouter

__all__ = ["Ollama", "OpenRouter"]
