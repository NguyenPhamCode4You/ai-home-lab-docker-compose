"""tokens — lightweight token-count approximation (TokenCounter).

Phase 0 strategy  : char/4 heuristic (``(len(text) + 3) // 4``), matching
                    Hermes's ``estimate_request_tokens_rough`` — one measure for
                    BOTH budget and compaction threshold so they never disagree.
Phase 2 seam      : call set_tokenizer() with a real tiktoken / HF tokenizer;
                    count_tokens() delegates to it transparently.
"""
from __future__ import annotations

import os
from typing import Callable, Optional

# Kept for backward-compat with the old flat loop; the canonical heuristic below
# is char/4 per §16 Open Q#8.
CHARS_PER_TOKEN: int = int(os.getenv("CHARS_PER_TOKEN", 3))

# Pluggable seam — None means use the char-approx default.
_tokenizer: Optional[Callable[[str], int]] = None


def set_tokenizer(fn: Callable[[str], int]) -> None:
    """Replace the char-approx with a real tokenizer for Phase 2+."""
    global _tokenizer
    _tokenizer = fn


def count_tokens(text: str) -> int:
    """Return an approximate token count for *text*.

    Default heuristic: ``(len(text) + 3) // 4`` — the same char/4 rule used for
    the compaction threshold (one measure for both; Hermes lesson, Open Q#8).
    Monotonically non-decreasing — longer text never returns fewer tokens.
    """
    if not text:
        return 0
    if _tokenizer is not None:
        return _tokenizer(text)
    return (len(text) + 3) // 4
