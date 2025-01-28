import json
import os
import httpx

from dotenv import load_dotenv
load_dotenv()

class Ollama:
    def __init__(self, url: str = None, model: str = None, num_ctx: int = None):
        self.url = url or os.getenv("OLLAMA_URL") or None
        self.model = model or os.getenv("OLLAMA_GENERAL_MODEL") or None
        self.num_ctx = num_ctx or 2048

    async def stream(self, prompt: str):
        if not self.url or not self.model:
            raise ValueError("URL and model must be set before using the assistant.")
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", f"{self.url}/api/generate", json={"model": self.model, "prompt": prompt, "options": {"num_ctx": self.num_ctx}}) as response:
                async for chunk in response.aiter_bytes():
                    if (len(chunk) > 1000):
                        continue
                    try:
                        response = json.loads(chunk).get("response", "")
                        yield response
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