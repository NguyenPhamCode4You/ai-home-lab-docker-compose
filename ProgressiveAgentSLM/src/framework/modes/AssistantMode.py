"""modes/AssistantMode — run_mode=assistant HTTP server (OpenAI-compatible).

Phase 3 wires the FastAPI server (api_configuration): CORS / auth, streaming +
non-streaming ``/api/v1/chat/completions``, ``/api/v1/models``, and
``/api/v1/health`` (§7b). Stub keeps the mode importable.
"""
from __future__ import annotations

from typing import Any


class AssistantMode:
    name = "assistant"

    def __init__(self, api_configuration: Any = None, communication_channels: Any = None) -> None:
        self.api_configuration = api_configuration or {}
        self.communication_channels = communication_channels or {}

    def build_app(self, agent: Any) -> Any:
        """Phase 3: return a FastAPI app wired to *agent*."""
        raise NotImplementedError("AssistantMode.build_app lands in Phase 3")