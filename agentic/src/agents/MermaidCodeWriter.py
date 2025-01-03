from .Task import Task
from .models.Ollama import Ollama

from .constants import OLLAMA_CODE_MODEL

class MermaidCodeWriter(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "mermaid-code-writer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama(model=OLLAMA_CODE_MODEL))
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
You are an intelligent mermaid markdown assistant that can help user create diagram basing on a given context.
{context}
{histories}
User question: {question}
Provide the markdown in mermaid language to create a diagram that best answers the user question.
TRY to be as simple in your code as possible.
Return markdown wrapped in ```mermaid ``` block, no explanation needed
Example of a good timeline diagram:
```mermaid
gantt
    title Timeline of Itinerary Items
    dateFormat  YYYY-MM-DD
    section Hamburg
    Arrival  :a1, 2024-11-29, 0d
    Departure: d1, 2024-12-02, 0d
    section Lisbon
    Arrival  :a2, 2024-12-07, 0d
    Departure: d2, 2024-12-08, 0d
```
            """)
        super().__init__(**kwargs)