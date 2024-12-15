from serpapi import GoogleSearch

def search_with_serpapi(query, api_key, num_results=10):
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

# # Example usage
# if __name__ == "__main__":
#     API_KEY = ""  # Replace with your SerpAPI key
#     query = "The impact of AI on healthcare"

#     # Fetch results
#     results = search_with_serpapi(query, API_KEY)

#     # Display the results
#     for idx, result in enumerate(results, start=1):
#         print(f"Result {idx}:")
#         print(f"Title: {result['title']}")
#         print(f"URL: {result['url']}")
#         print(f"Snippet: {result['snippet']}\n")
