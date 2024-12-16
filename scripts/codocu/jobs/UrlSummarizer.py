import json
import httpx
import requests
from bs4 import BeautifulSoup

class UrlSummarizer:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        Given the content from the following URL:
        {document}

        Assist the user with the following question: {question}

        Provide a detailed, well-structured, bullet-points answer based on the content from the url.
        Follow the format: - **Key point:** <Explaination>

        """

    async def scrape_content(self, url: str) -> str:
        """
        Asynchronously scrapes and extracts meaningful content from a URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            str: Extracted text content from the URL.
        """
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the main content (e.g., from <p> tags or main article sections)
                # Extract all content
                content = []

                # Optionally, you can add specific content
                headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                for heading in headings:
                    content.append(heading.text.strip())

                paragraphs = soup.find_all('p')
                for paragraph in paragraphs:
                    content.append(paragraph.text.strip())

                lists = soup.find_all(['ul', 'ol'])
                for lst in lists:
                    content.append(lst.text.strip())

                links = soup.find_all('a')
                for link in links:
                    content.append(link.get_text(strip=True))

                # Return joined content
                return "\n".join(content)
            
        except Exception as e:
            raise Exception(f"Failed to scrape URL {url}: {e}")

    async def stream(self, question: str, url: str):
        document = await self.scrape_content(url)
        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    async def run(self, question: str, url: str) -> str:
        document = await self.scrape_content(url)
        print(document)
        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            response = await client.post(
                url=self.url,
                json={"model": self.model, "prompt": str(prompt), "stream": False}
            )
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        return self._clean_json_response(response.json())

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response
    
# Run the FastAPI app
if __name__ == "__main__":
    import asyncio
    summarizer = UrlSummarizer(url="http://10.13.13.4:11434", model="gemma2:9b-instruct-q8_0")
    question = "What are the key points from this article?"
    url = "https://www.limecube.co/the-ultimate-guide-to-ai-agents"
    asyncio.run(summarizer.run(question, url))