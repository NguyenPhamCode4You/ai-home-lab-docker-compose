import json
import os
import httpx

from dotenv import load_dotenv
load_dotenv()

class LlamaServer:
    def __init__(self, url: str = None, n_predict: int = None, temperature: float = None):
        self.url = url or os.getenv("LLAMA_SERVER_URL") or None
        self.n_predict = n_predict or 512
        self.temperature = temperature or 0.8

    async def stream(self, prompt: str):
        if not self.url:
            raise ValueError("URL must be set before using the assistant.")
        
        # Prepare the request payload for llama-server
        payload = {
            "prompt": prompt,
            "n_predict": self.n_predict,
            "temperature": self.temperature,
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
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            response = await client.post(f"{self.url}/completion", json=payload)
            data = response.json()
            return data.get("content", "")

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_stream():
        server = LlamaServer()
        print("Testing stream completion:")
        async for response in server.stream("Who is the president of the United States?"):
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
        await test_stream()
        await test_chat()
        await test_non_stream()
    
    asyncio.run(main())
