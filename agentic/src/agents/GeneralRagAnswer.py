from .Task import Task
from .models.Ollama import Ollama

class GeneralRagAnswer(Task):
    def __init__(self, llm_model = None, context_chunk_size: int = None, max_context_tokens: int = 5500, allow_reflection: bool = False):
        super().__init__(
            task_name="general-rag-answer",
            context_chunk_size=context_chunk_size,
            max_context_tokens=max_context_tokens,
            allow_reflection=allow_reflection,
            llm_model=llm_model or Ollama(),
            instruction_template="""
            You are an intelligent RAG AI agent to assist users with their questions.
            Here is the user question: {question}

            First, analyze carefully the knowledge below to base your answer on. Consider only the relevant information to the question being asked.
            {context}

            ALWAYS generate a WELL-STRUCTURED, BULLET-POINT, ACCURATE and DETAILED, easy to understand answer to the question.
            Important:
            - Always base your answer on the retrieved knowledge.
            - You may enhance your response with factual support when possible.
            - If you could not find the answer, just say with "For more information, please consult [some source here]."

            Now, answer with confidence.
            """
        )