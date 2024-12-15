import json
import httpx
import requests
from bs4 import BeautifulSoup

class WebScrapeAnswerer:
    def __init__(self, url: str = 'http://localhost:11434', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        Given the content from the following URL:
        {document}

        First, produce a summary of the content to understand the context, no more than 200 words.

        Then, given the user's question: {question}
        Provide a concise, well-structured, bullet-points answer based on the content.

        """

    def scrape_content(self, url: str) -> str:
        """
        Scrapes and extracts meaningful content from a URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            str: Extracted text content from the URL.
        """
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the main content (e.g., from <p> tags or main article sections)
            paragraphs = soup.find_all('p')
            content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
            return content
        except Exception as e:
            raise Exception(f"Failed to scrape URL {url}: {e}")

    async def stream(self, question: str, url: str):
        document = self.scrape_content(url)
        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def run(self, question: str, url: str) -> str:
        document = self.scrape_content(url)
        prompt = self.base_prompt.format(document=document, question=question)
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": str(prompt), "stream": False}
        )
        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        # Clean and format the JSON response
        return self._clean_json_response(response.json())

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response
    
# import asyncio

# # Example usaged
# async def main():
#     url = "https://bmcmededuc.biomedcentral.com/articles/10.1186/s12909-023-04698-z"
#     question = "What are the main points of the article?"
#     web_scraper = WebScrapeAnswerer(
#         url="http://10.13.13.4:11434",
#     )

#     try:
#         async for agent_chunk in web_scraper.stream(question, url):
#             if len(agent_chunk) > 1000:
#                 continue
#             agent_response = json.loads(agent_chunk)["response"]
#             print(agent_response, end="", flush=True)  # Real-time console output
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(main())