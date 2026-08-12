"""memory/RawLog — append-only iteration_logging (L1, the single source of truth).

Every finished block is appended as one JSON line to ``iteration_*.jsonl`` (one
file per iteration). The log is **append-only, never rewritten**; a
``block_id → byte-offset`` map gives O(1) fetch. Read back via ``JsonlQueryTool``.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class RawLog:
    def __init__(self, base_folder: str, *, enabled: bool = True) -> None:
        self._dir = os.path.join(base_folder, "iteration_logging")
        self.enabled = enabled
        self._offsets: Dict[str, int] = {}
        self._current_file: Optional[str] = None
        if enabled:
            os.makedirs(self._dir, exist_ok=True)

    def _next_file(self) -> str:
        n = len([f for f in os.listdir(self._dir) if f.endswith(".jsonl")]) if os.path.isdir(self._dir) else 0
        return os.path.join(self._dir, f"iteration_{n + 1:03d}.jsonl")

    def append(self, block: Dict[str, Any]) -> str:
        """Append a block; returns its ``block_id``. Never rewrites history."""
        block_id = str(uuid.uuid4())
        record = {
            "block_id": block_id,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            **block,
        }
        if not self.enabled:
            return block_id
        if self._current_file is None:
            self._current_file = self._next_file()
        line = json.dumps(record, ensure_ascii=False) + "\n"
        offset = os.path.getsize(self._current_file) if os.path.exists(self._current_file) else 0
        with open(self._current_file, "a", encoding="utf-8") as fh:
            fh.write(line)
        self._offsets[block_id] = offset
        return block_id

    def fetch(self, block_id: str) -> Optional[Dict[str, Any]]:
        """O(1) fetch of a block by id via the offset map (Phase 1: real seek)."""
        offset = self._offsets.get(block_id)
        if offset is None or self._current_file is None:
            return None
        with open(self._current_file, "r", encoding="utf-8") as fh:
            fh.seek(offset)
            line = fh.readline()
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None

    @property
    def file(self) -> Optional[str]:
        return self._current_file
