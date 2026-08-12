"""delegates/contracts — typed immutable delegate boundary.

Pattern ported from Hermes ``agent/subagent_lifecycle.py`` (MIT). A parent never
hands a delegate a live agent object; it hands a **frozen request** and receives
a **frozen result**, with an explicit state machine. Byte caps bound the goal /
context / result so a deep delegate tree can't balloon memory.
"""
from __future__ import annotations

import dataclasses
import enum
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Tuple

# Byte caps (mirror Hermes).
MAX_GOAL_CHARS = 16_000
MAX_CONTEXT_CHARS = 32_000
MAX_RESULT_CHARS = 32_000


class DelegateState(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


def _check_byte_cap(text: str, cap: int, name: str) -> str:
    if len(text) > cap:
        raise ValueError(f"{name} exceeds {cap} chars ({len(text)})")
    return text


@dataclass(frozen=True)
class DelegateRequest:
    """Immutable request handed to a delegate."""

    goal: str
    context: Optional[str] = None
    role: str = "leaf"
    allowed_toolsets: Optional[Tuple[str, ...]] = None
    blocked_tools: Tuple[str, ...] = ()
    timeout_seconds: Optional[float] = None

    def __post_init__(self) -> None:
        _check_byte_cap(self.goal, MAX_GOAL_CHARS, "goal")
        if self.context is not None:
            _check_byte_cap(self.context, MAX_CONTEXT_CHARS, "context")


@dataclass(frozen=True)
class DelegateResult:
    """Immutable result a delegate returns to its parent."""

    state: DelegateState
    summary: Dict[str, Any] = field(default_factory=dict)
    ref: Optional[str] = None
    confidence: float = 0.0
    diagnostic: Optional[str] = None

    def __post_init__(self) -> None:
        text = str(self.summary.get("answer", ""))
        _check_byte_cap(text, MAX_RESULT_CHARS, "result.answer")


def truncated_result(result: DelegateResult, cap: int = MAX_RESULT_CHARS) -> DelegateResult:
    """Return a copy with the answer truncated to *cap* chars (defense-in-depth)."""
    answer = str(result.summary.get("answer", ""))
    if len(answer) <= cap:
        return result
    summary = dict(result.summary)
    summary["answer"] = answer[:cap]
    return DelegateResult(
        state=result.state,
        summary=summary,
        ref=result.ref,
        confidence=result.confidence,
        diagnostic=result.diagnostic,
    )


__all__ = [
    "DelegateState",
    "DelegateRequest",
    "DelegateResult",
    "MAX_GOAL_CHARS",
    "MAX_CONTEXT_CHARS",
    "MAX_RESULT_CHARS",
    "truncated_result",
]