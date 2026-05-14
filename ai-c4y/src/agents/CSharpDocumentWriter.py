from .Task import Task
from .models.Ollama import Ollama
from .constants import OLLAMA_CODE_MODEL


class CSharpDocumentWriter(Task):
    """
    Phase 2 agent.

    Generates a concise, file-focused markdown document for a single C# file.
    Receives:
      context  = full .cs file content
      question = JSON index context (architecture_layer, file_type, injected_services, known_callers, ...)

    Output adapts to file type:
      - Handlers/Use-cases (IRequestHandler) → workflow-focused: numbered steps, sub-handlers called, flags
      - Domain/DTO classes → member-focused: computed props, fallback chains, business fields
      - Validators → rule-focused: each RuleFor with its business constraint
      - Other → general members + dependencies

    The **Explanation** delimiter is intentional — the existing insert_code_documents()
    in CodeDocumentWorkflow.py splits on this boundary to store code and explanation
    as separate vector embeddings.
    """

    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "csharp-document-writer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_CODE_MODEL))
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
You are a senior .NET architect writing internal reference documentation for the BVMS codebase.
Be concise and direct. Do NOT explain what Clean Architecture, CQRS, or layers are in general —
that is assumed knowledge. Focus only on THIS file.

File metadata (use to enrich your explanations — do not just repeat it verbatim):
{question}

First, identify the file type from the code:
- HANDLER: implements IRequestHandler — the Handle/main method is a multi-step business workflow
- DOMAIN/DTO: a class with properties, computed fields, or domain logic (no Handle method)
- VALIDATOR: uses FluentValidation RuleFor chains
- OTHER: utility, helper, extension, or anything else

Then write the document using the matching template below. Use EXACTLY the sections shown.

# [Actual class name from the file]

## Purpose
One or two sentences: what does this class do and why does it exist?

## Business Responsibility
What specific business operation does this class own? How critical is it?
(e.g. "Core path for voyage cost finalization — called on every estimate save", "Low-impact DTO for list views")
IMPORTANT: Name the actual classes, DTOs, interfaces, and services from the index context that consume or depend on this file.
For example: "Acts as the EF Core entity mapped by `DataContext`. Projected into `StorageObjectDto` via AutoMapper. Consumed by `CreateFile` and `CreateFolder` handlers."
Do NOT write generic sentences like "core abstraction" or "canonical representation" without naming the real consumers.
2-4 sentences max.

[Now use the matching template below based on the file type identified above:]

[IF HANDLER (IRequestHandler):]

## Request Parameters
List each field on the Request class with its type and default value.
Format: `FieldName` (Type, default=X) — what enabling/disabling this flag changes in behavior.

## Guard Conditions
List every early-exit, skip, or short-circuit condition in the handler and the business reason for it.
Format: - Condition: `[code condition]` — Why: [business reason — what breaks or is meaningless without this guard]

## Workflow Steps
Document the Handle/main method as a numbered ordered sequence of business steps.
Each step = one or a few related lines that together achieve a distinct business outcome.
Cover every significant operation — do not skip mediator.Send calls or named helper calls.

### Step 1 — [What happens]
```csharp
[the exact code lines for this step]
```
**Why**: Business reason this step exists. What does it fix, validate, or produce? What breaks if it is skipped?

### Step 2 — ...
[continue for every meaningful step in execution order]

## Sub-handlers Invoked
List every `mediator.Send(new X.Request...)` call, in order of invocation:
- `HandlerName` — what business operation it performs and what it reads or mutates on the entity

[END HANDLER TEMPLATE]

[IF DOMAIN/DTO:]

## Members
Non-trivial members ONLY:
- Include: computed properties (`=>` expressions), `??` fallback chains, conditional logic, non-obvious default values that affect routing or behavior.
- SKIP: plain auto-properties with no logic (e.g. `public string Name {{ get; set; }}`), trivial constructors, ToString/Equals.

IMPORTANT — if the class has NO non-trivial members (all properties are plain auto-properties):
Do NOT invent explanations for simple properties. Instead write a single paragraph under `## Members` in this format:
"This class is a pure data carrier with no computed logic. All properties are scalar auto-properties mapped directly to [EF Core table / AutoMapper target / DTO projection]. It serves as [specific role: the primary persistence entity / the API response shape / the command input for XHandler]. Key fields: list the 3-5 most domain-meaningful field names and what they represent."

When documenting a non-trivial member, name the specific downstream handlers, services, or calculations that consume its value.

### 1. [MemberName] — [one-line purpose]
```csharp
[exact expression body or method body]
```
**Explanation**: What it computes, which fields it reads, the fallback/priority order, and which specific handlers or calculations downstream consume this value. 2-5 sentences.

[Repeat for each non-trivial member in file order.]

[END DOMAIN/DTO TEMPLATE]

[IF VALIDATOR:]

## Validation Rules
For each RuleFor block:
### [PropertyName]
- Rule: [what FluentValidation rule is applied]
- Business constraint: [why this field must satisfy this constraint in domain terms]

[END VALIDATOR TEMPLATE]

[IF OTHER (helper/extension/utility):]

## Members
Same format as DOMAIN/DTO above but focus on non-obvious logic and side-effects.

[END OTHER TEMPLATE]

## Dependencies
Bullet list. For each injected service, base class, interface, or key referenced type:
`Name` — why THIS file specifically needs it. Name the concrete capability it provides (e.g. "supplies `Id`, `CreatedAt`, `UpdatedAt` audit fields required by EF Core mapping and soft-delete contracts" not just "base entity").
Skip primitive types.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]

C# file to document:

{context}
        """)
        super().__init__(**kwargs)
