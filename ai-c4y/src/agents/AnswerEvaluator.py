from .Task import Task
from .models.Ollama import Ollama

class AnswerEvaluator(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "answer-evaluator")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            You are a strict evaluator. Given the user's original question and the current answer, decide whether the answer is complete and satisfactory.

            User question: {question}

            Current answer:
            {context}

            Reply ONLY with a valid JSON object — no extra text, no markdown:
            If the answer is complete and satisfactory: {{"satisfied": true}}
            If the answer is incomplete or missing important details: {{"satisfied": false, "follow_up": "describe specifically what aspect is still unanswered or needs more detail"}}
        """)
        super().__init__(**kwargs)
