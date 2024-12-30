from .Task import Task
from .models.Ollama import Ollama

from .constants import OLLAMA_CODE_MODEL

class JSONSummarizer(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "json-summarizer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_CODE_MODEL))
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            Given the following JSON response:
            -------------------
            {context}
            -------------------
            
            User Question: 
            -------------------
            {question}
            -------------------

            Describe the response in plain text format, conform to the user's question. 
            Be concise, accurate and produce a well-structured response with bullet points.
            DO NOT make up information not present in the response.

            Important:
            - Provide minimal details and avoid verbosity if user does not ask for detailed information.
        """)
        super().__init__(**kwargs)