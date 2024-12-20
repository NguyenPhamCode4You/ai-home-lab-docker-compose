import os

from models.Ollama import Ollama
from models.ChatGpt import ChatGpt

from tools.Crawler import Crawler
from tools.Job import Job

ollama = Ollama()
chatgpt = ChatGpt()
crawler = Crawler()

async def main():
    content_writer=Job(
        name="ContentWriter",
        model=ollama,
        instruction=""" 
        Using markdown, rewrite the content below in your own words. {context}
        Important:
        - Do NOT omit any important information. However Do NOT include noise or irrelevant information, like: ads, comments, page navigation, hyberlink, citations, references.
        - Keep the content clear, detailed, well-structured with bullet points, and easy to understand.
        - Just return the written content, no extra explanation needed.
        """
    )
    # url_content = await crawler.craw("https://en.wikipedia.org/wiki/Python_(programming_language)")
    file_path = "C:\\Users\\niche\\ai-home-lab-docker-compose\\agentic\\logs\\crawler\\2024-12-20\\firecraw-2024-12-20-httpsenwikipediaorgwikiPythonprogramminglanguage.md"
    with open(file_path, "r", encoding="utf-8") as file:
        url_content = file.read()

    async for chunk in content_writer.stream(url_content):
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
