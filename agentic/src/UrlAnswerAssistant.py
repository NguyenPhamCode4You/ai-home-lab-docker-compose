from .agents.Task import Task
from .agents.SimpleEntityExtractor import SimpleEntityExtractor
from .agents.ContextAnswer import ContextAnswer
from .agents.tools.Crawler import Crawler

class UrlAnswerAssistant():
    def __init__(self,
            llm_url_extractor: Task = None,
            llm_question_extractor: Task = None,
            llm_context_answer: Task = None
        ):
        self.crawler = Crawler()
        self.url_extractor = llm_url_extractor or SimpleEntityExtractor("URLs")
        self.question_extractor = llm_question_extractor or SimpleEntityExtractor("user requests")
        self.context_answer = llm_context_answer or ContextAnswer()

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        urls_string = await self.url_extractor.run(context=question)
        questions_string = await self.question_extractor.run(context=question)
        if "No data found" in urls_string or "No data found" in questions_string:
            yield "Error while processing the request."
            return
        urls = [url for url in urls_string.split("\n") if url.strip()]
        for url in urls:
            yield "\n\n"
            yield f"\n📖 **Reading**: {url}\n"
            yield "\n\n"
            url_context = await self.crawler.run(url)
            async for context_chunk in self.context_answer.stream(context=url_context, question=questions_string):
                yield context_chunk

            

