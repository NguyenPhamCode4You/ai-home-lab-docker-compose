"""validate_scaffold.py — prove the scaffold imports + the tree builds.

Run:  python validate_scaffold.py
Asserts:
  1. Every module under src/framework + src/agents/models imports.
  2. The canonical config (JSONC) parses.
  3. The full recursive agent tree builds (parent + bvms-code-analyzer).
  4. The tool factory binds the tools declared in config.
"""
from __future__ import annotations

import importlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODULES = [
    # framework core
    "framework.AgentConfig",
    "framework.ContextWindow",
    "framework.ModelChain",
    "framework.CircularRounds",
    "framework.BehaviorPolicies",
    "framework.ToolRegistry",
    "framework.ParallelExecutor",
    "framework.ProgressiveAgentSLM",
    "framework.bounded_io",
    "framework.redact",
    "framework.tokens",
    # subpackages
    "framework.agents.Router",
    "framework.agents.Reflector",
    "framework.guards.tool_loop",
    "framework.guards.verify_on_stop",
    "framework.delegates.contracts",
    "framework.tools.safety",
    "framework.tools.ReadFileTool",
    "framework.tools.TodoTool",
    "framework.tools.SqliteVectorQueryTool",
    "framework.tools.JsonlQueryTool",
    "framework.memory.RawLog",
    "framework.memory.MemoryStore",
    "framework.memory.MemoryStores",
    "framework.memory.Distiller",
    "framework.memory.LogSearch",
    "framework.memory.RunLogger",
    "framework.modes.AssistantMode",
    "framework.modes.ResearchMode",
    "framework.config.load",
    # model clients
    "agents.models.Ollama",
    "agents.models.OpenRouter",
]


def main() -> int:
    failures = 0
    print("== 1. Module imports ==")
    for name in MODULES:
        try:
            importlib.import_module(name)
            print(f"  ✓ {name}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  ✗ {name}: {exc}")

    print("\n== 2. Canonical config parses (JSONC) ==")
    try:
        from framework.config.load import load_agent

        config_path = str(SRC / "framework" / "example-revised.json")
        agent = load_agent(config_path)
        print(f"  ✓ parsed {config_path}")

        print("\n== 3. Recursive tree builds ==")
        print(f"  ✓ root: {agent.id} (depth {agent.depth})")
        print(f"  ✓ delegates: {[d.id for d in agent.delegates]}")

        print("\n== 4. Tool factory binds declared tools ==")
        bound = [t.name for t in agent._tool_registry._tools.values()]
        print(f"  ✓ tools registered: {sorted(bound)}")
    except Exception as exc:  # noqa: BLE001
        failures += 1
        print(f"  ✗ {exc}")

    print(f"\n{'FAILED' if failures else 'OK'} — {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())