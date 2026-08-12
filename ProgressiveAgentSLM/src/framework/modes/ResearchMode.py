"""modes/ResearchMode — run_mode=research autonomous loop.

Iterates over ``research_configuration.topics`` / ``goals``; stops on the first
active condition (goals / time / iterations, OR-combined); invokes
``SelfEvaluationQuizz`` after (``run_quizz_after_finish``); resumes on fail if
``resume_if_quizz_failed``. Phase 2/3 wires the loop; stub keeps it importable.
"""
from __future__ import annotations

from typing import Any, Dict, Optional


class ResearchMode:
    name = "research"

    def __init__(self, research_configuration: Optional[Dict[str, Any]] = None) -> None:
        self.config = research_configuration or {}

    def should_stop(self, *, goals_met: bool, elapsed_s: float, iterations: int) -> bool:
        stop_goals = bool(self.config.get("stop_when_goals_achieved")) and goals_met
        time_limit = self.config.get("time_limit")
        stop_time = bool(time_limit) and elapsed_s >= time_limit
        iter_limit = self.config.get("iterations_limit")
        stop_iter = bool(iter_limit) and iterations >= iter_limit
        return stop_goals or stop_time or stop_iter