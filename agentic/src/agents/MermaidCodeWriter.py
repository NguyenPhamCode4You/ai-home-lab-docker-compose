from .Task import Task
from .models.Ollama import Ollama

from .constants import OLLAMA_CODE_MODEL

class MermaidCodeWriter(Task):
    def __init__(self):
        super().__init__(
            task_name="mermaid-code-writer",
            llm_model=Ollama(
                model=OLLAMA_CODE_MODEL
            ),
            instruction_template="""
            You are an intelligent mermaid markdown assistant that can help user create diagram basing on a given context.
            {context}
            {histories}
            User question: {question}
            Provide the markdown in mermaid language to create a diagram that best answers the user question.
            TRY to be as simple in your code as possible.
            Return markdown wrapped in ```mermaid ``` block, no explaination needed
            """
        )