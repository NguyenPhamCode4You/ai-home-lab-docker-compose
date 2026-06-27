"""VectorSearchTool — searches a Supabase vector store for relevant context.

Wraps SupabaseVectorStore.async_get_documents_string() so it can be used
as a first-class delegate in the ProgressiveAgentSLM routing loop.
"""
from __future__ import annotations

from ..ToolRegistry import Tool


class VectorSearchTool(Tool):
    """
    Semantic search over a Supabase pgvector table.

    Args:
        vector_store:  SupabaseVectorStore instance (with async methods).
        function_name: Supabase RPC function name (e.g. "match_n8n_documents_bvms_neo").
        match_count:   Max documents to retrieve.
        name:          Override tool name (default "vector_search").
        description:   Override description shown to the Forwarder.
    """

    def __init__(
        self,
        vector_store,
        function_name: str,
        match_count: int = 10,
        name: str = None,
        description: str = None,
    ) -> None:
        self.name = name or "vector_search"
        self.description = description or (
            "Search the knowledge base for relevant domain context. "
            "Use for questions requiring background knowledge."
        )
        self._store = vector_store
        self._function_name = function_name
        self._match_count = match_count

    async def run(
        self,
        question: str,
        context: str = None,
        conversation_history: list = None,
    ) -> str:
        result = await self._store.async_get_documents_string(
            self._function_name, question, self._match_count
        )
        if not result or not result.strip():
            return "⚠️ VectorSearchTool: no results found."
        return result
