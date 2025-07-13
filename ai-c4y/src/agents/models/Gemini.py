import asyncio
import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

class Gemini:
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or None
        self.model = model or "gemini-1.5-flash"
        genai.configure(api_key=api_key)

    async def stream(self, prompt: str):
        if not self.api_key:
            raise ValueError("Gemini API key must be set before using the assistant.")
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            yield chunk.text

if __name__ == "__main__":
    import asyncio
    async def main():
        model = Gemini()
        async for response in model.stream("Can you write me a 400 words poem?"):
            print(response, end="", flush=True)
    asyncio.run(main())