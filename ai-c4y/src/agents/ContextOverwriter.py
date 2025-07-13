from .Task import Task
from .models.Ollama import Ollama

class ContextOverwriter(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "context-overwriter")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            Using markdown, rewrite the content below in your own words, conform to user question if provided.
            {context}
            User question: {question}
            Important:
            1. DO NOT include noise or irrelevant information, for example: ads, comments, page navigation, hyberlink, citations, references.
            2. Keep the content clear, detailed, well-structured with bullet points, and easy to understand.
            3. Create markdown headers for each section, each header should be concise, informative, and relevant to the content. Maximum 10 words.
            4. Just return the written content, no extra explanation needed.
        """)
        super().__init__(**kwargs)