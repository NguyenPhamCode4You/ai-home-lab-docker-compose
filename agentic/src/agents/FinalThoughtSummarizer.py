from .Task import Task
from .models.Ollama import Ollama

class FinalThoughtSummarizer(Task):
    def __init__(self, llm_model: Task = None, context_chunk_size: int = None):
        super().__init__(
            task_name="final-thought-summarizer",
            llm_model=llm_model or Ollama(),
            context_chunk_size=context_chunk_size,
            instruction_template="""
            You are the final thought that reflect your previous answers to the user questions.
            Here is the user question: {question}
            Your previous answers to the user questions:
            {context}
            Generate one final answer that combines all the previous answers to the user questions as your best answer to the user question.
            """
        )