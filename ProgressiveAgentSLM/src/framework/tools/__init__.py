# src/framework/tools — SqliteVectorQueryTool, JsonlQueryTool, ReadFileTool,
# SearchFileTool, WriteFileTool, TodoTool, GenerateDiagramTool, RunPythonTool,
# SearchInternetTool, CodeAnalysisTool

"""Tool factory: builds a Tool instance from a config dict `{type, when, ...}`.

Phase 1 fills each concrete tool; the factory returns ``None`` for tool types
that are not yet implemented so the scaffold stays importable and the agent tree
still builds from config before every tool exists.
"""
from __future__ import annotations

from typing import Optional

from ..ToolRegistry import Tool


def build_tool(cfg: dict) -> Optional[Tool]:
    """Build a tool from a config dict, or ``None`` if not yet implemented."""
    tool_type = cfg.get("type", "")
    when = cfg.get("when", "")

    if tool_type == "ReadFileTool":
        from .ReadFileTool import ReadFileTool

        tool = ReadFileTool()
        tool.when = when
        return tool
    if tool_type == "TodoTool":
        from .TodoTool import TodoTool

        tool = TodoTool()
        tool.when = when
        return tool
    if tool_type == "SqliteVectorQueryTool":
        from .SqliteVectorQueryTool import SqliteVectorQueryTool

        tool = SqliteVectorQueryTool(path=cfg.get("path", ""), table=cfg.get("table", ""))
        tool.when = when
        return tool
    if tool_type == "JsonlQueryTool":
        from .JsonlQueryTool import JsonlQueryTool

        tool = JsonlQueryTool(path=cfg.get("path", ""))
        tool.when = when
        return tool
    # SearchFileTool / WriteFileTool / GenerateDiagramTool / RunPythonTool /
    # SearchInternetTool / CodeAnalysisTool land in Phase 2.
    return None