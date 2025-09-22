import json
import os
import httpx

from dotenv import load_dotenv
load_dotenv()

class LlamaServer:
    def __init__(self, url: str = None, n_predict: int = None, temperature: float = None, 
                 n_ctx: int = None, n_keep: int = None):
        self.url = url or os.getenv("LLAMA_SERVER_URL") or None
        self.n_predict = n_predict or 24000
        self.temperature = temperature or 0.8
        self.n_ctx = n_ctx or 32000  # Context window size (default 4K)
        self.n_keep = n_keep or -1  # Number of tokens to keep from prompt (-1 = keep all)

    async def stream(self, prompt: str):
        if not self.url:
            raise ValueError("URL must be set before using the assistant.")
        
        # Prepare the request payload for llama-server
        payload = {
            "prompt": prompt,
            "n_predict": self.n_predict,
            "temperature": self.temperature,
            "n_ctx": self.n_ctx,
            "n_keep": self.n_keep,
            "stream": True
        }
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", f"{self.url}/completion", json=payload) as response:
                async for chunk in response.aiter_bytes():
                    if len(chunk) <= 1:
                        continue
                    try:
                        # Parse the SSE data format used by llama-server
                        chunk_str = chunk.decode('utf-8').strip()
                        if chunk_str.startswith('data: '):
                            json_str = chunk_str[6:]  # Remove 'data: ' prefix
                            if json_str == '[DONE]':
                                break
                            data = json.loads(json_str)
                            content = data.get("content", "")
                            if content:
                                yield content
                    except Exception as e:
                        print(f"Error decoding chunk: {e}")
                        continue

    async def chat(self, messages: list):
        """Chat completion endpoint for llama-server"""
        if not self.url:
            raise ValueError("URL must be set before using the assistant.")
        
        payload = {
            "messages": messages,
            "n_predict": self.n_predict,
            "temperature": self.temperature,
            "n_ctx": self.n_ctx,
            "n_keep": self.n_keep,
            "stream": True
        }
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", f"{self.url}/v1/chat/completions", json=payload) as response:
                async for chunk in response.aiter_bytes():
                    if len(chunk) <= 1:
                        continue
                    try:
                        chunk_str = chunk.decode('utf-8').strip()
                        if chunk_str.startswith('data: '):
                            json_str = chunk_str[6:]
                            if json_str == '[DONE]':
                                break
                            data = json.loads(json_str)
                            choices = data.get("choices", [])
                            if choices and "delta" in choices[0]:
                                content = choices[0]["delta"].get("content", "")
                                if content:
                                    yield content
                    except Exception as e:
                        print(f"Error decoding chunk: {e}")
                        continue

    async def generate_non_stream(self, prompt: str):
        """Non-streaming completion for llama-server"""
        if not self.url:
            raise ValueError("URL must be set before using the assistant.")
        
        payload = {
            "prompt": prompt,
            "n_predict": self.n_predict,
            "temperature": self.temperature,
            "n_ctx": self.n_ctx,
            "n_keep": self.n_keep,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            response = await client.post(f"{self.url}/completion", json=payload)
            data = response.json()
            return data.get("content", "")

# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_stream(n_predict=102000):
        server = LlamaServer()
        print("Testing stream completion:")
        async for response in server.stream("Write me a simple snake game in python?"):
            print(response, end="", flush=True)
        print("\n")
    
    async def test_large_context():
        # Example with increased context length
        server = LlamaServer(
            n_ctx=128000,     # 128K context window
            n_keep=-1,      # Keep all tokens from prompt
            n_predict=16000  # Generate up to 16K tokens
        )
        print("Testing stream completion with 128K context:")
        
        # Read prompt from file
        try:
            with open(".\\src\\agents\\models\\long-text.txt", "r", encoding="utf-8") as f:
                prompt = f.read()
            print(f"Loaded prompt with {len(prompt)} characters")
        except FileNotFoundError:
            print("Warning: ./long-text.txt not found")
            return
        
        async for response in server.stream(prompt):
            print(response, end="", flush=True)
        print("\n")
    
    async def test_chat():
        server = LlamaServer()
        print("Testing chat completion:")
        messages = [
            {"role": "user", "content": "Hello, how are you?"}
        ]
        async for response in server.chat(messages):
            print(response, end="", flush=True)
        print("\n")
    
    async def test_non_stream():
        server = LlamaServer()
        print("Testing non-stream completion:")
        response = await server.generate_non_stream("What is the capital of France?")
        print(response)
    
    async def main():
        # await test_stream()
        await test_large_context()
        # await test_chat()
        # await test_non_stream()
    
    asyncio.run(main())
