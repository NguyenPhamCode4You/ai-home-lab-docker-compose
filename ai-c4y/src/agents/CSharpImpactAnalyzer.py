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

Below is the documentation for a C# file, followed by the JSON list of other files that reference it.

--- DOCUMENTATION ---
{context}

--- KNOWN CALLERS (files that import or reference this class) ---
{question}

Generate EXACTLY these two sections. No preamble, no extra commentary — output only the markdown:

---

# Impact Scope

**Impact Rating:** [Low | Medium | High | Critical]

**Impact Justification:**
1–2 sentences explaining the rating based on how many callers exist, what they do,
and what business operations depend on this file.

**What breaks if this file changes:**

1. [Name a specific handler / business flow / operation that relies on this file, and what it loses]
2. [Another specific dependent — use exact class names from the callers list]
(list all significant callers; if there are none, state "No known callers — change is safe.")

**Affected Business Areas:**

- [Module name]: [how this module is affected — e.g., "VoyageManagement: all voyage reads would fail"]
(list only affected areas; omit modules with no dependency on this file)

**Safe to modify:** [Yes | With caution | Requires full regression test]
[One sentence explaining the assessment.]

# Used By

[List all callers from the provided JSON, grouped by architecture layer.
If a layer has no callers, omit that layer heading entirely.]

**Domain Layer:**
- `FileName.cs` — [one-line note on how it uses this file]

**Business Layer (Handlers):**
- `FileName.cs` — [one-line note]

**Infrastructure Layer:**
- `FileName.cs` — [one-line note]

**API Layer:**
- `FileName.cs` — [one-line note]

**Other:**
- `FileName.cs` — [one-line note]
        """)
        super().__init__(**kwargs)
