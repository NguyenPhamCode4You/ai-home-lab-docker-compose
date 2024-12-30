from .Task import Task
from .models.Ollama import Ollama

class SimpleEntityExtractor(Task):
    def __init__(self, entity: str = 'question', **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "simple-entity-extractor")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", f"""
            Extract the {entity} from the context below.
            {"{context}"}
            Important:
            - If no {entity} can be found, just return "No data found".
            - Return only the {entity} separated with a new line, no extra information or explanation needed.
        """)
        super().__init__(**kwargs)