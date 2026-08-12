"""AgentConfig unit tests — defaults + delegate inheritance (§2)."""
from __future__ import annotations

from src.framework.AgentConfig import AgentConfig


def _parent() -> AgentConfig:
    return AgentConfig(
        id="parent",
        description="parent agent",
        base_folder_path="runs/parent",
        models_ladder=[{"platform": "ollama", "name": "gpt-oss:20b", "is_general_purpose": True}],
        max_retries_until_switching_models=7,
        parallel_subprocesses=2,
        behavior_policies_max_circular_rounds=3,
        context_window_breakdown_percentages={"cognition_window": 50, "attention_window": 30, "response_window": 20},
    )


def test_requires_id_and_description():
    c = AgentConfig()
    try:
        c.validate()
        assert False, "should raise"
    except ValueError:
        pass


def test_delegate_inherits_ladder_and_budget():
    p = _parent()
    d = AgentConfig(id="child", description="child agent", base_folder_path=None)
    d.inherit_from(p)
    assert d.models_ladder == p.models_ladder
    assert d.max_retries_until_switching_models == 7
    assert d.parallel_subprocesses == 2
    assert d.behavior_policies_max_circular_rounds == 3


def test_delegate_keeps_own_windows():
    p = _parent()
    d = AgentConfig(
        id="child",
        description="child",
        base_folder_path=None,
        context_window_breakdown_percentages={"cognition_window": 40, "attention_window": 40, "response_window": 20},
    )
    d.inherit_from(p)
    assert d.window_sum() == 100.0
    assert d.context_window_breakdown_percentages != p.context_window_breakdown_percentages


def test_nest_base_folder_under_parent():
    p = _parent()
    d = AgentConfig(id="child", description="child", base_folder_path=None)
    d.inherit_from(p)
    assert d.folder.startswith(p.folder)
    assert "child" in d.folder