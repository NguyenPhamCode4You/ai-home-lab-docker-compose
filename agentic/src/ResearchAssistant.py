from .agents.Task import Task
from .agents.tools.Crawler import Crawler
from .agents.ResearchTopicAnalyzer import ResearchTopicAnalyzer

class ResearchAssistant():
    def __init__(self,
            llm_topic_analyzer: Task = None,
        ):
        self.crawler = Crawler()
        self.topic_analyzer = llm_topic_analyzer or ResearchTopicAnalyzer()

    async def stream(self, question: str = None, conversation_history: list = None):
        async for response_chunk in self.topic_analyzer.stream(question=question):
            yield response_chunk

