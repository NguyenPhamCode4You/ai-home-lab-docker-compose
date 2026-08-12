"""agents/Reflector — progressive compaction engine (pluggable lifecycle).

Pattern ported/adapted from Hermes ``context_engine.py`` (MIT): a pluggable
engine with ``should_compress()`` / ``compress()`` lifecycle, not a hardcoded
50% call site. Compacts the working set **adaptively** (only enough to fit),
protecting head + tail and **updating** the prior summary (iterative,
goal-tracking). The raw log + stores stay intact (recoverable).
"""
from __future__ import annotations

from typing import Optional

from ..tokens import count_tokens


class Reflector:
    """Pluggable context-engine for the working set."""

    name = "reflector"

    # Token state (read by the loop for display / preflight).
    last_prompt_tokens: int = 0
    last_total_tokens: int = 0
    compression_count: int = 0
    context_length: int = 0

    def should_compress(self, working_tokens: int, budget_tokens: int) -> bool:
        return working_tokens > budget_tokens

    def compress(self, working: str, budget_tokens: int) -> str:
        """Adaptively shrink *working* until it fits ``budget_tokens``.

        Phase 1/2: real iterative goal-tracking summarization (reuse
        ``KnowledgeCompression`` / ``IterationSummarizer``). Stub: head + taill
        preserved, middle dropped to fit.
        """
        if not working or count_tokens(working) <= budget_tokens:
            return working
        ratio = budget_tokens / max(1, count_tokens(working))
        head = working[: int(len(working) * ratio / 2)]
        tail = working[-int(len(working) * ratio / 2):]
        result = head + "\n…[compacted to fit window]…\n" + tail
        self.compression_count += 1
        return result