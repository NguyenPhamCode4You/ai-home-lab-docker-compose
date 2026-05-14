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

    Output sections (in order):
      # [ClassName]
      ## Purpose
      ## Business Responsibility
      ## Methods
      ## Dependencies
      # Impact Scope    ← PLACEHOLDER, replaced in Phase 3

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
that is assumed knowledge. Focus only on THIS file: what it does, why it matters, and how it behaves.

File metadata (use to enrich your explanations — do not just repeat it verbatim):
{question}

Write a compact markdown document using EXACTLY these sections in this order:

---

# [Actual class name from the file]

## Purpose
One or two sentences. What does this class do and why does it exist?

## Business Responsibility
What specific business operation or rule does this class own?
How critical is it to the business process? (e.g. "Core path for voyage cost finalization", "Low-impact utility for formatting")
Keep to 2–4 sentences.

## Methods

### 1. [MethodName] — [one-line purpose]
```csharp
[exact method signature only — no body needed unless the body IS the documentation value]
```
**Explanation**: What this method does, what it returns or persists, and any embedded business rules. Be specific — name fields, entities, conditions. 2–5 sentences max.

[Repeat ### N. for each significant public method. Skip trivial getters/setters.]

## Dependencies
Bullet list. For each injected service or key type: `ServiceName` — why this file needs it specifically.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]

---

C# file to document:

{context}
        """)
        super().__init__(**kwargs)
