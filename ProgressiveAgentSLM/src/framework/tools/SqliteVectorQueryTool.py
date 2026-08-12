"""SqliteVectorQueryTool — primary embedded vector search (sqlite-vec).

Queries a local `.db` file's vector table via ``SqliteVectorStore.async_query``
(path + table). The `retrieval_tool` for every ``memory_data_store``. Optional
parallel ``DocumentRanking`` when ``ranking`` is set.
"""
from __future__ import annotations

from typing import Any, Optional

from ..ToolRegistry import Tool


class SqliteVectorQueryTool(Tool):
    name = "sqlite_vector_query"
    description = (
        "Semantic search over a distilled knowledge store. "
        "Returns the most relevant chunks for a question."
    )

    def __init__(self, path: str = "", table: str = "", ranking: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = path
        self.table = table
        self.ranking = ranking

    async def run(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> str:
        if not self.path or not self.table:
            return "❌ SqliteVectorQueryTool: path/table not bound (loader should bind them)."
        # Phase 1: drive SqliteVectorStore.async_query here. Stub result.
        return (
            f"🔎 SqliteVectorQueryTool[{self.table}] query={question!r} → "
            "(Phase 1: real sqlite-vec retrieval lands here)"
        )