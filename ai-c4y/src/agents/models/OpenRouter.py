import asyncio
import json
import os
import httpx

from dotenv import load_dotenv
load_dotenv()

class OpenRouter:
    # Global semaphore shared across all instances — limits concurrent requests to OpenRouter
    _semaphore: asyncio.Semaphore = None
    _semaphore_limit: int = 1

    @classmethod
    def _get_semaphore(cls) -> asyncio.Semaphore:
        if cls._semaphore is None:
            cls._semaphore = asyncio.Semaphore(cls._semaphore_limit)
        return cls._semaphore

    def __init__(self, api_key: str = None, model: str = None, max_retries: int = 8):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or None
        self.model = model or os.getenv("OPENROUTER_MODEL") or "openai/gpt-4o-mini"
        self.max_retries = max_retries

    async def stream(self, prompt: str):
        if not self.api_key:
            raise ValueError("OpenRouter API key must be set before using the assistant.")

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "stream": True,
            "messages": [{"role": "user", "content": prompt}],
        }

        for attempt in range(self.max_retries):
            try:
                async with self._get_semaphore():
                    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
                        async with client.stream("POST", url, json=payload, headers=headers) as response:
                            if response.status_code == 429:
                                retry_after = int(response.headers.get("retry-after", 2 ** attempt))
                                print(f"OpenRouter rate limited (429). Retrying in {retry_after}s (attempt {attempt + 1}/{self.max_retries})...")
                                await asyncio.sleep(retry_after)
                                continue
                            response.raise_for_status()
                            async for line in response.aiter_lines():
                                line = line.strip()
                                if not line or not line.startswith("data: "):
                                    continue
                                data = line[len("data: "):]
                                if data == "[DONE]":
                                    return
                                try:
                                    chunk = json.loads(data)
                                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                                    text = delta.get("content", "")
                                    if text:
                                        yield text
                                except Exception as e:
                                    print(f"Error decoding chunk: {e}")
                                    continue
                            return  # completed successfully
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    print(f"OpenRouter rate limited (429). Retrying in {wait}s (attempt {attempt + 1}/{self.max_retries})...")
                    await asyncio.sleep(wait)
                else:
                    raise
        raise RuntimeError(f"OpenRouter request failed after {self.max_retries} retries due to rate limiting.")

# Example usage
if __name__ == "__main__":
    import asyncio
    async def main():
        model = OpenRouter()
        async for response in model.stream("Who is the president of the United States?"):
            print(response, end="", flush=True)
    asyncio.run(main())
