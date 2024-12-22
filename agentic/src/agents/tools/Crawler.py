import datetime
import os
import re
from bs4 import BeautifulSoup
import httpx
from firecrawl import FirecrawlApp

from dotenv import load_dotenv
load_dotenv()

class Crawler:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("FIRECRAW_API_KEY") or None
        if api_key:
            self.firecrawl = FirecrawlApp(api_key)
        log_folder = os.path.join(os.getcwd(), "logs", "crawler")
        os.makedirs(log_folder, exist_ok=True)
        self.log_folder = log_folder

    async def run(self, url: str):
        final_content = f"\n\n📖 **Crawling content from {url}**...\n\n"
        if self.firecrawl:
            response = self.firecrawl.scrape_url(url=url, params={'formats': ['markdown']})
            document = response.get('markdown', '')
        else:
            document = await scrape_content(url)
        final_content += document
        self.write_to_log(f"{url}", document)
        return final_content

    def write_to_log(self, url, content):
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")
        final_file_name = f"firecraw-{datetime_str}-{cleanFileName(url)}.md"
        folder_path = os.path.join(self.log_folder, datetime_str)
        log_file_path = os.path.join(folder_path, final_file_name)
        os.makedirs(folder_path, exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as file:
            file.write(content)
            file.flush()

def cleanFileName(file_name: str) -> str:
    file_name = file_name.replace(" ", "-")
    file_name = re.sub(r'[^A-Za-z0-9\-]', '', file_name)
    file_name = re.sub(r'-+', '-', file_name)
    return file_name.strip("-")
    
async def scrape_content(url: str) -> str:
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = []
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
            return "\n".join(content)
    except Exception as e:
        raise Exception(f"Failed to scrape URL {url}: {e}")
    
def RecursiveSplitLines(document: str, limit: int = 1000):
    lines = document.split("\n")
    paragraphs = []
    paragraph = ""
    for line in lines:
        if len(paragraph) + len(line) + 1 > limit:
            if len(paragraph) > 0:
                paragraphs.append(paragraph)
            paragraph = f"{line}\n"
        else:
            paragraph += f"{line}\n"
    if len(paragraph) > 0:
        paragraphs.append(paragraph)
    return paragraphs
    
if __name__ == "__main__":
    import asyncio
    crawler = Crawler()
    url = "https://climate.ec.europa.eu/eu-action/transport/reducing-emissions-shipping-sector/faq-maritime-transport-eu-emissions-trading-system-ets_en"
    asyncio.run(crawler.run(url))