"""Unit tests for src/framework/tokens.py — Phase 0 Item 3."""
from __future__ import annotations

import pytest

from src.framework.tokens import CHARS_PER_TOKEN, count_tokens, set_tokenizer


class TestCountTokensCharApprox:
    def test_empty_string_returns_zero(self):
        assert count_tokens("") == 0

    def test_known_length(self):
        text = "abc" * 100  # len == 300
        expected = 300 // CHARS_PER_TOKEN
        assert count_tokens(text) == expected

    def test_approximation_matches_len_div_chars_per_token(self):
        for n in [1, 10, 50, 200]:
            text = "x" * n
            assert count_tokens(text) == len(text) // CHARS_PER_TOKEN

    def test_monotonicity(self):
        """Longer text must never produce fewer tokens."""
        lengths = [0, 1, 3, 10, 30, 100, 300, 1000]
        prev = -1
        for n in lengths:
            result = count_tokens("a" * n)
            assert result >= prev, f"monotonicity broken at len={n}: {result} < {prev}"
            prev = result


class TestPluggableTokenizer:
    def test_custom_tokenizer_is_called(self):
        called_with = []

        def fake_tokenizer(text: str) -> int:
            called_with.append(text)
            return 42

        set_tokenizer(fake_tokenizer)
        try:
            result = count_tokens("hello world")
            assert result == 42
            assert called_with == ["hello world"]
        finally:
            set_tokenizer(None)  # restore default

    def test_restoring_none_reverts_to_char_approx(self):
        set_tokenizer(lambda t: 999)
        set_tokenizer(None)
        text = "abc" * 100
        assert count_tokens(text) == len(text) // CHARS_PER_TOKEN
