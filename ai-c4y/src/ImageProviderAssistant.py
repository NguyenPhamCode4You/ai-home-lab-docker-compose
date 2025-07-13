import asyncio
from .agents.Task import Task
from .agents.models.Ollama import Ollama
from .agents.tools.ImageProvider import ImageProvider

class ImageProviderAssistant():
    def __init__(self,
            llm_model: Task = None,
        ):
        self.model = llm_model or Ollama()

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        count_images = await Task(
            llm_model=self.model,
            instruction_template="How many images user want to see? Return only the number, default is 1, maximum is 5. User: {question}.",
        ).run(context=context, question=question, conversation_history=conversation_history)

        image_provider = ImageProvider(count=int(count_images))

        search_topic = await Task(
            llm_model=self.model,
            instruction_template="Rewrite the user question into a query for searching the desired images. Expanse the query domain to includes better output. Return only the search query. User: {question}.",
        ).run(context=context, question=question, conversation_history=conversation_history)

        async for image_chunk in image_provider.stream(prompt=search_topic):
            yield image_chunk

            

