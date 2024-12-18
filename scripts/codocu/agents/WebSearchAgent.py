import asyncio
import datetime
import json
import os
import re
import httpx
from typing import List
from serpapi import GoogleSearch

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class WebSearchAgent:
    def __init__(
        self,
        url: str = "http://localhost:11434",
        model: str = "gemma2:9b-instruct-q8_0",
        serp_api_key: str = None,
        match_count: int = 5,
        url_summarizer = None,
        log_folder: str = None
    ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.serp_api_key = serp_api_key
        self.match_count = match_count
        self.url_summarizer = url_summarizer
        if log_folder:
            os.makedirs(log_folder, exist_ok=True)
        self.log_folder = log_folder

    async def stream(self, question: str, messages: List[Message] = None):
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            yield json.dumps({"response": f"\n\n🔍 Searching for relevant urls ...\n\n"})
            try:
                urls_result = search_using_serp_api(question, self.serp_api_key, self.match_count)
            except Exception as e:
                yield json.dumps({"response": f"\n\n❌ Search for urls error: {e}\n\n"})
                return

            if not urls_result:
                yield json.dumps({"response": f"\n\n❌ No relevant urls found.\n\n"})
                return
            
            # ---------------------------------------
            # 1.Verbosely list the urls
            # ----------------------------------------
            for url_index, url_result in enumerate(urls_result):
                url_link = format_url_link(url_result)
                snippet = url_result.get("snippet", "No snippet available.")
                yield json.dumps({"response": f"🔗 {url_index + 1}. {url_link}: {snippet}\n"})
                await asyncio.sleep(0.25)

            yield json.dumps({"response": f"\n\n### 🤖 Start the reading process... \n\n\n"})

            # ---------------------------------------
            # 2. Summarize the content of each URL
            # ----------------------------------------
            final_analysis_content = ""
            for url_index, url_result in enumerate(urls_result):
                url_link = format_url_link(url_result)
                content_header = f"\n\n📖 {url_index + 1}. Summarizing content from {url_link}...\n\n"
                yield json.dumps({"response": content_header})
                final_analysis_content += content_header
                await asyncio.sleep(0.5)
                try:
                    async for agent_chunk in self.url_summarizer.stream(question, url_result.get("url")):
                        if len(agent_chunk) > 1000:
                            continue
                        final_analysis_content += json.loads(agent_chunk).get("response", "")
                        yield agent_chunk
                except Exception as e:
                    yield json.dumps({"response": f"\n\n❌ Failed to summarize for {url_link}: {e}\n\n"})
                    continue

                await asyncio.sleep(0.5)

            # ---------------------------------------
            # 3. Generate the final analysis
            # ----------------------------------------
            self.write_to_log(question, final_analysis_content)

    def write_to_log(self, question, content):
        if not self.log_folder:
            return
        final_file_name = f"websearch-{cleanFileName(question)}.md"
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(self.log_folder, datetime_str)
        log_file_path = os.path.join(folder_path, final_file_name)
        os.makedirs(folder_path, exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as file:
            file.write(content)
            file.flush()

def format_url_link(url_result):
    return f"[{url_result['title']}]({url_result['url']})"

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

def search_using_serp_api(query, api_key, num_results=10):
    """
    Uses SerpAPI to fetch search results for a given query.

    Args:
        query (str): The search query string.
        api_key (str): Your SerpAPI key.
        num_results (int): Number of results to fetch.

    Returns:
        list: A list of dictionaries containing URL and title information.
    """
    try:
        # Configure the search parameters
        params = {
            "engine": "google",
            "q": query,
            "num": num_results,
            "api_key": api_key
        }

        # Perform the search
        search = GoogleSearch(params)
        results = search.get_dict()

        # Extract relevant information from the results
        search_results = []
        if "organic_results" in results:
            for result in results["organic_results"]:
                search_results.append({
                    "title": result.get("title"),
                    "url": result.get("link"),
                    "snippet": result.get("snippet")
                })
        return search_results

    except Exception as e:
        print(f"Error during SerpAPI search: {e}")
        return []
        