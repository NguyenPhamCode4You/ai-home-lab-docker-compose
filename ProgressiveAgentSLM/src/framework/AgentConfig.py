"""AgentConfig — parsed configuration for one ProgressiveAgentSLM.

Parses every §2 field with documented defaults, and applies parent→delegate
inheritance for the fields that are inherited (`models_ladder`, `model_selection`,
`max_retries_until_switching_models`, `working_directories`,
`parallel_subprocesses`, `behavior_policies_max_circular_rounds`). Per-agent
fields (`context_window_breakdown_percentages`, `system_prompt`,
`behavior_policies`, `tools`, `memory_data_stores`) are **not** inherited.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentConfig:
    # Identity
    id: str = ""
    description: str = ""
    system_prompt: Optional[str] = None

    # Storage
    base_folder_path: Optional[str] = None  # defaults to id
    iteration_logging_enabled: bool = False
    iteration_logging: Optional[dict] = None  # {type, path, retrieval_tool, when}

    # Models
    model_selection: str = "auto"
    models_ladder: List[dict] = field(default_factory=list)
    max_retries_until_switching_models: int = 5

    # Context budget (percentages, sum = 100)
    context_window_breakdown_percentages: Dict[str, float] = field(default_factory=dict)

    # Behavior policies
    circular_behavior_policies_allowed: bool = False
    behavior_policies_max_circular_rounds: int = 5
    behavior_policies: List[dict] = field(default_factory=list)

    # Working dirs / tools / memory / parallelism
    working_directories: List[dict] = field(default_factory=list)
    tools: List[dict] = field(default_factory=list)
    memory_data_stores: List[dict] = field(default_factory=list)
    parallel_subprocesses: int = 1

    # Modes (assistant / research / reflection)
    run_mode: str = "assistant"
    api_configuration: Optional[dict] = None
    communication_channels: Optional[dict] = None
    research_configuration: Optional[dict] = None
    reflection_configuration: Optional[dict] = None
    self_evaluation_quizz: Optional[dict] = None

    # Recursion
    delegates: List["AgentConfig"] = field(default_factory=list)

    # ── Derived helpers ────────────────────────────────────────────────────

    @property
    def folder(self) -> str:
        return self.base_folder_path or self.id or "agent"

    def window_sum(self) -> float:
        b = self.context_window_breakdown_percentages
        return sum(b.get(k, 0.0) for k in ("cognition_window", "attention_window", "response_window"))

    def validate(self) -> None:
        """Raise ValueError on an invalid config (loader-time guard)."""
        if not self.id:
            raise ValueError("AgentConfig requires an `id`")
        if not self.description:
            raise ValueError(f"AgentConfig {self.id!r} requires a `description`")
        if self.window_sum() and abs(self.window_sum() - 100.0) > 1e-6:
            raise ValueError(
                f"AgentConfig {self.id!r}: context_window_breakdown_percentages must sum to 100 "
                f"(got {self.window_sum()})"
            )

    # ── Inheritance ────────────────────────────────────────────────────────

    def inherit_from(self, parent: "AgentConfig") -> None:
        """Fill inherited fields from *parent* where this agent omitted them."""
        if not self.models_ladder:
            self.models_ladder = list(parent.models_ladder)
        if self.model_selection in (None, "", "auto") and parent.model_selection:
            self.model_selection = parent.model_selection
        # model_selection is allowed to stay "auto" even when parent differs
        if not self.max_retries_until_switching_models:
            self.max_retries_until_switching_models = parent.max_retries_until_switching_models
        if not self.working_directories:
            self.working_directories = list(parent.working_directories)
        if not self.parallel_subprocesses:
            self.parallel_subprocesses = parent.parallel_subprocesses
        if not self.behavior_policies_max_circular_rounds:
            self.behavior_policies_max_circular_rounds = parent.behavior_policies_max_circular_rounds
        # Nest this delegate's tree under the parent's base_folder_path when
        # the config uses the [base_folder_path] placeholder or is unset.
        if self.base_folder_path is None or self.base_folder_path.startswith("[base_folder_path]"):
            parent_folder = parent.folder
            suffix = self.id if self.base_folder_path is None else self.base_folder_path.replace("[base_folder_path]", parent_folder)
            self.base_folder_path = f"{parent_folder}/{suffix}" if self.base_folder_path is None else suffix
