# Phase 6 — RAG Chat Setup

## Status: ⏳ NOT STARTED

**Purpose:** Wire the `n8n_documents_bvms_code` knowledge base into the existing chat system. Create a specialized code-technical RAG assistant and register it as the third agent in the existing `AssistantOrchestra`.

---

## Files to Create / Modify

| File                    | Action                              |
| ----------------------- | ----------------------------------- |
| `rag_chat_bvms_code.py` | Create — mirrors `rag_chat_bvms.py` |
| `rag_orchestra.py`      | Modify — add third agent            |

---

## Design Details

### 6.1 — `rag_chat_bvms_code.py`

Mirrors the existing `rag_chat_bvms.py`. Key differences:

- `query_function_name = "match_n8n_documents_bvms_code"`
- Uses `OpenRouter` as the default model (code questions benefit from stronger reasoning)
- Instruction template is C#/CQRS-specific with emphasis on impact analysis

```python
from src.agents.models.Ollama import Ollama
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.RagAssistant import RagAssistant
from src.agents.DocumentRanking import DocumentRanking
from src.agents.models.OpenRouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()

bvms_code_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_code",
    llm_document_ranking=DocumentRanking(
        llm_model=Ollama(model="gemma3:4b"),
    ),
    llm_rag_answer=GeneralRagAnswer(
        llm_model=OpenRouter(model="qwen/qwen3-32b"),
        instruction_template="""
        You are a deep technical expert on the BVMS (BBC Voyager Management System) C# backend.
        You understand Clean Architecture, CQRS with MediatR, Entity Framework Core,
        FluentValidation, and the BVMS domain (voyage management, shipping, P&L calculation).

        Use the knowledge base below to answer technical questions about:
        - Specific handlers, entities, services, and their purpose
        - End-to-end business workflow flows (e.g., how a voyage is created from an estimate)
        - Impact analysis: what breaks if a specific file, method, or entity is changed
        - Development guidance: where to put new code, what patterns to follow
        - Business rules embedded in the code (validation, calculations, state transitions)

        {context}

        User question: {question}

        Be specific. Reference exact file names, class names, and method names from the knowledge base.
        When discussing impact, clearly state impact rating (Low/Medium/High/Critical) and which flows are affected.
        When giving development guidance, reference the correct folder paths and existing patterns to follow.
        """
    )
)

if __name__ == "__main__":
    import uvicorn
    from src.ChatBackend import create_chat_backend
    app = create_chat_backend(bvms_code_rag_assistant)
    uvicorn.run(app, host="0.0.0.0", port=8002, timeout_keep_alive=300)
```

Note: runs on port `8002` (not `8001`) when run standalone to avoid conflict with `rag_orchestra.py`.

---

### 6.2 — Update `rag_orchestra.py`

Add the third agent to the existing `assistant.agents` dict:

```python
from rag_chat_bvms_code import bvms_code_rag_assistant

assistant.agents = {
    "BVMS-General Assistant": {
        "agent": bvms_rag_assistant,
        "context_awareness": True,
        "description": "This agent can generate detailed responses about a software named BVMS (BBC Voyager Management System)"
    },
    "BVMS-Code Assistant": {
        "agent": bvms_code_assistant,
        "context_awareness": True,
        "description": "This agent can provide code snippet and code explanation for a software named BVMS (BBC Voyager Management System)"
    },
    "BVMS-Code Technical Assistant": {
        "agent": bvms_code_rag_assistant,
        "context_awareness": True,
        "description": "This agent answers deep technical questions about the BVMS C# codebase: specific handler flows, entity relationships, impact analysis for code changes, and step-by-step development guidance for new features. Best for questions like 'what breaks if I change X', 'how does the voyage P&L calculation work', or 'where should I put this new handler'."
    },
}
```

The `QuestionForwarder` in `AssistantOrchestra` will route technical C# questions to this agent based on the description.

---

### 6.3 — Port & Docker Config

If running via Docker (`docker-compose.yml` in `ai-c4y/`), no new service is needed — `rag_orchestra.py` already includes all three agents on port `8001`.

If running `rag_chat_bvms_code.py` standalone for testing, it uses port `8002`.

---

## Verification

- [ ] Run `python rag_chat_bvms_code.py` standalone
- [ ] Ask: "What does `GetVoyageById` do?" — verify it returns accurate handler description with method details
- [ ] Ask: "What is the impact of changing `VoyageEntity`?" — verify it returns `Critical` impact with list of dependents
- [ ] Ask: "How does the voyage P&L calculation work?" — verify it returns the workflow narrative with formula details
- [ ] Ask: "Where should I put a new handler to cancel a voyage?" — verify it gives correct folder path and pattern guidance
- [ ] Run `rag_orchestra.py` — verify the orchestra correctly routes "what breaks if I modify ShipmentValidator" to `BVMS-Code Technical Assistant`
- [ ] Verify `BVMS-General Assistant` still routes business-level questions correctly (regression check)

---

## What Was Done

_(Fill in after completion)_
