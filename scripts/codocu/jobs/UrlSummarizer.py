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
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the main content (e.g., from <p> tags or main article sections)
                paragraphs = soup.find_all('p')
                content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
                return content
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