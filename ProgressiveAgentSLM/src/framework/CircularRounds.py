"""CircularRounds — thread-safe total-work budget for behavior_policies loops.

Pattern ported from Hermes ``agent/iteration_budget.py`` (MIT). This is the
**total-work** budget, kept separate from model failover: it bounds
``behavior_policies`` circular loops by ``behavior_policies_max_circular_rounds``
(default 5). Either this cap OR model-ladder exhaustion ends a run (§2, §4, §5).

The key refinement (Hermes lesson): programmatic / batched tool turns are
**refunded** — a tool call the loop itself issued (not the model) should not burn
the model's iteration budget.
"""
from __future__ import annotations

import threading


class CircularRounds:
    """Thread-safe consume/refund round counter for one agent.

    Each agent (parent or delegate) gets its own counter. The parent's cap comes
    from ``behavior_policies_max_circular_rounds`` (default 5); a delegate may
    pin its own cap, else inherits the parent's. ``refund`` gives back one round
    for batched/programmatic tool turns so they don't eat the budget.
    """

    def __init__(self, max_total: int) -> None:
        self.max_total = max_total
        self._used = 0
        self._lock = threading.Lock()

    def consume(self) -> bool:
        """Try to consume one round. Returns True if allowed."""
        with self._lock:
            if self._used >= self.max_total:
                return False
            self._used += 1
            return True

    def refund(self) -> None:
        """Give back one round (e.g. for batched tool turns)."""
        with self._lock:
            if self._used > 0:
                self._used -= 1

    @property
    def used(self) -> int:
        with self._lock:
            return self._used

    @property
    def remaining(self) -> int:
        with self._lock:
            return max(0, self.max_total - self._used)

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return f"CircularRounds(used={self._used}, max={self.max_total})"


__all__ = ["CircularRounds"]
