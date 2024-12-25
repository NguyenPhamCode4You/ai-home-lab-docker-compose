from .Task import Task
from .models.Ollama import Ollama

class SimpleEntityExtractor(Task):
    def __init__(self, entity: str = 'question'):
        super().__init__(
            task_name="simple-entity-extractor",
            llm_model=Ollama(),
            instruction_template=f"""
            Extract the {entity} from the context below.
            {"{context}"}
            Important:
            - If no {entity} can be found, just return "No data found".
            - Return only the {entity} seperated with a new line, no extra information or explanation needed.
            """
        )