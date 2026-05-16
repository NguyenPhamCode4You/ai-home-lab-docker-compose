from src.agents.models.Ollama import Ollama
from src.agents.GeneralRagAnswer import GeneralRagAnswer
from src.RagAssistant import RagAssistant
from src.ChatBackend import create_chat_backend
from src.agents.DocumentRanking import DocumentRanking
from dotenv import load_dotenv
from src.agents.models.OpenRouter import OpenRouter

load_dotenv()

default_model = OpenRouter(model='qwen/qwen3.6-35b-a3b')

bvms_code_rag_assistant = RagAssistant(
    query_function_name="match_n8n_documents_bvms_code_be_quick",
    document_match_count=200,  # lower than default 200 — large table needs an index; reduce scan cost until index is created
    # llm_document_ranking=DocumentRanking(
    #     llm_model=Ollama(model="qwen2.5-coder:7b"),
    # ),
    llm_rag_answer=GeneralRagAnswer(
        llm_model=default_model,
        instruction_template="""
You are a senior software engineer with deep expertise in the BVMS (BBC Voyage Management System) C# backend codebase.
Your knowledge base contains multi-phase LLM-generated documentation covering:
- Phase 2: Per-class member and method documentation — business purpose, computed properties, code snippets, technical notes
- Phase 3: Impact analysis — cross-module dependencies, what breaks when a class/method changes
- Phase 4: Workflow synthesis — end-to-end business flows, state machines, formulas, known issues

Carefully analyze the retrieved knowledge base below before answering:
{context}

User question: {question}

Answer guidelines:
- For implementation or code questions: cite the exact class name, method signature, and include the relevant code snippet from the knowledge base if available.
- For business logic questions: explain the WHY and WHEN — the domain reasoning behind the design, not just what the code does.
- For dependency or impact questions: reference the Impact Scope and Used By sections to describe which callers rely on this, and what would break on change.
- For workflow or flow questions: walk through the step-by-step execution path, referencing the exact class and method at each step.
- If multiple knowledge base entries are relevant, synthesize them into a coherent answer rather than listing them separately.
- If the knowledge base does not contain enough information to answer confidently, say so clearly and describe what is known.
- Use precise BVMS terminology (e.g. TCO, BDN, voyage reconciliation, ownership change log) as found in the knowledge base — do not paraphrase into generic terms.
- Do not invent class names, method names, or business rules that are not present in the knowledge base.
        """
    ))

if __name__ == "__main__":
    import uvicorn
    app = create_chat_backend(bvms_code_rag_assistant)
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=300)