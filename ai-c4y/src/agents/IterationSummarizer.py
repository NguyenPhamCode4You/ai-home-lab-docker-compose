from .Task import Task
from .models.Ollama import Ollama

class IterationSummarizer(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "iteration-summarizer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            You are a concise summarizer. The following text is a previous answer attempt to a user's question.
            Extract and preserve ONLY the core facts, key points, code snippets, and conclusions that are relevant to the question.
            Discard any filler text, repeated content, or low-value explanation.

            User question: {question}

            Previous answer to summarize:
            {context}

            Return a compact but complete summary that retains all important information.
            The summary will be used as context for a follow-up answer, so accuracy and completeness matter more than brevity.
        """)
        super().__init__(**kwargs)
