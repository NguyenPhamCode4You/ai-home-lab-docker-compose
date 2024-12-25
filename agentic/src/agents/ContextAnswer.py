from .Task import Task
from .models.Ollama import Ollama

class ContextAnswer(Task):
    def __init__(self):
        super().__init__(
            task_name="context-answer",
            llm_model=Ollama(),
            instruction_template="""
            Base on the context below, generate a well-structured, bullet-point and accurate answer to the question.
            {context}
            User question: {question}
            """
        )