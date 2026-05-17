import os

from dotenv import load_dotenv

from .Task import Task
from .models.OpenRouter import OpenRouter

load_dotenv()

OPENROUTER_SYNTHESIS_MODEL = os.getenv("CIA_OPENROUTER_MODEL", "qwen/qwen3-32b")


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
Do NOT explain what these patterns are — focus entirely on the specific business logic in the cluster.

Write with depth. For every section, use exact class names, method names, and field names from the docs.
Answer WHAT each component does, WHY it exists in this flow, WHEN it is triggered, and WHAT BREAKS
if it is absent or incorrect. Do NOT write generic sentences that could apply to any system.

Cluster being synthesized: {question}

Below are enriched documentation files for all handlers and files in this business flow cluster.
Read all of them carefully, then synthesize a single cohesive workflow document.

[ENRICHED DOCS]
{context}
[END OF DOCS]

Generate a markdown document with EXACTLY these sections in this order.
Use the actual class names, method names, and file paths you found in the docs above.

# [Module] — [VerbCluster] Workflow

(Replace [Module] and [VerbCluster] with the actual values from the cluster label: "{question}")

## Business Purpose
What business goal does this cluster of operations serve?
What problem does it solve for the BVMS shipping/voyage management domain?
Name the specific user-facing operation(s) that trigger this workflow and what they produce.
Cover: who initiates it, what data it requires, what it persists or returns, and why it matters to the business.

## Flow Overview
Detailed step-by-step narrative of the end-to-end execution path.
Cover: HTTP request → Controller → MediatR.Send → Handler.Handle → EF Core DB operations → Response.
For each step, name the exact handler class and method. Explain what data it receives, what it validates,
what it computes or mutates, and what it hands off to the next step.

## Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Mediator as MediatR
    participant Handler
    participant DB as DataContext
```
Draw the primary flow using exact class names from the documentation.
Add extra participants for sub-handlers, ExternalClients, or BackgroundServices if invoked.

## Key Business Rules
Numbered list of ALL business rules, FluentValidation constraints, and conditional logic embedded in
this cluster. For each rule: name the class it lives in, quote the field name or condition,
and explain WHY this rule exists — what business invariant or data integrity concern it enforces.

## Entities Involved
- `EntityName` — role in this flow (primary / child / reference lookup / output DTO) and which handler reads/writes it

## External Integrations Triggered
All ExternalClient calls, Azure Function triggers, or background service calls within this flow.
Name the exact method, what data it sends, and what the business consequence of failure is.
Write "None" if there are no external integrations.

## Error Conditions
Every ApiException, business exception, and validation failure this flow can raise.
For each: the exact trigger condition, which handler raises it, and the business impact of the error.

## Technical Notes
Document any of the following found across the cluster docs — skip entirely if none apply:
- TODO / FIXME / bug reference comments from any file in the cluster: quote them and explain their current impact
- Ordering dependencies between handlers (e.g. "HandlerA must run before HandlerB because...")
- Non-obvious design decisions (e.g. why a two-step save, why a separate sub-handler exists)
- Known edge cases the code explicitly handles

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
