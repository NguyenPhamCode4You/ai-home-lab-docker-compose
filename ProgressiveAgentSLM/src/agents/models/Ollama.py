"""Ollama model client — local SLM endpoint.

Exposes ``async def stream(prompt) -> AsyncGenerator[str, None]`` via Ollama's
``/api/generate`` (with ``think`` + ``num_ctx`` / ``num_predict`` options). This
is the local-first entry in the ``models_ladder``.
"""
from __future__ import annotations

import json
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

default_token_length = int(os.getenv("TOKENS_LENGTH", 28000))


class Ollama:
    def __init__(
        self,
        url: str = None,
        model: str = None,
        num_ctx: int = None,
        num_predict: int = None,
        think: bool = False,
    ) -> None:
        self.url = url or os.getenv("OLLAMA_URL") or None
        self.model = model or os.getenv("OLLAMA_GENERAL_MODEL") or None
        self.num_ctx = num_ctx or default_token_length
        self.num_predict = num_predict or -1  # -1 = unlimited output length
        self.think = think

    async def stream(self, prompt: str):
        if not self.url or not self.model:
            raise ValueError("URL and model must be set before using the assistant.")
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream(
                "POST",
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "think": self.think,
                    "options": {"num_ctx": self.num_ctx, "num_predict": self.num_predict},
                },
            ) as response:
                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line).get("response", "")
                    except Exception as exc:  # noqa: BLE001
                        print(f"Error decoding chunk: {exc}", file=sys.stderr)
                        continue


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        model = Ollama()
        async for chunk in model.stream("Who is the president of the United States?"):
            print(chunk, end="", flush=True)

    asyncio.run(main())