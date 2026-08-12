"""memory/Distiller — L1 → L2/L3 promoter (cheap-first).

Runs each store's ``distill_from`` → ``distill_prompt`` into structured records
via KeywordExtractor / SimpleEntityExtractor + a ladder model (cheap-first:
deterministic extraction seeds the record; the LLM runs the summary only when
needed). Redacts on egress; the curator marks stale/archived (never hard-deletes).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..redact import redact_sensitive_text
from .MemoryStore import MemoryStore


class Distiller:
    def __init__(self, stores: List[MemoryStore]) -> None:
        self._stores = stores

    def _extract_keywords(self, text: str) -> List[str]:
        """Cheap-first: deterministic keyword seed (no LLM yet)."""
        import re

        tokens = re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", text.lower())
        stop = {"the", "and", "for", "with", "this", "that", "from", "into", "are", "you"}
        return list(dict.fromkeys(t for t in tokens if t not in stop))[:8]

    def distil_block(self, block: Dict[str, Any]) -> List[Optional[str]]:
        """Distil one block into every store that lists its hook in distill_from."""
        if not block:
            return []
        # Redact on egress to any other model.
        safe_content = redact_sensitive_text(str(block.get("content", "")))
        # cheap-first keywords
        keywords = self._extract_keywords(safe_content)
        ids = []
        for store in self._stores:
            if store.pre_built:
                continue  # never self-mutate pre-built stores
            if any(h == block.get("phase") for h in store.distill_from):
                ids.append(store.distil({"content": safe_content, "keywords": keywords}))
        return ids