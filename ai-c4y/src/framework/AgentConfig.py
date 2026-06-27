"""AgentConfig — configuration dataclass for ProgressiveAgentSLM."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ReflectionConfig:
    enabled: bool = True
    every_step: bool = True
    persist_to_kb: Optional[str] = None  # name of knowledge source to write durable facts to


@dataclass
class AgentConfig:
    goal: str = ""
    knowledge: List[Any] = field(default_factory=list)        # KnowledgeProvider instances
    tools: List[Any] = field(default_factory=list)            # Tool instances
    sub_agents: Dict[str, Any] = field(default_factory=dict)  # name → {agent, description, context_awareness}
    reflection: ReflectionConfig = field(default_factory=ReflectionConfig)
    model_registry: Optional[Any] = None   # ModelRegistry instance; None → use default
    max_steps: int = 6
    max_react_iters: int = 3
    compact_threshold_tokens: int = 24000
    runs_dir: str = "runs"
