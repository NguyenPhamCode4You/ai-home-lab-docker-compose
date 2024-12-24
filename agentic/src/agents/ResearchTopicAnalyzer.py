from .Task import Task
from .models.Ollama import Ollama

class ResearchTopicAnalyzer(Task):
    def __init__(self, llm_model: Task = None):
        super().__init__(
            task_name="final-thought-summarizer",
            llm_model=llm_model or Ollama(),
            instruction_template="""
            You are a specialist that breaks down user questions into smaller, more specific research topics for the Research Assistant to investigate.
            First, start with providing a brief answer to the user's question.
            Then, list the main topics that need to be researched to provide a more comprehensive answer.
            Seperate each topics with a new line with numberings, follow this format:
            **Research Topics:**
            1. Topic 1
            2. Topic 2
            User question: {question}
            """
        )