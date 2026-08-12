"""OpenRouter model client — cloud fallback entry in the models_ladder.

Exposes ``async def stream(prompt) -> AsyncGenerator[str, None]`` with 429 /
backoff retry and provider ordering. This is the automatic cloud backstop.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

_CONCURRENCY = int(os.getenv("OPENROUTER_CONCURRENCY", "1"))
_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "8192"))
_PROVIDER_ORDER = [p.strip() for p in os.getenv("OPENROUTER_PROVIDER_ORDER", "").split(",") if p.strip()]
_NO_THINK = os.getenv("OPENROUTER_NO_THINK", "false").lower() in ("1", "true", "yes")


class OpenRouter:
    """Cloud model client with rate-limit backoff and a shared concurrency semaphore."""

    _semaphore: asyncio.Semaphore = None
    _concurrency: int = _CONCURRENCY

    @classmethod
    def set_concurrency(cls, n: int) -> None:
        cls._concurrency = max(1, n)
        cls._semaphore = asyncio.Semaphore(cls._concurrency)

    @classmethod
    def _get_semaphore(cls) -> asyncio.Semaphore:
        if cls._semaphore is None:
            cls._semaphore = asyncio.Semaphore(cls._concurrency)
        return cls._semaphore

    def __init__(self, api_key: str = None, model: str = None, max_retries: int = 8) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or None
        self.model = model or os.getenv("OPENROUTER_DEFAULT_MODEL") or "openai/gpt-4o-mini"
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
            "max_tokens": _MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }
        if _PROVIDER_ORDER:
            payload["provider"] = {"order": _PROVIDER_ORDER, "allow_fallbacks": True}
        if _NO_THINK:
            payload["include_reasoning"] = False

        for attempt in range(self.max_retries):
            try:
                async with self._get_semaphore():
                    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
                        async with client.stream("POST", url, json=payload, headers=headers) as response:
                            if response.status_code == 429:
                                retry_after = int(response.headers.get("retry-after", 2 ** attempt))
                                print(
                                    f"OpenRouter rate limited (429). Retrying in {retry_after}s "
                                    f"(attempt {attempt + 1}/{self.max_retries})...",
                                    file=sys.stderr,
                                )
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
                                except Exception as exc:  # noqa: BLE001
                                    print(f"Error decoding chunk: {exc}", file=sys.stderr)
                                    continue
                            return  # completed successfully
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 429 and attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    print(
                        f"OpenRouter rate limited (429). Retrying in {wait}s "
                        f"(attempt {attempt + 1}/{self.max_retries})...",
                        file=sys.stderr,
                    )
                    await asyncio.sleep(wait)
                else:
                    raise
        raise RuntimeError(f"OpenRouter request failed after {self.max_retries} retries due to rate limiting.")


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        model = OpenRouter()
        async for chunk in model.stream("Who is the president of the United States?"):
            print(chunk, end="", flush=True)

    asyncio.run(main())