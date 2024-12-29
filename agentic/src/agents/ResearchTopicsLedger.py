from .Task import Task
from .models.Ollama import Ollama

class ResearchTopicsLedger(Task):
    def __init__(self, llm_model: Task = None, topics_count: int = 3):
        super().__init__(
            task_name="research-topics-ledger",
            llm_model=llm_model or Ollama(),
            instruction_template=f"""
            You are a specialist that breaks down user questions into {topics_count} smaller, more specific research topics for the Research Assistant to investigate.
            First, start with providing a brief answer to the user's question, using "### Introduction:" as the header.
            Then, list the main topics that need to be researched to provide a more comprehensive answer.
            Separate each topics with a new line with numberings, follow this format:
            **Research Contents:**\n
            1. **Topic name 1**: description in 150 words maximum.
            2. **Topic name 2**: description in 150 words maximum.
            Remember to limit the topics to {topics_count}.
            User question: {"{question}"}
            """
        )