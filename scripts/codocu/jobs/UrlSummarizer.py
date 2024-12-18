import datetime
import json
import os
import re
import httpx
import requests
from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp

class UrlSummarizer:
    def __init__(self, 
            url: str = 'http://localhost:11434', 
            model: str = 'gemma2:9b-instruct-q8_0', 
            fire_craw_api_key: str = None,
            log_folder: str = None
        ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.base_prompt = """
        Given the content from the following URL:
        {document}

        Assist the user with the following question: {question}

        Provide a detailed, well-structured, bullet-points answer based on the content from the url.
        Follow the format: - **Key point:** <Explaination>

        """
        if fire_craw_api_key:
            self.firecrawl = FirecrawlApp(fire_craw_api_key)
        if log_folder:
            os.makedirs(log_folder, exist_ok=True)
        self.log_folder = log_folder

    async def stream(self, question: str, url: str):
        final_content = f"\n\n📖 **Crawling content from {url}**...\n\n"
        if self.firecrawl:
            response = self.firecrawl.scrape_url(url=url, params={'formats': ['markdown']})
            document = response.get('markdown', '')
        else:
            document = await scrape_content(url)
        
        final_content += document
        final_content += f"\n\n📖 **Summarizing content**...\n\n"

        prompt = self.base_prompt.format(document=document, question=question)
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    if len(chunk) > 1000:
                        continue
                    final_content += json.loads(chunk).get("response", "")
                    yield chunk

        # ---------------------------------------
        # 3. Generate the final analysis
        # ----------------------------------------
        self.write_to_log(url, final_content)

    def write_to_log(self, url, content):
        if not self.log_folder:
            return
        final_file_name = f"firecraw-{cleanFileName(url)}.md"
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(self.log_folder, datetime_str)
        log_file_path = os.path.join(folder_path, final_file_name)
        os.makedirs(folder_path, exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as file:
            file.write(content)
            file.flush()

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response
    
def cleanFileName(file_name: str) -> str:
    """
    Cleans a file name by keeping only alphanumeric characters,
    replacing spaces with dashes, and removing special characters.

    Args:
        file_name (str): The original file name.

    Returns:
        str: The cleaned file name.
    """
    # Replace spaces with dashes
    file_name = file_name.replace(" ", "-")
    # Remove non-alphanumeric characters except dashes
    file_name = re.sub(r'[^A-Za-z0-9\-]', '', file_name)
    # Ensure no double dashes
    file_name = re.sub(r'-+', '-', file_name)
    return file_name.strip("-")
    
async def scrape_content(url: str) -> str:
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
    
# if __name__ == "__main__":
#     import asyncio
#     summarizer = UrlSummarizer(url="http://10.13.13.4:11434", model="gemma2:9b-instruct-q8_0")
#     question = "What are the key points from this article?"
#     url = "https://climate.ec.europa.eu/eu-action/transport/reducing-emissions-shipping-sector/faq-maritime-transport-eu-emissions-trading-system-ets_en"
#     asyncio.run(summarizer.run(question, url))