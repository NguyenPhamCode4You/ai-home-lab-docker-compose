from .Task import Task
from .models.Ollama import Ollama
from .constants import OLLAMA_CODE_MODEL


class CSharpDocumentWriter(Task):
    """
    Phase 2 agent.

    Generates a structured markdown document for a single C# file.
    Receives:
      context  = full .cs file content
      question = JSON index context (architecture_layer, file_type, injected_services, known_callers, ...)

    Output sections (in order):
      # General Purpose
      # Architecture Layer
      # Class: <Name>
      ## N. MethodName — purpose
      ```csharp ... ``` + **Explanation**: ...
      # Dependencies
      # Impact Scope    ← PLACEHOLDER, replaced in Phase 3

    The **Explanation** delimiter is intentional — the existing insert_code_documents()
    in CodeDocumentWorkflow.py splits on this boundary to store code and explanation
    as separate vector embeddings.
    """

    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "csharp-document-writer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_CODE_MODEL))
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
You are a senior .NET software architect documenting the BVMS C# backend codebase.
BVMS (BBC Voyager Management System) is a shipping/voyage management platform.
The codebase follows Clean Architecture with CQRS (MediatR), EF Core, FluentValidation, and AutoMapper.

File metadata from the index (use this to enrich your explanations):
{question}

Generate a markdown document for the C# file below.
Use EXACTLY these sections in this order — do not skip any section:

---

# General Purpose
One paragraph explaining what this file does and WHY it exists in the system.
Describe its role within its architecture layer of CQRS/Clean Architecture.

# Architecture Layer
State the layer: Domain | Business | Infrastructure | API | ExternalClient | Functions
Explain the responsibilities of this layer and how this specific file fits within it.

# Class: [write the actual class name here]
Brief class-level description.
List constructor parameters / injected dependencies.
Name any interface contracts the class implements (IRequestHandler, IValidator, etc.).

## 1. [MethodName] — [one-line purpose]
```csharp
[paste the exact code of this method from the file]
```

**Explanation**:
Detailed explanation: what this method does step by step, what inputs it expects,
what it returns or what side-effects it produces, and any business rules or conditions
embedded in the logic. Reference field names, entity names, and service calls explicitly.

[Repeat ## N. for each public method in the class. Use sequential numbers starting at 1.]

# Dependencies
List every injected service, repository, DbContext, IMapper, and entity type referenced in this file.
For each, write one line explaining WHY it is needed in this file's context.

# Impact Scope
[PLACEHOLDER — will be filled in Phase 3]

---

Now document this C# file:

{context}
        """)
        super().__init__(**kwargs)
