import asyncio
from .agents.Task import Task
from .agents.tools.Crawler import Crawler
from .agents.models.Perplexity import Perplexity
from .agents.models.Serp import Serp
from .agents.ResearchTopicsLedger import ResearchTopicsLedger

class ResearchAssistant():
    def __init__(self,
            llm_topics_ledger: Task = None,
            llm_context_summarizer: Task = None,
            research_mode: str = "perplexity",
            allow_summarize_url: bool = False,
            topics_count: int = 3
        ):
        self.crawler = allow_summarize_url and Crawler() or None
        self.topic_ledger = llm_topics_ledger or ResearchTopicsLedger(topics_count=topics_count)
        self.researcher = Perplexity(crawler=self.crawler) if research_mode == "perplexity" else Serp(crawler=self.crawler)
        self.context_summarizer = llm_context_summarizer

    async def stream(self, question: str = None, conversation_history: list = None):
        topics_string = ""
        async for topic_ledger_chunk in self.topic_ledger.stream(question=question):
            yield topic_ledger_chunk
            topics_string += topic_ledger_chunk

        topics_parts = topics_string.split("**Research Contents:**\n")
        if len(topics_parts) > 1:
            topics_string = topics_parts[1]
            topics = topics_string.split("\n")
        else:
            topics = []

        topics = [topic for topic in topics if topic is not None and len(topic) > 0 and ":" in topic]
        research_result = ""

        if self.researcher is not None:
            for topic in topics:
                yield "\n\n"
                topic_name = f"\n## 📖 Section {topic.split(":")[0].replace("**", "").strip()}:\n"
                yield topic_name
                await asyncio.sleep(1)
                topic_description = f"\n**Description**: {topic.split(':')[1].replace("**", "").strip()}\n"
                yield topic_description
                yield "\n\n"
                research_result += topic_name
                research_prompt = f"""
                Provide a comprehensive answer for this topic: {topic}.
                Your answer should be written is a well-structured, informative bullet points format.
                Now, jump into the content directly.
                """
                async for research_chunk in self.researcher.stream(research_prompt):
                    yield research_chunk
                    research_result += research_chunk

        if self.context_summarizer is not None:
            async for summarizer_chunk in self.context_summarizer.stream(context=research_result, question=question):
                yield summarizer_chunk

            

