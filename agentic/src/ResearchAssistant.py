import asyncio
from .agents.Task import Task
from .agents.ResearchTopicsLedger import ResearchTopicsLedger
from .agents.models.Ollama import Ollama
from .agents.FinalThoughtSummarizer import FinalThoughtSummarizer
from .agents.tools.ImageProvider import ImageProvider

class ResearchAssistant():
    def __init__(self,
            llm_model: Task = None,
            llm_topics_ledger: Task = None,
            topics_count: int = 3,
            llm_summarizer: Task = None,
            image_provider: Task = None,
        ):
        self.topic_ledger = llm_topics_ledger or ResearchTopicsLedger(topics_count=topics_count)
        self.model = llm_model or Ollama()
        self.summarizer = llm_summarizer or FinalThoughtSummarizer()
        self.image_provider = image_provider or ImageProvider()

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        topics_string = ""
        async for topic_ledger_chunk in self.topic_ledger.stream(question=question):
            yield topic_ledger_chunk
            topics_string += topic_ledger_chunk

        topics = []
        if "**Research Contents:**\n" in topics_string:
            topics_string = topics_string.split("**Research Contents:**\n", 1)[1]
        topics = [topic for topic in topics_string.split("\n") if ":" in topic and topic.strip()]
        research_result = ""
        for topic in topics:
            yield "\n\n"
            topic_name = f"\n## 📖 Section {topic.split(":")[0].replace("**", "").strip()}:\n"
            research_result += topic_name
            yield topic_name
            await asyncio.sleep(1)
            topic_description = f"\n**Description**: {topic.split(':')[1].replace("**", "").strip()}\n"
            yield topic_description
            yield "\n\n"
            await asyncio.sleep(1)
            if self.image_provider:
                async for image_chunk in self.image_provider.stream(prompt=topic):
                    yield image_chunk
            await asyncio.sleep(1)
            research_prompt = f"""
            Provide a comprehensive answer for this topic: {topic}.
            Your answer should be written is a well-structured, informative bullet points format.
            Now, jump into the content directly.
            """
            async for research_chunk in self.model.stream(research_prompt):
                yield research_chunk
                research_result += research_chunk

        summarizer_header = f"\n\n## 🎯 Final Revision on this topic:\n\n"
        yield summarizer_header
        async for summarizer_chunk in self.summarizer.stream(context=research_result, question=question):
            yield summarizer_chunk

            

