"""ModelChain unit tests — ladder selection + failover + success reset (§4)."""
from __future__ import annotations

from src.framework.ModelChain import ModelChain

LADDER = [
    {"platform": "ollama", "name": "gpt-oss:20b", "is_general_purpose": True, "max_tokens": 62000},
    {"platform": "ollama", "name": "qwen3.6:27b", "is_general_purpose": True, "is_fallback": True, "max_tokens": 128000},
]


def test_auto_selects_first_general_purpose():
    chain = ModelChain(LADDER, model_selection="auto", max_retries_until_switching_models=5)
    entry = chain.select("general")
    assert entry.name == "gpt-oss:20b"


def test_pinned_selection():
    chain = ModelChain(LADDER, model_selection="qwen3.6:27b", max_retries_until_switching_models=5)
    entry = chain.select("general")
    assert entry.name == "qwen3.6:27b"


def test_failover_after_budget():
    chain = ModelChain(LADDER, model_selection="auto", max_retries_until_switching_models=2)
    chain.select("general")
    assert chain.current().name == "gpt-oss:20b"
    chain.record_failure()
    chain.record_failure()
    assert chain.current().name == "qwen3.6:27b"  # advanced after 2 failures


def test_success_resets_to_top():
    chain = ModelChain(LADDER, model_selection="auto", max_retries_until_switching_models=1)
    chain.select("general")
    chain.record_failure()
    assert chain.current().name == "qwen3.6:27b"
    chain.record_success()
    chain.select("general")
    assert chain.current().name == "gpt-oss:20b"


def test_quality_and_infra_share_one_counter():
    chain = ModelChain(LADDER, model_selection="auto", max_retries_until_switching_models=3)
    chain.select("general")
    chain.record_failure()  # infra
    chain.record_failure()  # quality
    assert chain.current().name == "gpt-oss:20b"
    chain.record_failure()  # 3rd → switch
    assert chain.current().name == "qwen3.6:27b"


def test_ladder_exhaustion_returns_true():
    chain = ModelChain(LADDER, model_selection="auto", max_retries_until_switching_models=1)
    chain.select("general")
    chain.record_failure()
    # Now on last; a failure spends it → exhausted.
    assert chain.record_failure() is True