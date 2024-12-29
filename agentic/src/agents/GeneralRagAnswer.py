from .Task import Task

class GeneralRagAnswer(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "general-rag-answer")
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
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
            """)
        super().__init__(**kwargs)