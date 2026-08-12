"""Shared pytest fixtures for the framework test suite."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make `src` importable from the project root (tests live in tests/).
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def canonical_config_path() -> Path:
    return ROOT / "src" / "framework" / "example-revised.json"


@pytest.fixture
def canonical_config_dict():
    """The canonical config as a plain dict (JSONC stripped)."""
    import json

    from src.framework.config.load import strip_jsonc

    raw = (ROOT / "src" / "framework" / "example-revised.json").read_text(encoding="utf-8")
    return json.loads(strip_jsonc(raw))
