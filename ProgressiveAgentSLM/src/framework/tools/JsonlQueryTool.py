"""JsonlQueryTool — the retrieval_tool for iteration_logging.

Queries the raw ``iteration_*.jsonl`` log for previous reasoning / intermediate
results (debug or trace a current problem). Read-only.
"""
from __future__ import annotations

import glob
import json

from ..ToolRegistry import Tool


class JsonlQueryTool(Tool):
    name = "jsonl_query"
    description = (
        "Query the iteration log (iteration_*.jsonl) for the agent's previous "
        "reasoning or intermediate results."
    )

    def __init__(self, path: str = "iteration_logging/iteration_*.jsonl", **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = path
        # Resolve the [base_folder_path] placeholder when bound by the loader.
        self.path = self.path.replace("[base_folder_path]/", "") if self.path.startswith("[base_folder_path]") else self.path

    async def run(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> str:
        files = sorted(glob.glob(self.path))
        if not files:
            return f"❌ JsonlQueryTool: no iteration logs at {self.path!r}"
        # Phase 1: real scoped querying. Stub returns the last file's lines.
        with open(files[-1], "r", encoding="utf-8") as fh:
            lines = [json.loads(line) for line in fh if line.strip()]
        return "\n".join(str(r.get("content", "")) for r in lines[-5:])