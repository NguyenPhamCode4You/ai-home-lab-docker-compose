import asyncio
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

class ChatGpt:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or None
        self.client = OpenAI(api_key=api_key)

    async def stream(self, prompt: str):
        response = self.client.chat.completions.create(
            model='gpt-4o',
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
    
    async def run(self, prompt: str):
        final_text = ""
        async for response_text in self.stream(prompt):
            final_text += response_text
        return final_text
            
# Example usage
if __name__ == "__main__":
    import asyncio
    async def main():
        model = ChatGpt()
        async for response in model.stream("Who is the president of the United States?"):
            print(response, end="", flush=True)
    asyncio.run(main())