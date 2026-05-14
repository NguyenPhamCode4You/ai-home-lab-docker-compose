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
Understanding its domain (voyages, shipments, bunker orders, financial settlement) is essential.

Critical workflow under analysis: {question}

Below are the enriched documentation files for every handler, entity, service,
and supporting file involved in this workflow. Read every section carefully.

--- ENRICHED DOCS ---
{context}
--- END OF DOCS ---

Produce the most thorough technical deep-dive document possible.
Use exact class names, method names, field names, and file paths from the documentation.
Generate EXACTLY these sections in this order:

---

# [FlowName] — Critical Workflow Deep Dive

(Replace [FlowName] with the workflow name: "{question}")

## Business Purpose
Why does this workflow exist? What business outcome does it produce for the shipping domain?

## Flow Overview
Detailed step-by-step narrative from HTTP request to final persisted state and response.
Cover every handler involved, not just the entry point.

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
Draw the complete flow including all handlers, services, and external clients.

## Key Business Rules
Numbered list of ALL business rules, validation constraints, and conditional logic
found across every file in this workflow. Quote field names and exact conditions.

## Entities Involved
- `EntityName` — role (primary entity / child entity / reference / output DTO)
(list every entity and DTO involved, with its specific role in this workflow)

## External Integrations Triggered
All ExternalClient calls, Azure Function triggers, background services, and outbound API calls.
Include exact method names. Write "None" if not applicable.

## Error Conditions
Every ApiException error code, business exception, and validation failure this workflow can raise.
State the exact condition that triggers each.

## Connection Links
Exact relative file paths from the codebase root for direct navigation:

- Handler(s): `Core/Business/...`
- Entity: `Core/Domain/...`
- DTO: `Core/Domain/...`
- Controller: `APIs/...`
- Validator: `Core/Business/...`
- External/Background: `...` (if applicable)

---

## Deep Technical Analysis

### Data Flow Map
Trace how data transforms step by step through the entire workflow:
Input DTO → FluentValidation → Handler logic → Entity construction/mutation →
Child record creation → EF Core SaveChangesAsync → Output DTO mapping.
Include specific field names, AutoMapper profiles, and derived calculation steps.

### State Machine
(Include this section ONLY if this workflow involves a status or lifecycle state field.)
Draw the complete state machine for the primary entity in this flow:

```mermaid
stateDiagram-v2
    [*] --> InitialState: TriggerAction
    InitialState --> NextState: ConditionOrEvent
    ...
```
List every valid state transition, guard condition, and what triggers each transition.
(Omit this section entirely if the workflow has no meaningful state machine.)

### Calculation Formula Breakdown
(Include this section ONLY for financial or calculation workflows.)
Document every formula extracted from the handler and domain code:

- `OutputField = [formula]` — [field-by-field explanation of operands and units]
- `AnotherField = [formula]` — [explanation]

List each formula as its own bullet. Explain what each operand represents in the domain.
(Omit this section entirely if the workflow performs no significant calculations.)

### Validation Gate Map
At which step in the flow does each FluentValidation rule fire?
Format as a table or numbered list showing: Rule → Trigger step → Error code/message → Hard stop or soft warning?

### Concurrency & Transaction Boundaries
Which operations share a single EF Core SaveChangesAsync transaction?
Where does optimistic concurrency (IVersionedEntity / RowVersion) apply?
Are there any race condition risks or known concurrency edge cases?

### Impact If Changed
For each key file in this workflow, assess the modification risk:

| File | Risk | Reason |
|---|---|---|
| `FileName.cs` | Low / Medium / High / Critical | [reason] |

### New Developer Onboarding Guide
Step-by-step guide for a developer who needs to add a new field or modify a business rule
within this specific workflow:

1. **Start here:** which file(s) to modify first and why
2. **Entity changes:** what to update in the domain entity and any related DTOs
3. **Mapping:** which AutoMapper profiles need updating
4. **Validation:** which FluentValidation rules to add or modify
5. **Handler logic:** what to change in the handler's Handle method
6. **Database migration:** is a new EF Core migration required?
7. **Testing:** which integration / unit tests must pass before merging
        """,
        )
        super().__init__(**kwargs)
