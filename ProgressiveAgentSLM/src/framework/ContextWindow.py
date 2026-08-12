"""ContextWindow — three-window percentage budget over the active model's max_tokens.

The budget is expressed as **percentages** of the selected model's ``max_tokens``
(§3): ``cognition_window`` / ``attention_window`` / ``response_window``, summing
to **100**. The same config runs unchanged on any model; each window's real
allowance is inferred at runtime as ``(percentage / 100) × max_tokens``.

Also tracks the always-use-in-cognition stores (each capped by its own
``cognition_window_budget_percentage``, which is a share of the cognition window,
not of the model), and exposes the stable-prefix/volatile-suffix assembly helper
(prompt-cache discipline: the prefix is rebuilt only on a sanctioned compaction).
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .tokens import count_tokens

DEFAULTS = {
    "cognition_window": 32.5,
    "attention_window": 52.5,
    "response_window": 15.0,
}


class ContextWindow:
    """Holds the three window percentages and resolves them to token budgets."""

    def __init__(self, cognition_window: float = None, attention_window: float = None,
                 response_window: float = None) -> None:
        self.cognition_window = cognition_window if cognition_window is not None else DEFAULTS["cognition_window"]
        self.attention_window = attention_window if attention_window is not None else DEFAULTS["attention_window"]
        self.response_window = response_window if response_window is not None else DEFAULTS["response_window"]
        total = self.cognition_window + self.attention_window + self.response_window
        if abs(total - 100.0) > 1e-6:
            raise ValueError(
                f"context_window_breakdown_percentages must sum to 100 (got {total})"
            )
        # Always-on stores, each {id, budget_pct_of_cognition} — validated so the
        # sum fits the cognition window (§3.2 review note).
        self._always_on_stores: Dict[str, float] = {}

    # ── Builders ───────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, breakdown: Optional[dict]) -> "ContextWindow":
        if not breakdown:
            return cls()
        return cls(
            cognition_window=breakdown.get("cognition_window"),
            attention_window=breakdown.get("attention_window"),
            response_window=breakdown.get("response_window"),
        )

    # ── Budget resolution ──────────────────────────────────────────────────

    def resolve(self, max_tokens: int) -> Dict[str, int]:
        """Return {window: token_budget} for a model with ``max_tokens`` context."""
        return {
            "cognition_window": int(self.cognition_window / 100.0 * max_tokens),
            "attention_window": int(self.attention_window / 100.0 * max_tokens),
            "response_window": int(self.response_window / 100.0 * max_tokens),
        }

    def response_budget(self, max_tokens: int) -> int:
        return int(self.response_window / 100.0 * max_tokens)

    # ── Always-on stores ───────────────────────────────────────────────────

    def register_always_on_store(self, store_id: str, budget_pct_of_cognition: float) -> None:
        self._always_on_stores[store_id] = budget_pct_of_cognition
        total = sum(self._always_on_stores.values())
        if total > 100.0:
            raise ValueError(
                f"always_use_in_cognition_window budget sum {total} > 100% of the "
                f"cognition window; adjust cognition_window_budget_percentage values"
            )

    def always_on_store_tokens(self, store_id: str, max_tokens: int) -> int:
        pct = self._always_on_stores.get(store_id, 0.0)
        cog_budget = self.resolve(max_tokens)["cognition_window"]
        return int(pct / 100.0 * cog_budget)

    # ── Trim / compaction signals ──────────────────────────────────────────

    @staticmethod
    def trim(text: str, budget_tokens: int) -> str:
        """Truncate *text* so ``count_tokens(result) ≤ budget_tokens``."""
        if not text:
            return text
        if count_tokens(text) <= budget_tokens:
            return text
        # char/4 heuristic → trim to ~4×budget chars, preserving a suffix marker.
        budget_chars = budget_tokens * 4
        return text[: budget_chars // 2] + "\n…[trimmed to fit window]…\n" + text[-budget_chars // 2:]

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return (
            f"ContextWindow(cognition={self.cognition_window}, "
            f"attention={self.attention_window}, response={self.response_window})"
        )
