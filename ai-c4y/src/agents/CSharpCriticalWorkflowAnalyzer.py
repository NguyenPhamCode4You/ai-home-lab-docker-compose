import os

from dotenv import load_dotenv

from .Task import Task
from .models.OpenRouter import OpenRouter

load_dotenv()

OPENROUTER_CRITICAL_MODEL = os.getenv("CIA_OPENROUTER_CRITICAL_MODEL", "google/gemini-2.5-pro")


class CSharpCriticalWorkflowAnalyzer(Task):
    """
    Phase 4 Pass B agent.

    Generates an exhaustive deep-dive document for a critical business workflow.
    Triggered for flows with is_critical=True files or matching the priority list
    (P&L calculation, voyage lifecycle, bunker cost, commission/payment, ETS emissions).

    Receives:
      context  = concatenated enriched markdown docs for the entire flow (up to 60 000 chars)
      question = flow name, e.g. "CalculateVoyagePnL" or "CreateVoyageFromEstimate"

    Output: a comprehensive technical document with everything from Pass A PLUS:
      - Data flow map with field-level transformations
      - State machine diagram (for lifecycle flows)
      - Calculation formula breakdown (for financial flows)
      - Validation gate map
      - Concurrency & transaction boundaries
      - Per-method impact assessment
      - New developer onboarding guide

    Always uses the best available cloud model (google/gemini-2.5-pro by default).
    """

    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "csharp-critical-workflow-analyzer")
        kwargs["llm_model"] = kwargs.get(
            "llm_model", OpenRouter(model=OPENROUTER_CRITICAL_MODEL)
        )
        kwargs["instruction_template"] = kwargs.get(
            "instruction_template",
            """
You are a principal .NET architect performing a deep technical analysis of a critical business
workflow in the BVMS (BBC Voyager Management System) shipping management platform.

BVMS follows Clean Architecture with CQRS (MediatR), EF Core, FluentValidation, and AutoMapper.
Do NOT explain what these patterns are — focus entirely on the specific BVMS domain logic.

Write with maximum depth. For every section: use exact class names, method names, field names
from the docs below. Answer WHAT it does, WHY it exists, WHEN it fires, and WHAT BREAKS if absent.
Never write a generic sentence that could apply to any system. Name real classes throughout.

Critical workflow under analysis: {question}

Below are the enriched documentation files for every handler, entity, service,
and supporting file involved in this workflow. Read every section carefully.

[ENRICHED DOCS]
{context}
[END OF DOCS]

Produce the most thorough technical deep-dive document possible.
Generate EXACTLY these sections in this order:

# [FlowName] — Critical Workflow Deep Dive

(Replace [FlowName] with the workflow name: "{question}")

## Business Purpose
Why does this workflow exist? What business outcome does it produce for the BVMS shipping domain?
Name the specific user-facing operation that triggers it, what it persists or computes, and
what downstream processes (invoicing, voyage reporting, ownership calculation) depend on its output.

## Flow Overview
Detailed step-by-step narrative from HTTP request to final persisted state and response.
Cover every handler involved, not just the entry point. For each handler, explain:
what input it receives, what validation it applies, what computation or mutation it performs,
and what it hands to the next step. Use exact class names throughout.

## Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Mediator as MediatR
    participant Handler
    participant DB as DataContext
```
Draw the complete flow including all handlers, services, and external clients with exact class names.

## Key Business Rules
Numbered list of ALL business rules, validation constraints, and conditional logic
found across every file in this workflow. For each rule:
- Name the class it lives in
- Quote the field name or exact condition
- Explain WHY this rule exists — what business invariant, financial integrity, or data consistency concern it enforces
- State WHAT BREAKS in BVMS if this rule is violated or bypassed

## Entities Involved
- `EntityName` — role (primary entity / child entity / reference / output DTO), which handler reads/writes it,
  and what data it carries that is critical to this flow

## External Integrations Triggered
All ExternalClient calls, Azure Function triggers, background services, and outbound API calls.
For each: exact method name, data sent, and business consequence of failure.
Write "None" if not applicable.

## Error Conditions
Every ApiException error code, business exception, and validation failure this workflow can raise.
For each: the exact trigger condition, which class raises it, and the business impact on the workflow.

## Connection Links
Exact relative file paths from the codebase root for direct navigation:

- Handler(s): `Core/Business/...`
- Entity: `Core/Domain/...`
- DTO: `Core/Domain/...`
- Controller: `APIs/...`
- Validator: `Core/Business/...`
- External/Background: `...` (if applicable)

## Deep Technical Analysis

### Data Flow Map
Trace how data transforms step by step through the entire workflow:
Input DTO → FluentValidation → Handler logic → Entity construction/mutation →
Child record creation → EF Core SaveChangesAsync → Output DTO mapping.
For each transformation, name the exact field, AutoMapper profile used, and any derived calculation.

### State Machine
(Include ONLY if this workflow involves a status or lifecycle state field.)
```mermaid
stateDiagram-v2
    [*] --> InitialState: TriggerAction
    InitialState --> NextState: ConditionOrEvent
```
List every valid state transition, guard condition, and what triggers each transition.
Explain WHY each guard exists and WHAT BREAKS if it is bypassed.
(Omit this section entirely if the workflow has no meaningful state machine.)

### Calculation Formula Breakdown
(Include ONLY for financial or calculation workflows.)
Document every formula extracted from the handler and domain code.
For each formula, show the exact C# code snippet:

```csharp
public decimal FieldName => [exact expression from source];
```
**Operands**: explain each variable — what it represents in the BVMS domain, where it comes from,
what unit or currency it carries, and what happens when it is null or zero.
**Business meaning**: what this calculated value is used for downstream.

(Omit this section entirely if the workflow performs no significant calculations.)

### Validation Gate Map
At which step in the flow does each FluentValidation rule fire?
For each rule: the class name, the rule condition, when it fires, the error raised,
and whether it is a hard stop (HTTP 400/422) or a soft warning.

### Concurrency & Transaction Boundaries
Which operations share a single EF Core SaveChangesAsync transaction?
Where does optimistic concurrency (IVersionedEntity / RowVersion) apply?
Are there any race condition risks or known concurrency edge cases?
What happens if a concurrent request modifies the same entity mid-flow?

### Impact If Changed
For each key file in this workflow, assess the modification risk:

| File | Risk | Reason |
|---|---|---|
| `FileName.cs` | Low / Medium / High / Critical | [exact reason — what callers break and why] |

### New Developer Onboarding Guide
Step-by-step guide for a developer who needs to add a new field or modify a business rule
within this specific BVMS workflow:

1. **Start here:** which file(s) to open first and exactly what to look for
2. **Entity changes:** what to add to the domain entity class and any related DTOs (name them)
3. **AutoMapper profiles:** which profile files need a new `.ForMember(...)` mapping
4. **FluentValidation:** which validator class to add or modify a `RuleFor(...)` in
5. **Handler logic:** what to change inside the `Handle(...)` method — which variable, which condition
6. **Database migration:** run `dotnet ef migrations add <MigrationName> -p Infrastructure -s API` — yes/no and why
7. **Testing:** which specific integration tests or test handlers must pass before merging

### Known Issues & Design Decisions
Document any of the following found in the enriched docs — skip entirely if none apply:
- TODO / FIXME / bug reference comments: quote the exact comment and explain its current business impact
- Ordering dependencies: e.g. "HandlerA must complete before HandlerB because entity X must exist"
- Non-obvious design decisions: e.g. why a two-step save, why a dedicated sub-handler was introduced
- Known edge cases the code explicitly handles and why the special path exists
        """,
        )
        super().__init__(**kwargs)
