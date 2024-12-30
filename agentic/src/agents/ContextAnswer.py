from .Task import Task
from .models.Ollama import Ollama

class ContextAnswer(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "context-answer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            Base on the context below, generate a well-structured, bullet-point and accurate answer to the question.
            {context}
            User question: {question}
        """)
        super().__init__(**kwargs)