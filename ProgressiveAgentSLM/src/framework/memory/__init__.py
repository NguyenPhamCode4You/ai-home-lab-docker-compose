# src/framework/memory — RawLog, MemoryStore, Distiller, MemoryStores, LogSearch

"""Memory subsystem (L1 → L4, §8).

- L1: `RawLog` — append-only iteration_logging (single source of truth).
- L2/L3: `MemoryStore` / `MemoryStores` — SQLite memory_data_stores.
- `Distiller` — cheap-first L1→L2/L3 promoter.
- `LogSearch` — FTS5 index over the iteration logs.
"""

from .Distiller import Distiller
from .LogSearch import LogSearch
from .MemoryStore import MemoryStore
from .MemoryStores import MemoryStores
from .RawLog import RawLog
from .RunLogger import RunLogger

__all__ = [
    "Distiller",
    "LogSearch",
    "MemoryStore",
    "MemoryStores",
    "RawLog",
    "RunLogger",
]