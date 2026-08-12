"""Reflector — rewrites and compacts the worklog after every step.

Wraps KnowledgeCompression + IterationSummarizer pattern.
Uses the *reflection* role model (gpt-oss:20b by default).

Input  (via Task.run):
  context  = current worklog content
  question = the overall user goal (anchor for relevance)

Output: revised worklog markdown (starts with "# Worklog").
"""
from __future__ import annotations

import os

from ...agents.Task import Task
from ...agents.models.Ollama import Ollama


class Reflector(Task):
    """
    Curates and compacts the shared worklog so it stays small and current.

    Called after every delegate round.  The output replaces the worklog file
    via Worklog.revise().
    """

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("task_name", "reflector")
        kwargs.setdefault(
            "llm_model",
            Ollama(model=os.getenv("FRAMEWORK_REFLECTION_MODEL", "gpt-oss:20b")),
        )
        kwargs.setdefault(
            "instruction_template",
            """You are a worklog curator for a multi-step agentic workflow.
The worklog is the shared memory that all delegates read as context.

Your job: revise and compact the worklog so it stays small, non-redundant, and current.

Rules:
- Keep all key findings, decisions, code snippets, and facts.
- Remove redundant or repetitive content.
- Preserve the markdown ## section structure.
- Do NOT invent new information — only reorganize and compress what is there.
- Return the revised worklog content ONLY (start with "# Worklog").

Overall user goal: {question}

Current worklog to revise:
{context}
""",
        )
        super().__init__(**kwargs)
