"""memory/LogSearch — SQLite FTS5 index over iteration_*.jsonl.

Pattern ported/adapted from Hermes ``hermes_state_search.py`` (MIT): trigram +
CJK tokenizer, incremental bounded merge, query char caps, resumable rebuild.
Phase 1/2 wires the actual FTS5 table; stub keeps the CLI importable.
"""
from __future__ import annotations

import glob
import os
import sqlite3
from typing import List

MAX_FTS5_QUERY_CHARS = 200


class LogSearch:
    def __init__(self, base_folder: str) -> None:
        self._db_path = os.path.join(base_folder, "log_index.db")
        self._conn = sqlite3.connect(self._db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        # Trigram tokenizer for substring / CJK (Phase 1: full DDL).
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS fts_blocks(
                block_id TEXT,
                iteration TEXT,
                actor TEXT,
                content TEXT
            )
            """
        )
        self._conn.commit()

    def index_file(self, path: str) -> int:
        """Index one iteration_*.jsonl file. Phase 1: real FTS insert + merge."""
        if not os.path.exists(path):
            return 0
        with open(path, "r", encoding="utf-8") as fh:
            lines = [ln for ln in fh if ln.strip()]
        cur = self._conn.cursor()
        for ln in lines:
            import json as _j

            try:
                rec = _j.loads(ln)
            except _j.JSONDecodeError:
                continue
            cur.execute(
                "INSERT OR REPLACE INTO fts_blocks VALUES (?,?,?,?)",
                (rec.get("block_id", ""), rec.get("iteration", ""), rec.get("actor", ""), rec.get("content", "")),
            )
        self._conn.commit()
        return len(lines)

    def search(self, query: str) -> List[dict]:
        """LIKE-based stub search (Phase 1: real FTS5 MATCH)."""
        if len(query) > MAX_FTS5_QUERY_CHARS:
            query = query[:MAX_FTS5_QUERY_CHARS]
        cur = self._conn.cursor()
        cur.execute(
            "SELECT block_id, iteration, actor, content FROM fts_blocks WHERE content LIKE ? LIMIT 20",
            (f"%{query}%",),
        )
        return [dict(zip(("block_id", "iteration", "actor", "content"), row)) for row in cur.fetchall()]

    def index_all(self, log_dir: str) -> int:
        total = 0
        for f in sorted(glob.glob(os.path.join(log_dir, "iteration_*.jsonl"))):
            total += self.index_file(f)
        return total