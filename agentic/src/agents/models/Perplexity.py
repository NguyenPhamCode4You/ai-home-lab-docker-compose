import asyncio
import os
import re
import httpx

from dotenv import load_dotenv
load_dotenv()

from .Ollama import Ollama

class Perplexity:
    def __init__(self, api_key: str = None, crawler = None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY") or None
        self.crawler = crawler

    async def stream(self, prompt: str):
        if not self.api_key:
            raise ValueError("Perflexity API key must be set before using the assistant.")
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "stream": False,
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            final_text = ""
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                final_text, citations = _clean_perplexity_json_response(response_data)
                async for token in stream_batch_words(final_text, batch_size=3, stream_delay=0.05):
                    yield token
            except Exception as exc:
                raise RuntimeError(f"Unexpected error: {exc}")
            
            if self.crawler is not None:
                citations = citations[:3]
                general_answer = Ollama()
                for url_index, url in enumerate(citations):
                    yield f"\n\n📖 **{url_index + 1}. Summarizing content from:** {url}...\n\n"
                    url_content = await self.crawler.run(url)
                    async for summary_chunk in general_answer.stream(f"For less than 250 words, summarize this content: {url_content}"):
                        yield summary_chunk
    
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

def _clean_perplexity_json_response(response_data: dict) -> str:
    """
    Extract and format the message content and citations from the API response.
    """
    choices = response_data.get("choices", [])
    if not choices:
        return "No content available."
    message = choices[0].get("message", {})
    content = message.get("content", "No content provided.")
    citations = response_data.get("citations", [])
    formatted_citations = "\n**Citations:**\n" + "\n".join(citations) if citations else ""
    return f"{content}\n{formatted_citations}", citations

# Example usage
if __name__ == "__main__":
    import asyncio
    async def main():
        model = Perplexity()
        async for response in model.stream("Who is the president of the United States?"):
            print(response, end="", flush=True)
    asyncio.run(main())