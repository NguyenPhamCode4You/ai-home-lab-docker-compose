from .Task import Task
from .models.Ollama import Ollama

from .constants import OLLAMA_CODE_MODEL

class CodeSummarizer(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "code-summarizer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_CODE_MODEL))
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            You are an expert in the field of software development. Your task is to provide a summary of a code file.
            Summary should be concise and informative, highlighting the purpose of the code in terms of business logic and functionality.
            Now, in less than 200 words, summarize the code below:
            {context}
        """)
        super().__init__(**kwargs)