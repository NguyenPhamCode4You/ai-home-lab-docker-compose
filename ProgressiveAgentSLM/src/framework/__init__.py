# src/framework — ProgressiveAgentSLM framework package

"""ProgressiveAgentSLM framework.

The single recursive agent class, configured by one object (JSON or Python).
Local/SLM-first: the discipline (hooks, budgets, deny-lists, redaction) lives
in deterministic code; the trained model only supplies reasoning.
"""

from .AgentConfig import AgentConfig
from .BehaviorPolicies import BehaviorPolicies
from .CircularRounds import CircularRounds
from .ContextWindow import ContextWindow
from .ModelChain import ModelChain
from .ParallelExecutor import ParallelExecutor
from .ToolRegistry import Tool, ToolRegistry
from .bounded_io import read_bounded, read_bounded_or_default
from .tokens import count_tokens, set_tokenizer

__all__ = [
    "AgentConfig",
    "BehaviorPolicies",
    "CircularRounds",
    "ContextWindow",
    "ModelChain",
    "ParallelExecutor",
    "Tool",
    "ToolRegistry",
    "read_bounded",
    "read_bounded_or_default",
    "count_tokens",
    "set_tokenizer",
]
