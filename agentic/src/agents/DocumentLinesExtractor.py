from .Task import Task
from .models.Ollama import Ollama

class DocumentLinesExtractor(Task):
    def __init__(self, line_delimiter="\nVNAGL\n"):
        super().__init__(
            task_name="document-lines-extractor",
            llm_model=Ollama(),
            instruction_template=f"""
            Your task is to extract important lines from the given paragraph. One line can contains 1-3 sentences. 
            Seperate each line by "{line_delimiter}".

            1. Sentences in one line should be closely related to each other.
            2. Each line should not exceed 250 characters.
            3. Exception for code blocks, api urls, json object, xml, always put them in one line.

            Return only the important lines, selerated by "{line_delimiter}".
            No extra explaination is needed.

            Now, let's start with the paragraph:
            {"{context}"}
            """
        )