import asyncio
import json
import re
import httpx
from typing import List
import requests
from serpapi import GoogleSearch

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class PerflexityAgent:
    def __init__(
        self,
        api_key: str = None,
    ):
        self.api_key = api_key

    async def stream(self, question: str, messages: List[dict] = None):
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "stream": False,
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{"role": "user", "content": question}],
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()

                # Parse the response and clean the final text
                response_data = response.json()
                final_text = await self._clean_json_response(response_data)

                async for token in stream_batch_words(final_text, batch_size=3, stream_delay=0.05):
                    yield token

            except httpx.HTTPStatusError as exc:
                raise RuntimeError(f"HTTP error: {exc.response.status_code} - {exc.response.text}")
            except Exception as exc:
                raise RuntimeError(f"Unexpected error: {exc}")
    
    async def _clean_json_response(self, response_data: dict) -> str:
        """
        Extract and format the message content and citations from the API response.
        """
        choices = response_data.get("choices", [])
        if not choices:
            return "No content available."

        # Extract message content
        message = choices[0].get("message", {})
        content = message.get("content", "No content provided.")

        # Format citations
        citations = response_data.get("citations", [])
        formatted_citations = "\n**Citations:**\n" + "\n".join(citations) if citations else ""

        return f"{content}\n{formatted_citations}"
    

async def stream_batch_words(final_text: str, batch_size: int = 2, stream_delay: float = 0.1):
    # Use regex to capture words and whitespace, preserving newlines
    tokens = re.findall(r'\S+|\s+', final_text)
    
    batch = []
    
    for token in tokens:
        batch.append(token)
        
        # When batch reaches the desired size, yield it as a JSON response
        if len(batch) >= batch_size:
            yield json.dumps({"response": "".join(batch)})
            batch = []  # Reset the batch
            await asyncio.sleep(stream_delay)
        
        # If there's still leftover tokens, yield them after finishing the loop
    if batch:
        yield json.dumps({"response": "".join(batch)})
    
    await asyncio.sleep(stream_delay)
            