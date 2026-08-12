"""ProgressiveAgentSLM — the single recursive agent class.

Owns ``context_window_breakdown_percentages``, ``models_ladder``,
``behavior_policies``, tools, ``memory_data_stores``, and ``delegates``; runs the
progressive loop (retrieve → assemble 3-window prompt → act → append → distil →
self-eval) and recurses into delegates.

The progressive-loop internals are identical across the three run modes
(assistant / research / reflection); the mode is the outer shell (see `modes/`).

Phase 0–1 note (2026-08-12): this is the **scaffolded skeleton** of the class —
the flat orchestrator that shipped in the previous home is being replaced by this
recursive form. The per-step loop body is stubbed and filled in by the Phase 1
checklist items.
"""
from __future__ import annotations

import asyncio
from typing import Any, AsyncGenerator, Dict, List, Optional

from .AgentConfig import AgentConfig
from .CircularRounds import CircularRounds
from .ContextWindow import ContextWindow
from .ToolRegistry import ToolRegistry
from .delegates.contracts import DelegateRequest, DelegateResult, DelegateState


class ProgressiveAgentSLM:
    """Recursive agent: a "team" is an agent whose delegates are more agents."""

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        context_window: Optional[ContextWindow] = None,
        tool_registry: Optional[ToolRegistry] = None,
        parent: Optional["ProgressiveAgentSLM"] = None,
        depth: int = 0,
    ) -> None:
        self.config = config or AgentConfig()
        self.config.validate()
        self._context_window = context_window or ContextWindow.from_config(
            self.config.context_window_breakdown_percentages
        )
        self._tool_registry = tool_registry or ToolRegistry()
        self._rounds = CircularRounds(
            max_total=self.config.behavior_policies_max_circular_rounds
        )
        self.parent = parent
        self.depth = depth

        # Recursively build delegates (each inherits from this agent's config).
        self.delegates: List["ProgressiveAgentSLM"] = []
        for dcfg in self.config.delegates:
            dcfg.inherit_from(self.config)
            self.delegates.append(
                ProgressiveAgentSLM(
                    config=dcfg,
                    context_window=ContextWindow.from_config(dcfg.context_window_breakdown_percentages),
                    parent=self,
                    depth=self.depth + 1,
                )
            )

        # Register tools from config (loader-bound) into the registry.
        for tool_cfg in self.config.tools:
            self._register_tool_from_config(tool_cfg)

    # ── Public surface ─────────────────────────────────────────────────────

    @property
    def id(self) -> str:
        return self.config.id

    @property
    def description(self) -> str:
        return self.config.description

    def delegate_by_id(self, delegate_id: str) -> Optional["ProgressiveAgentSLM"]:
        for d in self.delegates:
            if d.id == delegate_id:
                return d
        return None

    # ── Tools ──────────────────────────────────────────────────────────────

    def _register_tool_from_config(self, cfg: dict) -> None:
        """Build a tool instance from its config dict and register it.

        Phase 1 fills in the tool factories; the stub keeps the registry
        importable so the tree builds even before every tool exists.
        """
        from .tools import build_tool

        tool = build_tool(cfg)
        if tool is not None:
            self._tool_registry.register(tool)

    def add_tool(self, tool: Any) -> "ProgressiveAgentSLM":
        self._tool_registry.register(tool)
        return self

    # ── The progressive loop ───────────────────────────────────────────────

    async def stream(self, question: str, context: str = "") -> AsyncGenerator[str, None]:
        """Stream the agent's answer to *question*.

        Per-step (Phase 1 fills the stubs):
          1. retrieve relevant knowledge (memory_data_stores / raw log)
          2. assemble the 3-window prompt (stable prefix + volatile suffix)
          3. select a model from the ladder, fire behavior_policies, route
          4. answer (response_window), append + distil, self-eval
          5. recurse into delegates; stop on ladder exhaustion or round cap
        """
        if not self._rounds.consume():
            yield self._honest_stop("no rounds remaining")
            return

        # Stub loop body — replaced by Phase 1 checklist items. Kept functional
        # so the scaffold is runnable end-to-end with a stub model.
        async for chunk in self._respond(question, context):
            yield chunk

    async def _respond(self, question: str, context: str) -> AsyncGenerator[str, None]:
        # Phase 1: replace with the real 3-window prompt assembly + model call.
        prompt = self._assemble_prompt(question, context)
        # A real model call goes here (ModelChain-selected). Stub: echo.
        yield prompt

    def _assemble_prompt(self, question: str, context: str) -> str:
        parts = [self.config.system_prompt or f"You are {self.description}"]
        if self.config.behavior_policies:
            rules = "\n".join(
                f"- When {p.get('when', '')}, then {p.get('then', '')}."
                for p in self.config.behavior_policies
            )
            parts.append("Behavior policies:\n" + rules)
        if self.delegates:
            descs = "\n".join(f"- delegate:{d.id}: {d.description}" for d in self.delegates)
            parts.append("Available delegates:\n" + descs)
        tool_menu = self._tool_registry.descriptions()
        if tool_menu:
            parts.append("Tools:\n" + tool_menu)
        if context:
            parts.append("Context:\n" + context)
        parts.append("Question: " + question)
        return "\n\n".join(parts)

    def _honest_stop(self, reason: str) -> str:
        return f"[stopped: {reason}] I could not complete this safely and prefer not to invent an answer."

    # ── Delegate dispatch (Phase 1) ────────────────────────────────────────

    async def dispatch(
        self, request: DelegateRequest, delegate_id: Optional[str] = None
    ) -> DelegateResult:
        """Run a delegate's own full loop and return its frozen result."""
        target = self.delegate_by_id(delegate_id) if delegate_id else (self.delegates[0] if self.delegates else None)
        if target is None:
            return DelegateResult(state=DelegateState.FAILED, summary={"answer": "no delegate"}, diagnostic="unknown delegate")
        answer = ""
        async for chunk in target.stream(request.goal, request.context or ""):
            answer += chunk
        return DelegateResult(
            state=DelegateState.SUCCEEDED,
            summary={"answer": answer, "evidence_refs": [], "confidence": 0.5},
            ref=f"[{target.config.folder}]/iteration_logging/",
            confidence=0.5,
        )
