import os
from serpapi import GoogleSearch

from dotenv import load_dotenv
load_dotenv()

class SerpUrlProvider:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERP_API_KEY") or None

    def run(self, query, num_results=10):
        try:
            params = {
                "engine": "google",
                "q": query,
                "num": num_results,
                "api_key": self.api_key
            }
            # Perform the search
            search = GoogleSearch(params)
            results = search.get_dict()
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
        
if __name__ == "__main__":
    serp = SerpUrlProvider()
    results = serp.run("Python programming", num_results=5)
    for result in results:
        print(f"{result['title']}: {result['url']}")