"""memory/MemoryStore — a single memory_data_store (SQLite / sqlite-vec).

Distils a block via ``distill_prompt`` into a structured record + embed, and
queries via ``SqliteVectorQueryTool``. A store with an **empty ``distill_from``**
is a **pre-built** external knowledge base (filled once by the extraction
pipeline, never self-mutated); a populated one is **self-cultivated** at runtime.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class MemoryStore:
    def __init__(self, cfg: Dict[str, Any], base_folder: str) -> None:
        self.id: str = cfg["id"]
        self.type: str = cfg.get("type", "sqlite")
        self.distill_from: List[str] = list(cfg.get("distill_from", []) or [])
        self.distill_prompt: Optional[str] = cfg.get("distill_prompt")
        raw_path: str = cfg.get("path", "")
        self.path: str = raw_path.replace("[base_folder_path]", base_folder)
        self.table: str = cfg.get("table", self.id)
        self.retrieval_tool: str = cfg.get("retrieval_tool", "SqliteVectorQueryTool")
        self.when: str = cfg.get("when", "")
        self.always_use_in_cognition_window: bool = bool(cfg.get("always_use_in_cognition_window", False))
        self.cognition_window_budget_percentage: float = float(cfg.get("cognition_window_budget_percentage", 0.0) or 0.0)

    @property
    def pre_built(self) -> bool:
        """Empty ``distill_from`` → pre-built external KB, never self-mutated."""
        return not self.distill_from

    def distil(self, block: Dict[str, Any]) -> Optional[str]:
        """Phase 2: cheap-first extract + embed + upsert. Stub returns None."""
        if self.pre_built:
            return None  # pre-built stores are never self-mutated
        return None

    def query(self, question: str, k: int = 10) -> List[Dict[str, Any]]:
        """Phase 1/2: real sqlite-vec query. Stub returns empty."""
        return []
