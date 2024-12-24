from .Task import Task
from .models.Ollama import Ollama

class ContextSummarizer(Task):
    def __init__(self, max_char: int = 250, llm_model: Task = None, context_chunk_size: int = 6000):
        super().__init__(
            task_name="context-summarizer",
            llm_model=llm_model or Ollama(),
            context_chunk_size=context_chunk_size,
            instruction_template=f"""
            Your task is to summarize the given paragraph. 

            - The summary should be concise and should contain the main purpose of the paragraph.
            - The summary should not exceed {max_char} characters. 

            Return only the summary. No extra explaination is needed.
            Now, let's start with the paragraph:
            {"{context}"}
            """
        )