import datetime
import os
import re
from firecrawl import FirecrawlApp

from dotenv import load_dotenv
load_dotenv()

class FireCraw:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("FIRECRAW_API_KEY") or None
        if api_key:
            self.firecrawl = FirecrawlApp(api_key)
        log_folder = os.path.join(os.getcwd(), "logs", "crawler")
        os.makedirs(log_folder, exist_ok=True)
        self.log_folder = log_folder

    async def run(self, url: str):
        final_content = f"\n\n📖 **Crawling content from {url}**...\n\n"
        response = self.firecrawl.scrape_url(url=url, params={'formats': ['markdown']})
        document = response.get('markdown', '')
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
    
if __name__ == "__main__":
    import asyncio
    crawler = FireCraw()
    url = "https://climate.ec.europa.eu/eu-action/transport/reducing-emissions-shipping-sector/faq-maritime-transport-eu-emissions-trading-system-ets_en"
    asyncio.run(crawler.run(url))