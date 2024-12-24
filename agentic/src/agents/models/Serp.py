import os
import asyncio
import re
import aiohttp
from dotenv import load_dotenv
load_dotenv()

from .Ollama import Ollama

class Serp:
    def __init__(self, api_key: str = None, crawler = None):
        self.api_key = api_key or os.getenv("SERP_API_KEY") or None
        self.general_answer = Ollama()
        self.crawler = crawler

    async def stream(self, prompt: str):
        async for general_answer_chunk in self.general_answer.stream(f"Provide comprehensive answer for this topic: {prompt}"):
            yield general_answer_chunk
        try:
            params = {
                "engine": "google",
                "q": prompt,
                "num": 5,
                "api_key": self.api_key
            }
            url = "https://serpapi.com/search"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        yield (f"Error: Received status code {response.status}")
                    results = await response.json()

            search_results = []
            if "organic_results" in results:
                for result in results["organic_results"]:
                    search_results.append(result.get("link"))
            citation_string = f"\n**Citations:**\n{"\n".join(search_results)}" 
            async for token in stream_batch_words(citation_string, batch_size=3, stream_delay=0.05):
                yield token

            if self.crawler is not None:
                topics_parts = citation_string.split("\n**Citations:**\n")
                if len(topics_parts) > 1:
                    topics_string = topics_parts[1]
                    topics = topics_string.split("\n")
                else:
                    topics = []
                citations = [topic for topic in topics if topic is not None and len(topic) > 0 and ":" in topic]
                citations = citations[:3]
                for url in citations:
                    yield f"\n\n📖 **Summarizing content from {url}**...\n\n"
                    url_content = await self.crawler.run(url)
                    url_summarize_prompt = f"For less than 250 words, summarize this content: {url_content}"
                    async for summary_chunk in self.general_answer.stream():
                        yield summary_chunk

        except Exception as e:
            yield (f"Error during SerpAPI search: {e}")
        
async def stream_batch_words(final_text: str, batch_size: int = 2, stream_delay: float = 0.1):
    # Use regex to capture words and whitespace, preserving newlines
    tokens = re.findall(r'\S+|\s+', final_text)
    batch = []
    for token in tokens:
        batch.append(token)
        if len(batch) >= batch_size:
            yield "".join(batch)
            batch = []  # Reset the batch
            await asyncio.sleep(stream_delay)
    # If there's still leftover tokens, yield them after finishing the loop
    if batch:
        yield "".join(batch)
    await asyncio.sleep(stream_delay)

if __name__ == "__main__":
    async def main():
        serp = Serp()
        async for response in serp.stream("What is python?"):
            print(response, end="", flush=True)

    asyncio.run(main())
