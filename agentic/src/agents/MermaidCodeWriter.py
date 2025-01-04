from .Task import Task
from .models.Ollama import Ollama

from .constants import OLLAMA_CODE_MODEL

class MermaidCodeWriter(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "mermaid-code-writer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_CODE_MODEL))
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            You are an intelligent mermaid markdown assistant that can help user create diagram basing on a given context.
            {context}
            {histories}
            User question: {question}
            Provide the markdown in mermaid language to create a diagram that best answers the user question.
            TRY to be as simple in your code as possible.
            Return markdown wrapped in ```mermaid ``` block, no explanation needed.
            """)
        super().__init__(**kwargs)