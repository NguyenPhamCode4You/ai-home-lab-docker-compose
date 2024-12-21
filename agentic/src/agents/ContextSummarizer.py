from Task import Task
from models.Ollama import Ollama

class ContextSummarizer(Task):
    def __init__(self):
        super().__init__(
            task_name="context-summarizer",
            llm_model=Ollama(),
            instruction_template="""
            Your task is to summarize the given paragraph. 

            - The summary should be concise and should contain the main purpose of the paragraph.
            - The summary should not exceed 250 characters. 

            Return only the summary. No extra explaination is needed.
            Now, let's start with the paragraph:
            {context}
            """
        )