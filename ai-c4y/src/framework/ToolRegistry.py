"""ToolRegistry — registry for callable tools.

Tool protocol::

    class MyTool(Tool):
        name = "my_tool"
        description = "What this tool does."

        async def run(self, question: str, context: str = None,
                      conversation_history: list = None) -> str:
            ...

Tools are also given a default ``stream()`` that wraps ``run()``, so they
can be dispatched by the same code path as agents.
"""
from __future__ import annotations

from typing import AsyncGenerator, Dict, Optional


class Tool:
    """Base class / protocol for all framework tools."""

    name: str = "tool"
    description: str = "A tool."

    async def stream(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> AsyncGenerator[str, None]:
        """Default streaming wrapper — calls run() and yields the result in one chunk."""
        result = await self.run(question, context, conversation_history)
        yield result

    async def run(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> str:
        raise NotImplementedError(f"{self.__class__.__name__}.run() not implemented")


class ToolRegistry:
    """Registry of named Tool instances."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def names(self) -> list:
        return list(self._tools.keys())

    def descriptions(self) -> str:
        return "\n".join(
            f"- **{name}**: {tool.description}"
            for name, tool in self._tools.items()
        )
