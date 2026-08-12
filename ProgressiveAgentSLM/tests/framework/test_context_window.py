"""ContextWindow unit tests — three-window percentage budget (§3)."""
from __future__ import annotations

import pytest

from src.framework.ContextWindow import ContextWindow


def test_defaults_sum_to_100():
    cw = ContextWindow()
    assert cw.cognition_window == 32.5
    assert cw.attention_window == 52.5
    assert cw.response_window == 15.0
    assert abs(cw.cognition_window + cw.attention_window + cw.response_window - 100.0) < 1e-6


def test_rejects_non_100_sum():
    with pytest.raises(ValueError):
        ContextWindow(cognition_window=50, attention_window=50, response_window=10)


def test_resolve_budgets_for_gpt_oss():
    cw = ContextWindow.from_config({"cognition_window": 32.5, "attention_window": 52.5, "response_window": 15.0})
    b = cw.resolve(62_000)
    assert b["cognition_window"] == 20_150
    assert b["attention_window"] == 32_550
    assert b["response_window"] == 9_300


def test_response_budget():
    cw = ContextWindow.from_config({"cognition_window": 50, "attention_window": 30, "response_window": 20})
    assert cw.response_budget(10_000) == 2_000


def test_always_on_store_budget_sum_guard():
    cw = ContextWindow.from_config({"cognition_window": 50, "attention_window": 30, "response_window": 20})
    cw.register_always_on_store("a", 60)
    with pytest.raises(ValueError):
        cw.register_always_on_store("b", 50)  # 60 + 50 > 100


def test_trim_respects_budget():
    cw = ContextWindow.from_config({"cognition_window": 50, "attention_window": 30, "response_window": 20})
    trimmed = cw.trim("a" * 10_000, budget_tokens=100)
    assert len(trimmed) < 10_000
