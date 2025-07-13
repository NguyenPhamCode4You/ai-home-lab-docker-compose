import os
import asyncio
import re
import aiohttp
from dotenv import load_dotenv
load_dotenv()

class ImageProvider:
    def __init__(self, api_key: str = None, count: int = 1):
        self.api_key = api_key or os.getenv("SERP_API_KEY") or None
        self.count = count

    async def stream(self, prompt: str):
        if not self.api_key:
            yield ""
            return
        try:
            # Define the search parameters for image search
            params = {
                "engine": "google_images",
                "q": prompt,
                "num": self.count,  # Number of image results to fetch
                "api_key": self.api_key
            }
            url = "https://serpapi.com/search"
            
            # Send the request to SerpAPI
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        yield (f"Error: Received status code {response.status}")
                        return
                    results = await response.json()

            images_markdown = ""
            if "images_results" in results:
                for image_index, image in enumerate(results["images_results"][:self.count]):
                    title = image.get('title', '').strip()
                    title_cleaned = re.sub(r'\s+', ' ', title)  # Replace multiple spaces/newlines with a single space
                    url = image.get('original')
                    if title_cleaned and url:
                        images_markdown += f"![{title_cleaned}]({url}){'\n' if image_index == 0 else ' '}"

            async for token in stream_batch_words(images_markdown, batch_size=3, stream_delay=0.05):
                yield token

        except Exception as e:
            yield (f"Error during SerpAPI image search: {e}")

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
        serp = ImageProvider()
        async for response in serp.stream("Diagram of AI Agent Memory System Design"):
            print(response, end="", flush=True)

    asyncio.run(main())
