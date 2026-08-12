"""guards/tool_loop — anti-drift tool-call loop guard.

Pattern ported from Hermes ``agent/tool_guardrails.py`` (MIT). The controller is
intentionally **side-effect free**: it tracks per-turn tool-call observations and
returns decisions. Runtime code owns whether those decisions become warning
guidance, a synthetic result, or a controlled turn halt.

The key primitive is a **stable, non-reversible signature** for a tool call:
``tool_name + sha256(canonical_args)`` — so "same tool, same args" is detected
deterministically, and the signature's public metadata never leaks raw argument
values.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, MutableMapping, Optional

IDEMPOTENT_TOOL_NAMES = frozenset({
    "read_file", "search_files", "sqlite_vector_query", "jsonl_query",
    "web_search",
})
MUTATING_TOOL_NAMES = frozenset({
    "write_file", "todo", "run_python", "generate_diagram", "search_internet",
    "code_analysis", "delegate_task",
})


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical_args(args: Mapping[str, Any]) -> str:
    """Serialize args deterministically (sorted keys) for signature hashing."""
    try:
        return json.dumps(args, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError):
        return json.dumps({})


@dataclass(frozen=True)
class ToolCallSignature:
    """Stable, non-reversible identity for a tool name plus canonical args."""

    tool_name: str
    args_hash: str

    @classmethod
    def from_call(cls, tool_name: str, args: Optional[Mapping[str, Any]]) -> "ToolCallSignature":
        return cls(tool_name=tool_name, args_hash=_sha256(_canonical_args(args or {})))

    def to_metadata(self) -> Dict[str, str]:
        """Public metadata without raw argument values."""
        return {"tool_name": self.tool_name, "args_hash": self.args_hash}


@dataclass(frozen=True)
class ToolGuardrailConfig:
    """Thresholds for per-turn tool-call loop detection."""

    warnings_enabled: bool = True
    hard_stop_enabled: bool = False
    exact_failure_warn_after: int = 2
    exact_failure_block_after: int = 5
    same_tool_failure_warn_after: int = 3
    same_tool_failure_halt_after: int = 8
    idempotent_tools: frozenset = field(default_factory=lambda: IDEMPOTENT_TOOL_NAMES)
    mutating_tools: frozenset = field(default_factory=lambda: MUTATING_TOOL_NAMES)


@dataclass(frozen=True)
class ToolGuardrailDecision:
    """Decision returned by the guard controller."""

    action: str = "allow"  # allow | warn | block | halt
    code: str = "allow"
    message: str = ""
    tool_name: str = ""


class ToolLoopGuard:
    """Per-turn (per-agent-loop) tool-call loop detector.

    Call ``observe(name, args, failed)`` after each tool call, then read
    ``decide()``. Counters reset at the start of every agent loop
    (``reset_for_turn``) so the limit is "within a single turn", not cumulative
    over the whole run.
    """

    def __init__(self, config: Optional[ToolGuardrailConfig] = None) -> None:
        self._config = config or ToolGuardrailConfig()
        self._exact_failures: MutableMapping[ToolCallSignature, int] = {}
        self._tool_failures: MutableMapping[str, int] = {}
        self._calls_by_signature: MutableMapping[ToolCallSignature, int] = {}
        self._calls_by_tool: MutableMapping[str, int] = {}

    def reset_for_turn(self) -> None:
        self._exact_failures.clear()
        self._tool_failures.clear()
        self._calls_by_signature.clear()
        self._calls_by_tool.clear()

    # -- observation ---------------------------------------------------------

    def observe(self, tool_name: str, args: Optional[Mapping[str, Any]], failed: bool = False) -> None:
        sig = ToolCallSignature.from_call(tool_name, args)
        self._calls_by_signature[sig] = self._calls_by_signature.get(sig, 0) + 1
        self._calls_by_tool[tool_name] = self._calls_by_tool.get(tool_name, 0) + 1
        if failed:
            self._exact_failures[sig] = self._exact_failures.get(sig, 0) + 1
            self._tool_failures[tool_name] = self._tool_failures.get(tool_name, 0) + 1

    # -- decision ------------------------------------------------------------

    def decide(self, tool_name: str, args: Optional[Mapping[str, Any]], failed: bool) -> ToolGuardrailDecision:
        sig = ToolCallSignature.from_call(tool_name, args)
        if failed:
            exact = self._exact_failures.get(sig, 0)
            by_tool = self._tool_failures.get(tool_name, 0)
            if self._config.hard_stop_enabled and exact >= self._config.exact_failure_block_after:
                return ToolGuardrailDecision("block", "exact_failure_block", f"Tool {tool_name!r} failed {exact}x; blocking.", tool_name)
            if exact >= self._config.exact_failure_warn_after:
                return ToolGuardrailDecision("warn", "exact_failure_warn", f"Tool {tool_name!r} failed {exact}x; check it.", tool_name)
            if self._config.hard_stop_enabled and by_tool >= self._config.same_tool_failure_halt_after:
                return ToolGuardrailDecision("halt", "same_tool_failure_halt", f"Tool {tool_name!r} failing repeatedly ({by_tool}x); halting.", tool_name)
            if by_tool >= self._config.same_tool_failure_warn_after:
                return ToolGuardrailDecision("warn", "same_tool_failure_warn", f"Tool {tool_name!r} failing {by_tool}x this turn.", tool_name)

        total = self._calls_by_signature.get(sig, 0)
        if self._config.hard_stop_enabled and total >= self._config.exact_failure_block_after and tool_name not in self._config.mutating_tools:
            return ToolGuardrailDecision("block", "idempotent_repeat_block", f"Idempotent {tool_name!r} called {total}x identically; blocking.", tool_name)
        if total >= self._config.exact_failure_warn_after and tool_name in self._config.idempotent_tools:
            return ToolGuardrailDecision("warn", "idempotent_repeat_warn", f"Idempotent {tool_name!r} called {total}x identically; ensure progress.", tool_name)
        return ToolGuardrailDecision("allow", "allow", "", tool_name)