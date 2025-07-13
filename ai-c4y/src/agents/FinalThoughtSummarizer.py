from .Task import Task
from .models.Ollama import Ollama

class FinalThoughtSummarizer(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "final-thought-summarizer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            You are the final thought that reflects your previous answers to the user questions.
            Here is the user question: {question}
            Your previous answers to the user questions:
            {context}
            Generate one final answer that combines all the previous answers to the user questions as your best answer to the user question.
        """)
        super().__init__(**kwargs)