"""agents/Router — description-based delegate routing + tool-menu pruning.

Reads each delegate's ``description`` and picks delegate(s) for a sub-question via
the generalized ``_parse_agent_routing`` JSON pattern (``delegate:<id>``). Also
prunes the tool menu by each tool's ``when``.
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List

_ROUTING_RE = re.compile(r"```json\s*(\[.*?\])\s*```", re.DOTALL)


def parse_agent_routing(text: str) -> List[Dict[str, Any]]:
    """Parse a ```json [{agent, question}]``` routing block; robust fallback."""
    m = _ROUTING_RE.search(text)
    if not m:
        return []
    try:
        parsed = json.loads(m.group(1))
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    return [r for r in parsed if isinstance(r, dict) and r.get("agent")]


class Router:
    def __init__(self, delegates: List[Any]) -> None:
        self._delegates = {d.description: d for d in delegates}

    def matches(self, description: str) -> Any:
        return self._delegates.get(description)

    def route(self, routing_text: str) -> List[Dict[str, Any]]:
        """Return [{agent, question}] from a model's routing output."""
        return parse_agent_routing(routing_text)