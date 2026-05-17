from .Task import Task
from .models.Ollama import Ollama
from .constants import OLLAMA_GENERAL_MODEL


class CSharpImpactAnalyzer(Task):
    """
    Phase 3 agent.

    Performs cross-reference impact analysis for a single C# file.
    Receives:
      context  = the Phase 2 markdown document for this file
      question = JSON list of caller file entries from the used_by reverse-lookup index

    Generates two sections that are injected into the enriched doc:
      # Impact Scope   — replaces the PLACEHOLDER from Phase 2
      # Used By        — grouped caller list by architecture layer
    """

    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "csharp-impact-analyzer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_GENERAL_MODEL))
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
You are a senior .NET architect performing cross-reference impact analysis for the BVMS system.
BVMS follows Clean Architecture: Domain → Business → Infrastructure → API.
Do NOT explain what Clean Architecture or CQRS are — that is assumed knowledge.

Write with depth. For every explanation, answer: WHAT it does, WHY it matters, WHEN it is triggered,
and WHAT BREAKS if this file is changed or removed. Use exact class names and method names throughout.
Do NOT write generic sentences without naming real classes from the caller list.

Below is the documentation for a C# file, followed by the JSON list of other files that reference it.

[DOCUMENTATION]
{context}

[KNOWN CALLERS — files that import or reference this class]
{question}

Generate EXACTLY these two sections. No preamble, no extra commentary — output only the markdown:

# Impact Scope

**Impact Rating:** [Low | Medium | High | Critical]

**Impact Justification:**
Thorough explanation of the rating. Cover: how many callers exist and what layers they belong to,
which specific business operations (name the handler classes) depend on this file,
what data or behavior they extract from it, and whether this file is on a hot path
(called on every request vs. rare edge case). Do NOT pad with generic sentences.

**What breaks if this file changes:**

For each significant caller, write a specific entry:
1. `CallerClassName` — [exactly what operation it performs using this file, and what fails or corrupts if the contract changes]
2. [Next caller — use exact class names from the callers JSON]
(Cover ALL callers in the JSON. If there are none, state "No known callers — change is safe.")

**Affected Business Areas:**

- [Module name]: [specific operations and data flows in this module that are affected — name handler classes]
(List only affected areas with real specifics. Omit modules with zero dependency.)

**Safe to modify:** [Yes | With caution | Requires full regression test]
Explain: which specific callers require retesting, what integration points to verify, and whether
a database migration or AutoMapper profile update is needed alongside any code change.

# Used By

[List all callers from the provided JSON, grouped by architecture layer.
If a layer has no callers, omit that layer heading entirely.]

**Domain Layer:**
- `FileName.cs` — [what it inherits, implements, or references from this file and why]

**Business Layer (Handlers):**
- `FileName.cs` — [what specific operation it performs using this file: reads which field, calls which method, passes it to which calculation]

**Infrastructure Layer:**
- `FileName.cs` — [specific EF Core mapping, AutoMapper profile, or repository operation involving this file]

**API Layer:**
- `FileName.cs` — [which endpoint exposes or receives this class and what contract it enforces]

**Other:**
- `FileName.cs` — [specific usage]
        """)
        super().__init__(**kwargs)
