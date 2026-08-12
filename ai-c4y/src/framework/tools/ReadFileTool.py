"""ReadFileTool — reads a file from disk and returns its contents.

The delegate question is scanned for a file path (quoted or bare token).
"""
from __future__ import annotations

import os
import re

from ..ToolRegistry import Tool


class ReadFileTool(Tool):
    name = "read_file"
    description = (
        "Read the contents of a local file given its path. "
        "Sub-question should mention the file path, e.g. 'read src/foo.py'."
    )

    async def run(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> str:
        path = self._extract_path(question)
        if not path:
            return f"❌ ReadFileTool: could not find a file path in: {question!r}"
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            return f"📄 **{path}**\n\n```\n{content}\n```\n"
        except FileNotFoundError:
            return f"❌ ReadFileTool: file not found: {path!r}"
        except Exception as exc:
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
