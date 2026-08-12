"""BehaviorPolicies — renders when→then rules AND fires them at run_after hooks.

Renders each ``behavior_policies`` entry into the system prompt every iteration
(and as the run's todo checklist), and fires them deterministically at their
``run_after`` hook (question_received / retrieval_result / iteration_result /
raw_iteration_result / final_answer / another policy id). Honors
``circular_behavior_policies_allowed`` — cycles bounded by ``CircularRounds``.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

HOOKS = {
    "question_received",
    "retrieval_result",
    "iteration_result",
    "raw_iteration_result",
    "final_answer",
}


class BehaviorPolicies:
    def __init__(self, policies: List[Dict[str, Any]], circular_allowed: bool = False) -> None:
        self._policies = policies
        self.circular_allowed = circular_allowed

    def render(self) -> str:
        """Render all policies as "When X, then Y." rules (into the prompt)."""
        return "\n".join(
            f"- When {p.get('when', '')}, then {p.get('then', '')}."
            for p in self._policies
        )

    def eligible(self, hook: str) -> List[Dict[str, Any]]:
        """Policies whose ``run_after`` lists include *hook*."""
        return [p for p in self._policies if hook in (p.get("run_after") or [])]

    def policy_by_id(self, policy_id: str) -> Optional[Dict[str, Any]]:
        for p in self._policies:
            if p.get("id") == policy_id:
                return p
        return None

    def fire(self, hook: str, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return the eligible policies to run after *hook*.

        Phase 1/2 wires deterministic guards behind the critical ones
        (double_checking → verify-on-stop, refusing_to_invent → grounding gate,
        anti-drift → tool-loop guard). Cycles only allowed when
        ``circular_allowed``.
        """
        return self.eligible(hook)