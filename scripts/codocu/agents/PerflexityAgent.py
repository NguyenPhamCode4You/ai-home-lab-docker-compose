import asyncio
import datetime
import json
import os
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
        log_folder: str = None,
        url_summarizer = None
    ):
        self.api_key = api_key
        if log_folder:
            os.makedirs(log_folder, exist_ok=True)
        self.log_folder = log_folder
        self.url_summarizer = url_summarizer

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
                citations, final_text = await self._clean_json_response(response_data)

                # ---------------------------------------
                # 3. Generate the final analysis
                # ----------------------------------------
                self.write_to_log(question, final_text)

                async for token in stream_batch_words(final_text, batch_size=3, stream_delay=0.05):
                    yield token

                if citations and self.url_summarizer:
                    citations = citations[:3]  # Limit to 3 citations
                    for url_index, citation in enumerate(citations):
                        try:
                            yield json.dumps({"response": f"\n\n📖 {url_index + 1}. Summarizing content from {citation}...\n\n"})
                            await asyncio.sleep(0.5)
                            async for agent_chunk in self.url_summarizer.stream(question, citation):
                                yield agent_chunk
                        except Exception as e:
                            yield json.dumps({"response": f"\n\n❌ Summary error: {e}\n\n"})

            except httpx.HTTPStatusError as exc:
                raise RuntimeError(f"HTTP error: {exc.response.status_code} - {exc.response.text}")
            except Exception as exc:
                raise RuntimeError(f"Unexpected error: {exc}")
            
    def write_to_log(self, question, content):
        if not self.log_folder:
            return
        final_file_name = f"perflexity-{''.join(e for e in question if e.isalnum())}.md"
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(self.log_folder, datetime_str)
        log_file_path = os.path.join(folder_path, final_file_name)
        os.makedirs(folder_path, exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as file:
            file.write(content)
            file.flush()
    
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

        return citations, f"{content}\n{formatted_citations}"
    

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
            