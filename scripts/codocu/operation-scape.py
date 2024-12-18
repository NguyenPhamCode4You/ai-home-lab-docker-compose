import json
import os
from jobs.UrlSummarizer import UrlSummarizer
import asyncio

from dotenv import load_dotenv
load_dotenv()

OLLAMA_URL      = "http://10.13.13.5:11434"
GENERAL_MODEL   = "gemma2:27b-instruct-q5_1"

url_summarizer = UrlSummarizer(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    fire_craw_api_key=os.getenv("FIRE_CRAW_API_KEY"),
    log_folder=os.path.join(os.path.dirname(__file__), "operation-scape-logs")
)

urls = [
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886365/IMOS+-+Compliance+with+IMO+2020",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886358/IMOS+-+Piracy+and+ECA+Routing",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886715/IMOS+-+Allocating+Expenses+to+a+Voyage",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886855/IMOS+-+Creating+a+New+Voyage+in+Operations",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886506/IMOS+-+Rescheduling+Voyages",
]

async def stream_urls(question, urls):
    """
    Stream summarized responses for a given question from a list of URLs.
    """
    for url in urls:
        try:
            # Stream responses from the summarizer
            async for agent_chunk in url_summarizer.stream(question, url):
                yield agent_chunk

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            continue

async def main():
    """
    Main function to run the async generator and process its output.
    """
    question = (
        "What are the key points to consider when rescheduling a voyage? "
        "Explain in detail, making sure to include all necessary steps."
    )

    # Consume the async generator
    async for response in stream_urls(question, urls):
        if (len(response) > 1000):
            continue
        try:
            response_data = json.loads(response)
            agent_response = response_data.get("response", "")
            
            # Skip if response is empty
            if not agent_response:
                continue
            print(agent_response, end="", flush=True)
        except Exception as e:
            print(f"Error processing response: {e}")
            continue

# Run the script
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")