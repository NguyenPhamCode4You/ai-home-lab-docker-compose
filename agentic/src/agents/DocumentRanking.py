from .Task import Task
from .models.Ollama import Ollama

class DocumentRanking(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "document-ranking")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            On the scale of 1 to 10, how would you rate the following documents based on their relevance to a given user question?
            The question: {question}
            The document: {context}
            Return only the score between 1 and 10. No extra explanation needed.
        """)
        super().__init__(**kwargs)