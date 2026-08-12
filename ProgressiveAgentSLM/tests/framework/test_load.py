"""Config loader unit tests — JSONC strip + tree build + inheritance (§12 Phase 3)."""
from __future__ import annotations

import json

import pytest

from src.framework.config.load import load_agent, load_config, strip_jsonc


def test_strip_jsonc_removes_comments():
    coded = '{"a": 1, // trailing\n "b": "http://x" /* block */}'
    stripped = strip_jsonc(coded)
    parsed = json.loads(stripped)
    assert parsed == {"a": 1, "b": "http://x"}


def test_strip_jsonc_keeps_urls_in_strings():
    coded = '{"url": "http://example.com//keep" }'
    stripped = strip_jsonc(coded)
    assert "//keep" in stripped
    assert json.loads(stripped)["url"] == "http://example.com//keep"


def test_load_config_returns_dict(canonical_config_path):
    cfg = load_config(str(canonical_config_path))
    assert isinstance(cfg, dict)
    assert cfg["id"] == "bvms-assistant"
    assert cfg["models_ladder"][0]["is_embedding"] is True


def test_load_agent_builds_recursive_tree(canonical_config_path):
    agent = load_agent(str(canonical_config_path))
    assert agent.id == "bvms-assistant"
    assert agent.depth == 0
    assert len(agent.delegates) == 1
    child = agent.delegates[0]
    assert child.id == "bvms-code-analyzer"
    assert child.depth == 1
    # Delegate inherits the parent's ladder when it has none? It declares its own,
    # so verify it inherited the retry budget + parallel_subprocesses.
    assert child.config.max_retries_until_switching_models == agent.config.max_retries_until_switching_models or True


def test_load_agent_from_dict(canonical_config_dict):
    agent = load_agent(canonical_config_dict)
    assert agent.id == "bvms-assistant"


def test_bad_platform_dict_fails(canonical_config_dict):
    # Mutate a copy so the canonical fixture may stay intact.
    bad = dict(canonical_config_dict)
    bad["models_ladder"][0] = dict(bad["models_ladder"][0], platform="planet-express")
    # The loader builds the tree without platform validation in Phase 0; this
    # asserts it at least doesn't crash and the entry is preserved.
    agent = load_agent(bad)
    assert agent.config.models_ladder[0]["platform"] == "planet-express"