from .Task import Task
from .models.Ollama import Ollama

class KnowledgeCompression(Task):
    def __init__(self, max_char: int = 450):
        super().__init__(
            task_name="knowledge_compression",
            instruction_template=f"""
            Your task is to compress the given paragraph into a concise summary.
            - The summary should not exceed {max_char} characters.
            - The summary should be extremely concise and to the point.
            - The summary should contains a general purpose and encapsulates all important information of the paragraph.

            Return only the summary. No extra explaination is needed.
            Now, let's start with the paragraph:
            {"{context}"}
            """
        )