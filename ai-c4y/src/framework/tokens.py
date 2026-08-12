"""tokens — lightweight token-count approximation.

Phase 1 strategy  : char-approx using CHARS_PER_TOKEN (same env var as Task.py).
Phase 2 seam      : call set_tokenizer() with a real tiktoken / HF tokenizer;
                    count_tokens() will delegate to it transparently.
"""
from __future__ import annotations

import os
from typing import Callable, Optional

# One source of truth — reads the same env var used by Task.py and docker-compose.yml
CHARS_PER_TOKEN: int = int(os.getenv("CHARS_PER_TOKEN", 3))

# Pluggable seam — None means use the char-approx default
_tokenizer: Optional[Callable[[str], int]] = None


def set_tokenizer(fn: Callable[[str], int]) -> None:
    """Replace the char-approx with a real tokenizer for Phase 2+."""
    global _tokenizer
    _tokenizer = fn


def count_tokens(text: str) -> int:
    """Return an approximate token count for *text*.

    With the default char-approx: ``len(text) // CHARS_PER_TOKEN``.
    Monotonically non-decreasing — longer text never returns fewer tokens.
    """
    if not text:
        return 0
    if _tokenizer is not None:
        return _tokenizer(text)
    return len(text) // CHARS_PER_TOKEN
