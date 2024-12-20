import asyncio
import json
import httpx

class BrainLLM:
    def __init__(self, url: str = None, model: str = None, open_api_key: str = None, perplexity_api_key: str = None, prompt: str = None):
        self.url = url
        self.model = model
        self.open_api_key = open_api_key
        self.perplexity_api_key = perplexity_api_key
        self.prompt = prompt

    async def stream_ollama(self, question: str, document: str = None):
        if not self.url or not self.model:
            raise ValueError("URL and model must be set before using the assistant.")
        prompt = self.prompt.format(question=question, document=document or "")
        string_result = ""
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
                    try:
                        string_result += json.loads(chunk).get("response", "")
                    except Exception as e:
                        print(f"Error decoding chunk: {e}")
        return string_result, []

    async def stream_perplexity(self, question: str, document: str = None):
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
                citations, final_text = _clean_perplexity_json_response(response_data)

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
            

def _clean_perplexity_json_response(response_data: dict) -> str:
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