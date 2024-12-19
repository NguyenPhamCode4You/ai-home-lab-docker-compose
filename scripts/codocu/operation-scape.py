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
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885898/IMOS+-+Voyages",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886847/IMOS+-+Voyage+Manager",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885781/IMOS+-+Cargo+Handling",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886851/IMOS+-+Voyage+Manager+Map+View",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885806/IMOS+-+Activity+Log",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887552/IMOS+-+Activity+Reports",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885788/IMOS+-+Agents+and+Notices",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887306/IMOS+-+Berth+Management",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887022/IMOS+-+Deviation+Estimate",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886492/IMOS+-+Voyage+Instructions+-+Voyage",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886127/IMOS+-+P+L+-+Voyage",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886525/IMOS+-+P+L+Calculation+Options",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/806912219/Apply+Adjust+Portion+Off+Hire+Calculation",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886131/IMOS+-+Invoices+-+Voyage",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888094/IMOS+-+Port+Activities",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886369/IMOS+-+Port+Expenses+Summary",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886765/IMOS+-+Port+Expense",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887872/IMOS+-+Voyage+Bunkers",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/695500848/IMOS+-+Add+New+Bunker+Type+to+Voyage",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887880/IMOS+-+Voyage+Expenses+Rebill+Management",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886261/IMOS+-+CP+Quantity+Details",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/3352068217/IMOS+-+Deviation+TCE",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887640/IMOS+-+Freight+Invoice",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885932/IMOS+-+Performance+Reporting+-+Operations",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/391905898/IMOS+-+Voyage+Bunker+Report",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887876/IMOS+-+Voyage+Other+Revenues+and+Expenses",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/660603544/IMOS+-+Rebilling+Different+Rebill+Type+Items",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885729/IMOS+-+Expense+Standards",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885720/IMOS+-+Standard+Expenses",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/2054979777/Rebill+for+FDA+port+expense",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888345/IMOS+-+Ledger+Expense+Setup",
    
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
        "Provide a thoughtful and detailed analysis of how a maritime voyage is created and managed."
        "Explain in detail, making sure to include all necessary information in a well-structured bullet-points."
        "If no information is related to the question, please return 'No information available'."
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