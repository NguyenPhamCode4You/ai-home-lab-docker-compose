import json
import os
from jobs.UrlSummarizer import UrlSummarizer
import asyncio

from dotenv import load_dotenv
load_dotenv()

from jobs.UrlSummarizer import scrape_content

OLLAMA_URL      = "http://10.13.13.5:11434"
GENERAL_MODEL   = "gemma2:27b-instruct-q5_1"

url_summarizer = UrlSummarizer(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    fire_craw_api_key=os.getenv("FIRE_CRAW_API_KEY"),
    log_folder=os.path.join(os.path.dirname(__file__), "operation-scape-logs")
)

urls = [
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888271/IMOS+-+Laytime+Calculation",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887824/IMOS+-+Demurrage+Despatch+Rates",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/133988913/IMOS+-+Calculation+of+Allowed+Days+in+Laytime+Calculation",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/2115764394/IMOS+-+Consolidated+Port+Activities+view+in+Laytime",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887416/IMOS+-+Demurrage+Time+Bar+Task+List",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885673/IMOS+-+Demurrage+Time+Bar+Task+Generation",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/1881341961/IMOS+-+Demurrage+Time+Bar+Task+Case+Study",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887836/IMOS+-+Booking-Based+Laytime+Calculation+Setup",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887856/IMOS+-+Booking-Based+Laytime+Calculation",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887848/IMOS+-+FOB+Delivered+Cargo",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885486/IMOS+-+FOB+Voyage",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887868/IMOS+-+Demurrage+Allocation+Summary",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887864/IMOS+-+Demurrage+Commission",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887860/IMOS+-+Estimated+Demurrage",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/2346090641/IMOS+-+Demurrage+Summary+Bookings+List",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886381/IMOS+-+Demurrage+Summary+Bookings+-+Legacy",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/324043174/IMOS+-+Berth+Scheduling",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/360776417/IMOS+-+Setup+-+Berth+Scheduling",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/326598667/IMOS+-+Berth+Management+Activity",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886377/IMOS+-+Berth+Schedule",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887828/IMOS+-+Bunkering",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887928/IMOS+-+Bunkering+Workflows",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887920/IMOS+-+Alternate+Operator-Bunker+Department+Workflow",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885771/IMOS+-+Requirement-Driven+Bunker+Procurement",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/323977471/IMOS+-+Debunkering+Workflow",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/634290178/How+do+I+apply+Bunker+Scrubber+Premium+on+Vessel+Delivery+Bunker+Lifting",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887924/IMOS+-+Typical+Operator-Bunker+Department+Workflow",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886982/IMOS+-+Bunker+Requirement",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887948/IMOS+-+Bunker+Requirement+-+Operator+Tasks",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887944/IMOS+-+Bunker+Manager",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886978/IMOS+-+Bunker+Purchase",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887952/IMOS+-+Bunker+Invoice",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888341/IMOS+-+Bunker+Liftings",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64885876/IMOS+-+Paid+By+For+Account+Impacts",
    "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886642/IMOS+-+TC+Bunker+Lifting+Options"
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