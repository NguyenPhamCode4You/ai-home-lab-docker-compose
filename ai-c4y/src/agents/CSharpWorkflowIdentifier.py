import json
import re

from .Task import Task
from .models.OpenRouter import OpenRouter
from .constants import OLLAMA_GENERAL_MODEL

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_CRITICAL_MODEL = os.getenv("CIA_OPENROUTER_CRITICAL_MODEL", "google/gemini-2.5-pro")

_SUFFIX = (
    "\n\nCRITICAL: Output ONLY the raw JSON array. "
    "No markdown code fences, no explanation. Start with [ and end with ]."
)


class CSharpWorkflowIdentifier(Task):
    """
    Workflow Identification agent.

    Receives a condensed per-module metadata snapshot of the entire C# codebase
    (class names, file types, handler verbs, referenced entities, criticality flags)
    and reverse-engineers which business workflows are likely complex / critical.

    Returns a JSON array of workflow candidates, each in the same format as
    PRIORITY_CRITICAL_FLOWS:

    [
      {
        "name":            "WorkflowName",         // CamelCase, no spaces
        "module":          "ModuleName",
        "required_tokens": ["token1"],             // ALL must match
        "any_tokens":      ["token2", "token3"],   // AT LEAST ONE must match
        "rationale":       "One sentence why this is critical"
      },
      ...
    ]

    The agent is intentionally liberal — it is better to over-identify and let
    Phase 4 Pass B discard flows with no matching enriched docs than to miss a
    genuinely complex workflow.
    """

    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "csharp-workflow-identifier")
        kwargs["llm_model"] = kwargs.get(
            "llm_model", OpenRouter(model=OPENROUTER_CRITICAL_MODEL)
        )
        kwargs["instruction_template"] = kwargs.get(
            "instruction_template",
            """
You are a principal .NET architect reverse-engineering a shipping management system called
BVMS (BBC Voyager Management System). The codebase follows Clean Architecture with CQRS
(MediatR handlers), EF Core, and a Domain-Business-Infrastructure layering.

Your task: study the condensed codebase metadata below and identify all **potentially complex
or critical business workflows** that are worth generating deep-dive documentation for.

Criteria for a "critical workflow":
  - Multi-step state transitions (e.g., lifecycle: created → confirmed → completed → closed)
  - Financial calculations with multiple inputs (P&L, commissions, ETS/carbon costs, bunker costs)
  - Cross-module operations that span two or more domain modules
  - Data sync / import / migration flows with external systems
  - Processes that, if broken, would directly impact billing, vessel scheduling, or regulatory reporting
  - Aggregation or estimation flows that feed downstream calculations

[CODEBASE METADATA]
{context}
[END OF METADATA]

Known workflow coverage to EXCLUDE (already have deep-dive docs):
{question}

Now identify NEW workflows not in the exclusion list.

For each candidate workflow, output a JSON object with:
  "name":            a CamelCase workflow identifier (no spaces, no special chars)
  "module":          the primary domain module (VoyageManagement, Finance, BunkerOrder,
                     MasterData, OrderRequest, UserManagement, ExternalClients, General)
  "required_tokens": list of lowercase word tokens that ALL matching class names MUST contain
  "any_tokens":      list of lowercase word tokens where AT LEAST ONE must appear in the class name
  "rationale":       one concise sentence explaining why this workflow is complex/critical

Return ONLY a JSON array of these objects. Aim for 5–20 candidates. Do not repeat anything
in the exclusion list.
""" + _SUFFIX,
        )
        kwargs.setdefault("max_context_chars", 200_000)  # cover full codebase metadata in one pass
        super().__init__(**kwargs)

    def parse_response(self, raw: str) -> list[dict]:
        """Extract and parse the JSON array from the LLM response."""
        # Strip markdown fences if present
        cleaned = re.sub(r"```(?:json)?\s*", "", raw).strip()
        cleaned = re.sub(r"```\s*$", "", cleaned).strip()
        # Find the outermost JSON array
        start = cleaned.find("[")
        end = cleaned.rfind("]")
        if start == -1 or end == -1:
            return []
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            return []
