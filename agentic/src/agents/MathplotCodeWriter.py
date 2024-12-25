from .Task import Task
from .models.Ollama import Ollama

from .constants import OLLAMA_CODE_MODEL

class MathplotCodeWriter(Task):
    def __init__(self):
        super().__init__(
            task_name="mathplot-code-writer",
            llm_model=Ollama(
                model=OLLAMA_CODE_MODEL
            ),
            instruction_template="""
            You are an intelligent matplotlib python assistant that can help user create simple charts basing on a given data.
            {context}
            User question: {question}
            Provide the code to create a chart that best answers the user question, in python using matplotlib.
            DO NOT include plt.show() in the code.
            TRY to be as simple in your code as possible.
            Return code wrapped in ```python ``` block, no explaination needed
            Your code:
            """
        )