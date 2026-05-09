import json
import os
import httpx

from dotenv import load_dotenv
load_dotenv()

default_token_length = int(os.getenv("TOKENS_LENGTH", 28000))

class Ollama:
    def __init__(self, url: str = None, model: str = None, num_ctx: int = None, num_predict: int = None):
        self.url = url or os.getenv("OLLAMA_URL") or None
        self.model = model or os.getenv("OLLAMA_GENERAL_MODEL") or None
        self.num_ctx = num_ctx or default_token_length
        self.num_predict = num_predict or -1  # -1 = unlimited output length

    async def stream(self, prompt: str):
        if not self.url or not self.model:
            raise ValueError("URL and model must be set before using the assistant.")
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", f"{self.url}/api/generate", json={"model": self.model, "prompt": prompt, "options": {"num_ctx": self.num_ctx, "num_predict": self.num_predict}}) as response:
                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line).get("response", "")
                    except Exception as e:
                        print(f"Error decoding chunk: {e}")
                        continue

# Example usage
if __name__ == "__main__":
    import asyncio
    async def main():
        model = Ollama()
        async for response in model.stream("Who is the president of the United States?"):
            print(response, end="", flush=True)
    asyncio.run(main())