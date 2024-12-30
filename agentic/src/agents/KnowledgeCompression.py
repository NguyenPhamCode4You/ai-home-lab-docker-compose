from .Task import Task

class KnowledgeCompression(Task):
    def __init__(self, max_char: int = 450, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "knowledge_compression")
        kwargs["instruction_template"] = kwargs.get("instruction_template", f"""
            Your task is to compress the given paragraph into a concise summary.
            - The summary should not exceed {max_char} characters.
            - The summary should be extremely concise and to the point.
            - The summary should contain a general purpose and encapsulate all important information of the paragraph.

            Return only the summary. No extra explanation is needed.
            Now, let's start with the paragraph:
            {"{context}"}
        """)
        super().__init__(**kwargs)