"""ReadFileTool — reads a file from disk, traversal-safe + deny-listed.

Paths resolve under the run's ``base_folder_path`` and any ``working_directories``
root; ``..`` / absolute escapes and the sensitive-path deny-list are rejected
(OWASP A01/A03 + §10).
"""
from __future__ import annotations

import re

from ..ToolRegistry import Tool
from .safety import PathSafety


class ReadFileTool(Tool):
    name = "read_file"
    description = (
        "Read the contents of a local file given its path. "
        "Sub-question should mention the file path, e.g. 'read src/foo.py'."
    )

    def __init__(self, roots=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._safety = PathSafety(roots or ["."])

    async def run(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> str:
        raw = self._extract_path(question)
        if not raw:
            return f"❌ ReadFileTool: could not find a file path in: {question!r}"
        resolved = self._safety.resolve(raw)
        if resolved is None:
            return f"❌ ReadFileTool: path not allowed (traversal or deny-list): {raw!r}"
        try:
            with open(resolved, "r", encoding="utf-8") as fh:
                content = fh.read()
            return f"📄 **{resolved}**\n\n```\n{content}\n```\n"
        except FileNotFoundError:
            return f"❌ ReadFileTool: file not found: {resolved!r}"
        except Exception as exc:  # noqa: BLE001
            return f"❌ ReadFileTool: {exc}"

    @staticmethod
    def _extract_path(text: str) -> str | None:
        # Quoted path first
        m = re.search(r'["\']([^"\']+)["\']', text)
        if m:
            return m.group(1)
        # Bare path-like token (contains / or \\ and a dot extension)
        m = re.search(r'[\w./\\-]+\.\w+', text)
        if m:
            return m.group(0)
        return None
