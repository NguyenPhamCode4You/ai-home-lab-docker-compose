"""config/load — build a ProgressiveAgentSLM tree from JSON or a Python dict.

Loads the canonical ``example-revised.json`` (which is **JSONC** — commented
JSON) by stripping comments, validates, applies delegate inheritance, and builds
the full recursive tree. ``load_agent(path_or_dict)``:
  path → read + strip JSONC → dict → build.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Union

from ..AgentConfig import AgentConfig
from ..ProgressiveAgentSLM import ProgressiveAgentSLM

_JSONC_COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)


def strip_jsonc(text: str) -> str:
    """Strip `//` and `/* */` comments from JSONC text (keeps strings intact)."""
    # Remove URLs inside strings from being treated as comments: process char by
    # char, tracking whether we are inside a string literal.
    out = []
    in_string = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '"' and (i == 0 or text[i - 1] != "\\"):
            in_string = not in_string
            out.append(ch)
            i += 1
        elif not in_string and text.startswith("//", i):
            j = text.find("\n", i)
            i = j if j != -1 else len(text)
        elif not in_string and text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = (j + 2) if j != -1 else len(text)
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def load_config(path_or_dict: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Read a JSONC file (or pass a dict through) into a plain dict."""
    if isinstance(path_or_dict, dict):
        return path_or_dict
    with open(path_or_dict, "r", encoding="utf-8") as fh:
        raw = fh.read()
    return json.loads(strip_jsonc(raw))


def resolve_base_folder(config: Dict[str, Any], parent_folder: str = "") -> str:
    """Resolve ``[base_folder_path]`` placeholders and default the folder."""
    raw = config.get("base_folder_path") or config.get("id") or "agent"
    if parent_folder and raw.startswith("[base_folder_path]"):
        return raw.replace("[base_folder_path]", parent_folder)
    return raw


def _build_agent(
    config: Dict[str, Any],
    parent_cfg: AgentConfig | None = None,
) -> AgentConfig:
    """Recursively build an AgentConfig tree, applying parent inheritance."""
    cfg = AgentConfig(**{k: v for k, v in config.items() if k != "delegates"})
    if parent_cfg is not None:
        cfg.inherit_from(parent_cfg)
    cfg.delegates = [_build_agent(d, cfg) for d in config.get("delegates", [])]
    cfg.validate()
    return cfg


def load_agent(path_or_dict: Union[str, Dict[str, Any]]) -> ProgressiveAgentSLM:
    """Build the full recursive agent tree from a JSONC path or Python dict.

    Example:
        agent = load_agent("src/framework/example-revised.json")
    """
    raw = load_config(path_or_dict)
    # Apply home-relative defaults for working_directories paths.
    home = os.path.expanduser("~")
    for wd in raw.get("working_directories", []):
        if wd.get("path", "").startswith("~"):
            wd["path"] = wd["path"].replace("~", home)

    cfg = _build_agent(raw)
    return ProgressiveAgentSLM(config=cfg)