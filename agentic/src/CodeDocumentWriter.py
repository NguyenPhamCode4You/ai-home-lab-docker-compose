from Task import Task
from models.Ollama import Ollama

from constants import OLLAMA_CODE_MODEL

class CodeDocumentWriter(Task):
    def __init__(self):
        super().__init__(
            task_name="code-document-writer",
            llm_model=Ollama(
                model=OLLAMA_CODE_MODEL
            ),
            instruction_template="""
            You are an expert in the field of software development. Your task is to write a detailed document about a code file.
            Your document should follow the below guidelines:

            1. First, give a brief general purpose of the code, using '# General Purpose' as the heading.
            2. Then, break down the code into main functions and describe the purpose of each function using the below format.

            ## [Numbering]. [Function name]
            [Code snippet]
            **Explanation**:
            [Explanation of the function]

            - Each function should have a clear and concise explanation of what it does.
            - Explaination should be detailed and easy to understand.

            Now, please write a detailed document about the code below:
            {context}
            """
        )