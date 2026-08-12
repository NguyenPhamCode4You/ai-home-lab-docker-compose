"""Planner — decomposes a goal into a sub-task DAG.

Uses the *reasoning* role model (strong, local qwen or cloud).

Output JSON schema::

    {
      "steps": [
        {
          "id":          "unique-step-id",
          "description": "What this step does",
          "assignee":    "self | agent:NAME | tool:NAME | knowledge:NAME",
          "depends_on":  [],
          "done_when":   "brief completion criterion"
        }
      ]
    }

The Planner is called when no static plan is provided in AgentConfig.
For simple routing (Phase 1) the Forwarder handles it; Planner is
wired into the full DAG execution path in Phase 2 (StepExecutor).
"""
from __future__ import annotations

import os

from ...agents.Task import Task
from ...agents.models.Ollama import Ollama


class Planner(Task):
    """
    Decomposes a user goal into a dependency-ordered sequence of sub-tasks.

    *context* = delegate descriptions (agents + tools + knowledge).
    *question* = the user goal.
    """

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("task_name", "planner")
        kwargs.setdefault(
            "llm_model",
            Ollama(model=os.getenv("FRAMEWORK_REASONING_MODEL", "qwen3.6:27b")),
        )
        kwargs.setdefault(
            "instruction_template",
            """You are a planning agent. Decompose the user's goal into a concrete sequence of \
sub-tasks that can be delegated to the available delegates.

Available delegates:
-----
{context}
-----

User goal: {question}

Think through the necessary steps, then output ONLY a JSON plan at the very end.

```json
{{
  "steps": [
    {{
      "id": "step-1",
      "description": "What this step does",
      "assignee": "self | agent:NAME | tool:NAME | knowledge:NAME",
      "depends_on": [],
      "done_when": "brief criterion for completion"
    }}
  ]
}}
```

Rules:
- Use "self" for steps the orchestrator handles directly.
- Assignee names MUST match the available delegates exactly (prefix with agent:/tool:/knowledge:).
- Keep the plan to the minimum necessary steps.
- Always end your response with the ```json block.
""",
        )
        super().__init__(**kwargs)
