"""Forwarder — routes a question/goal to delegates (agents, tools, knowledge).

Modeled on QuestionForwarder but aware of all delegate types.
Uses the *chat* role model (fast, cheap, local).

Outputs a ```json routing block at the end, parsed by _parse_agent_routing.
"""
from __future__ import annotations

import os

from ...agents.Task import Task
from ...agents.models.Ollama import Ollama


class Forwarder(Task):
    """
    Routes a question/goal to the right delegates.

    The delegate descriptions are passed as *context*; the user question as
    *question*.  After brief reasoning the model ends with a JSON block::

        ```json
        [{"agent": "ExactDelegateName", "question": "sub-question for this delegate"}]
        ```

    An empty array ``[]`` means the forwarder answers directly (no delegation).
    """

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("task_name", "forwarder")
        kwargs.setdefault(
            "llm_model",
            Ollama(model=os.getenv("FRAMEWORK_CHAT_MODEL", "gemma4:e4b")),
        )
        kwargs.setdefault(
            "instruction_template",
            """You are an intelligent orchestrator routing a goal or question to specialist delegates \
(agents, tools, knowledge sources).

Previous conversation:
-----
{histories}
-----

Available delegates and their capabilities:
-----
{context}
-----

User goal / question: {question}

Think step-by-step about which delegate(s) should handle this.
Then output ONLY a JSON routing block at the very end of your response.

To delegate to one or more:
```json
[
  {{"agent": "ExactDelegateName", "question": "specific sub-question tailored for this delegate"}}
]
```

If you can answer directly without any delegate:
```json
[]
```

Rules:
- Names in the JSON MUST exactly match the names listed above.
- Always end your response with the ```json block.
- Keep sub-questions focused and specific.
""",
        )
        super().__init__(**kwargs)
