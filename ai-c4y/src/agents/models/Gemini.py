import asyncio
import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

class Gemini:
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or None
        self.model = model or "gemini-1.5-flash"
        genai.configure(api_key=self.api_key)

    async def stream(self, prompt: str):
        if not self.api_key:
            raise ValueError("Gemini API key must be set before using the assistant.")

        loop = asyncio.get_running_loop()
        queue = asyncio.Queue()

        def _run_sync():
            try:
                model = genai.GenerativeModel(self.model)
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    try:
                        text = chunk.text
                        if text:
                            loop.call_soon_threadsafe(queue.put_nowait, text)
                    except Exception:
                        pass
            except Exception as e:
                loop.call_soon_threadsafe(queue.put_nowait, f"\n\n⚠️ Gemini error: {e}\n\n")
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)

        thread = asyncio.to_thread(_run_sync)
        asyncio.ensure_future(thread)

        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

if __name__ == "__main__":
    import asyncio
    async def main():
        model = Gemini()
        async for response in model.stream("Can you write me a 400 words poem?"):
            print(response, end="", flush=True)
    asyncio.run(main())