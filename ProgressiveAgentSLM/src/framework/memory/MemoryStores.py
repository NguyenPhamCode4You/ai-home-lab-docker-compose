"""memory/MemoryStores — coordinator over the store DAG.

Orders stores by ``distill_from`` (topological), resolves
``always_use_in_cognition_window`` injection, and serves on-demand retrieval for
the rest. Phase 1 wires real sqlite-vec store opening; the stub keeps the
coordinator importable and the tree buildable.
"""
from __future__ import annotations

from typing import Any, Dict, List

from .MemoryStore import MemoryStore


class MemoryStores:
    def __init__(self, store_configs: List[Dict[str, Any]], base_folder: str) -> None:
        self._stores: Dict[str, MemoryStore] = {
            cfg["id"]: MemoryStore(cfg, base_folder) for cfg in store_configs
        }

    def get(self, store_id: str) -> MemoryStore:
        return self._stores[store_id]

    def all(self) -> List[MemoryStore]:
        return list(self._stores.values())

    def always_on(self) -> List[MemoryStore]:
        return [s for s in self._stores.values() if s.always_use_in_cognition_window]

    def ordered_by_dependency(self) -> List[MemoryStore]:
        # Phase 2: true topological sort over distill_from. Stub: config order.
        return self.all()

    def retrieve(self, question: str, k: int = 10) -> Dict[str, List[Any]]:
        return {s.id: s.query(question, k) for s in self._stores.values() if not s.always_use_in_cognition_window}