import asyncio
import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

class Gemini:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or None
        genai.configure(api_key=api_key)

    async def stream(self, prompt: str):
        if not self.api_key:
            raise ValueError("Gemini API key must be set before using the assistant.")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            yield chunk

if __name__ == "__main__":
    import asyncio
    async def main():
        model = Gemini()
        async for response in model.stream("Who is the president of the United States?"):
            print(response, end="", flush=True)
    asyncio.run(main())