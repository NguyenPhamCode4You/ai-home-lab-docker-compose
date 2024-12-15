import asyncio
import json
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
    ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.serp_api_key = serp_api_key
        self.match_count = match_count
        self.url_summarizer = url_summarizer

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
            for url_index, url_result in enumerate(urls_result):
                url_link = format_url_link(url_result)
                yield json.dumps({"response": f"\n\n📖 {url_index + 1}. Summarizing content from {url_link}...\n\n"})
                await asyncio.sleep(0.5)
                try:
                    async for agent_chunk in self.url_summarizer.stream(question, url_result.get("url")):
                        if len(agent_chunk) > 1000:
                            continue
                        yield agent_chunk
                except Exception as e:
                    yield json.dumps({"response": f"\n\n❌ Failed to summarize for {url_link}: {e}\n\n"})
                    continue

                await asyncio.sleep(0.5)

    async def write_analysis(self, question: str, log_file_path: str):
        if not log_file_path:
            return print("No log file specified. Please set a log file to save the analysis.")
        try:
            with open(log_file_path, "w", encoding="utf-8") as file:
                file.write(f"\n\n## User question: {question}\n\n\n")
                async for agent_chunk in self.stream(question, []):
                    if len(agent_chunk) > 1000:
                        continue
                    try:
                        chunk = json.loads(agent_chunk).get("response", "")
                        file.write(chunk)
                        file.flush()  # Ensures real-time writing to the file
                        print(chunk, end="", flush=True)  # Real-time console output
                    except json.JSONDecodeError:
                        print(f"Invalid JSON received: {agent_chunk}")
                        continue
        except Exception as e:
            print(f"Error opening log file: {e}")     

def format_url_link(url_result):
    return f"[{url_result['title']}]({url_result['url']})"

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
        