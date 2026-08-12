"""TodoTool — maintains the run's checklist (anti-drift).

The model **rewrites the whole list** `[{id, content, status}]` into
``[base_folder_path]/todo.md``; the loop re-injects it each iteration.
"""
from __future__ import annotations

import json
import os
import re

from ..ToolRegistry import Tool

_ALLOWED_STATUS = {"pending", "in_progress", "completed"}


class TodoTool(Tool):
    name = "todo"
    description = (
        "Maintain the run's todo checklist. "
        "Rewrites the whole list [{id, content, status: pending|in_progress|completed}] "
        "into todo.md. Use at the start of multi-step tasks and when the plan changes."
    )

    def __init__(self, todo_path: str = "todo.md", **kwargs) -> None:
        super().__init__(**kwargs)
        self.todo_path = todo_path

    async def run(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> str:
        items = self._parse(question)
        if items is None:
            return f"❌ TodoTool: no valid todo JSON list found in: {question!r}"
        try:
            os.makedirs(os.path.dirname(self.todo_path) or ".", exist_ok=True)
            with open(self.todo_path, "w", encoding="utf-8") as fh:
                json.dump(items, fh, indent=2)
            return f"✅ Todo list written to {self.todo_path}: {len(items)} items."
        except Exception as exc:  # noqa: BLE001
            return f"❌ TodoTool: {exc}"

    @staticmethod
    def _parse(text: str):
        """Extract a JSON list of {id, content, status}; return None if malformed."""
        m = re.search(r"\[[\s\S]*\]", text)
        if not m:
            return None
        try:
            items = json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
        if not isinstance(items, list):
            return None
        for it in items:
            if not isinstance(it, dict) or "id" not in it or "content" not in it:
                return None
            if it.get("status", "pending") not in _ALLOWED_STATUS:
                return None
        return items
