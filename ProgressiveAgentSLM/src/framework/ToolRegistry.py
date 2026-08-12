"""ToolRegistry — base Tool + dispatch.

Each tool carries a ``name``, ``description``, a ``when`` guidance string (used
for menu pruning), and an optional own ``models_ladder`` (inherits the agent's
ladder when omitted, §6). Tools are dispatched by the same code path as agents
via a default ``stream()`` that wraps ``run()``.
"""
from __future__ import annotations

from typing import AsyncGenerator, Dict, List, Optional


class Tool:
    """Base class / protocol for all framework tools."""

    name: str = "tool"
    description: str = "A tool."
    when: str = ""

    def __init__(self, models_ladder: Optional[List[dict]] = None) -> None:
        # Optional own ladder — inherits the agent's when omitted (§6).
        self.models_ladder = models_ladder

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
    """Registry of named Tool instances, keyed by name."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def names(self) -> List[str]:
        return list(self._tools.keys())

    def descriptions(self) -> str:
        # Include the `when` guidance so a small model calls the tool at the
        # right moment (prompt menu), §6.
        lines = []
        for _name, tool in self._tools.items():
            line = f"- **{tool.name}**: {tool.description}"
            if tool.when:
                line += f" — _when: {tool.when}_"
            lines.append(line)
        return "\n".join(lines)

    def prune_by_when(self, step: str) -> List[str]:
        """Return only the tool names whose ``when`` matches the current step.

        Naive substring match on the `when` text vs. the step marker; override to
        tie to the same vocabulary as ``behavior_policies`` run_after hooks.
        """
        step_key = step.lower()
        out = []
        for name, tool in self._tools.items():
            if not tool.when or step_key in tool.when.lower():
                out.append(name)
        return out