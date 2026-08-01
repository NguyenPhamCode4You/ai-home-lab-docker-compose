"""ContextWindow — four-tier proportional budget over the active model's max_tokens.

The budget is expressed as **fractions** of the selected model's ``max_tokens`` so
the same config scales to any model without code changes (§3).

Three fractions are declared explicitly; the remainder (1 − Σ fractions) is
automatically reserved for the answer.

Default fractions (§13a parent):
    conversation_history_awareness  = 0.025
    cognitive_reflection_behavior   = 0.325
    current_working_attention       = 0.525
    answer_remainder (implicit)     ≈ 0.125

Items 5-8 (cascade-on-zero, resolve, trim, compaction signals) are added in the
next checklist steps.
"""
from __future__ import annotations


class ContextWindow:
    """Holds the three declared tier fractions and computes the answer remainder.

    Construct directly or by unpacking a ``context_window_breakdown`` dict::

        cw = ContextWindow(**config["context_window_breakdown"])
    """

    def __init__(
        self,
        conversation_history_awareness: float = 0.025,
        cognitive_reflection_behavior: float = 0.325,
        current_working_attention: float = 0.525,
    ) -> None:
        self.conversation_history_awareness = conversation_history_awareness
        self.cognitive_reflection_behavior = cognitive_reflection_behavior
        self.current_working_attention = current_working_attention

    # ── Derived ────────────────────────────────────────────────────────────

    @property
    def answer_remainder(self) -> float:
        """Fraction of max_tokens left for the answer (1 − Σ declared fractions)."""
        return 1.0 - (
            self.conversation_history_awareness
            + self.cognitive_reflection_behavior
            + self.current_working_attention
        )

    def fractions(self) -> dict:
        """Return all four fractions as a dict (answer_remainder included)."""
        return {
            "conversation_history_awareness": self.conversation_history_awareness,
            "cognitive_reflection_behavior": self.cognitive_reflection_behavior,
            "current_working_attention": self.current_working_attention,
            "answer_remainder": self.answer_remainder,
        }

    def __repr__(self) -> str:
        return (
            f"ContextWindow("
            f"awareness={self.conversation_history_awareness}, "
            f"reflection={self.cognitive_reflection_behavior}, "
            f"attention={self.current_working_attention}, "
            f"answer≈{self.answer_remainder:.3f})"
        )
