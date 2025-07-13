import asyncio
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

class ChatGpt:
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or None
        self.model = model or "gpt-4o"

    async def stream(self, prompt: str):
        if not self.api_key:
            raise ValueError("OpenAI API key must be set before using the assistant.")
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in response:
            try:
                result = chunk.choices[0].delta.content or ""
                yield result
            except Exception as e:
                print(f"Error decoding chunk: {e}")
                continue
    
# Example usage
if __name__ == "__main__":
    import asyncio
    async def main():
        model = ChatGpt()
        async for response in model.stream("Who is the president of the United States?"):
            print(response, end="", flush=True)
    asyncio.run(main())