"""memory/RunLogger — owns the base_folder_path run tree + single serialized writer.

Emits terminal + per-block events through the run's single writer so records stay
ordered and parallel delegates never interleave.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict

from .RawLog import RawLog

logger = logging.getLogger(__name__)


class RunLogger:
    def __init__(self, base_folder: str, *, iteration_logging_enabled: bool = False) -> None:
        self._base = base_folder
        os.makedirs(base_folder, exist_ok=True)
        self.raw_log = RawLog(base_folder, enabled=iteration_logging_enabled)

    def log_block(self, block: Dict[str, Any]) -> str:
        """Append a finished block to the raw log (single writer path)."""
        block_id = self.raw_log.append(block)
        logger.info("[runlog] %s %s", block.get("actor", "?"), block_id[:8])
        return block_id

    def note(self, message: str) -> None:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        logger.info("[runlog] %s %s", ts, message)