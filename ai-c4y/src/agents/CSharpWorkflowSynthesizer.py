import os

from dotenv import load_dotenv

from .Task import Task
from .models.OpenRouter import OpenRouter

load_dotenv()

OPENROUTER_SYNTHESIS_MODEL = os.getenv("CODE_IMPACT_ANALYZER_SYNTHESIS_MODEL", "qwen/qwen3-32b")


class CSharpWorkflowSynthesizer(Task):
    """
    Phase 4 Pass A agent.

    Synthesizes a cohesive workflow document from a cluster of enriched per-file docs
    that belong to the same domain module and business-verb group.

    Receives:
      context  = concatenated enriched markdown docs for the cluster (up to 40 000 chars)
      question = cluster label string, e.g. "VoyageManagement — WriteFlows"

    Output: a single workflow markdown doc with sequence diagram, business rules,
    entities, error conditions, and connection links.

    Always uses a cloud model (qwen/qwen3-32b by default) — local models lack the
    context window and reasoning depth required for multi-doc synthesis.
    """

    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "csharp-workflow-synthesizer")
        kwargs["llm_model"] = kwargs.get(
            "llm_model", OpenRouter(model=OPENROUTER_SYNTHESIS_MODEL)
        )
        kwargs["instruction_template"] = kwargs.get(
            "instruction_template",
            """
You are a senior .NET architect synthesizing business workflow documentation for the BVMS system.
BVMS (BBC Voyager Management System) is a shipping/voyage management platform.
The codebase follows Clean Architecture with CQRS (MediatR), EF Core, FluentValidation, and AutoMapper.

Cluster being synthesized: {question}

Below are enriched documentation files for all handlers and files in this business flow cluster.
Read all of them carefully, then synthesize a single cohesive workflow document.

--- ENRICHED DOCS ---
{context}
--- END OF DOCS ---

Generate a markdown document with EXACTLY these sections in this order.
Use the actual class names, method names, and file paths you found in the docs above.

---

# [Module] — [VerbCluster] Workflow

(Replace [Module] and [VerbCluster] with the actual values from the cluster label: "{question}")

## Business Purpose
What business goal does this cluster of operations serve?
What problem does it solve for the BVMS shipping/voyage management domain?
Keep to 2–4 sentences.

## Flow Overview
Step-by-step narrative of the typical end-to-end execution path.
Cover: HTTP request → Controller → MediatR.Send → Handler.Handle → EF Core DB operations → Response.
Reference exact class names and method names found in the docs.

## Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Mediator as MediatR
    participant Handler
    participant DB as DataContext
    ...
```
Draw the primary flow for this cluster using exact class names from the documentation.
Add extra participants for ExternalClients or BackgroundServices if they are invoked.

## Key Business Rules
Numbered list of all business rules, FluentValidation constraints, and conditional logic
embedded in this cluster of handlers. Be specific — quote field names and conditions.

## Entities Involved
- `EntityName` — role in this flow (primary / child / reference lookup / output DTO)
(list every entity and DTO class referenced across the cluster)

## External Integrations Triggered
List any ExternalClient calls, Azure Function triggers, or background service calls
that occur within this flow. Include method names.
Write "None" if there are no external integrations.

## Error Conditions
What ApiException error codes, business exceptions, or validation failures can this flow raise?
State each condition and the trigger.

## Connection Links
Direct file references for developer navigation (exact relative paths from the codebase root):

- Handler(s): `Core/Business/...`
- Entity: `Core/Domain/...`
- DTO: `Core/Domain/...`
- Controller: `APIs/...`
- Validator: `Core/Business/...`
- Background/External: `...` (include only if applicable)
        """,
        )
        super().__init__(**kwargs)
