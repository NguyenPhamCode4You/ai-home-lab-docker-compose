"""ParallelExecutor — bounded fan-out for subprocess steps.

Runs delegate fan-out, independent tool calls, per-store distillation, and DB
upserts sequentially (``parallel_subprocesses=1``) or in a bounded pool (>1).
"""
from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, List, TypeVar

T = TypeVar("T")


class ParallelExecutor:
    def __init__(self, max_workers: int = 1) -> None:
        self.max_workers = max(1, max_workers)

    async def map(self, fn: Callable[[Any], Awaitable[T]], items: List[Any]) -> List[T]:
        """Apply async *fn* to each *item*, bounded by ``max_workers``."""
        if self.max_workers == 1 or len(items) <= 1:
            out = []
            for item in items:
                out.append(await fn(item))
            return out
        sem = asyncio.Semaphore(self.max_workers)

        async def _worker(item: Any) -> T:
            async with sem:
                return await fn(item)

        return await asyncio.gather(*(_worker(item) for item in items))