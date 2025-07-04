"""
Ollama AI client for generating code reviews
"""

import json
import httpx
from typing import AsyncGenerator


class OllamaAPI:
    """Handle Ollama AI interactions"""
    
    def __init__(self, ollama_url: str, model: str, num_ctx: int = 6122):
        self.ollama_url = ollama_url.rstrip('/')
        self.model = model
        self.num_ctx = num_ctx  # Configurable context window
        self.max_content_tokens = int(self.num_ctx * 0.8)  # Reserve 20% for response and overhead
    
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from Ollama"""
        if not self.ollama_url or not self.model:
            raise ValueError("URL and model must be set before using the assistant.")
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream(
                "POST", 
                f"{self.ollama_url}/api/generate", 
                json={
                    "model": self.model, 
                    "prompt": prompt, 
                    "options": {"num_ctx": self.num_ctx}
                }
            ) as response:
                async for chunk in response.aiter_bytes():
                    if len(chunk) > 1000:
                        continue
                    try:
                        response_data = json.loads(chunk).get("response", "")
                        yield response_data
                    except Exception as e:
                        print(f"Error decoding chunk: {e}")
                        continue
    
    async def generate_review(self, content: str, guidelines: str) -> str:
        """Generate a complete review by collecting all streaming chunks"""
        # Prepare content with guidelines, truncating if necessary
        prepared_prompt = self._prepare_content_for_review(content, guidelines)
        
        output = ''
        print("🤖 AI is generating review...")
        
        async for chunk in self.stream(prepared_prompt):
            if chunk:
                output += chunk
                print(chunk, end='', flush=True)  # Print chunk to console in real-time
        
        print("\n🤖 Review generation completed!")
        return output
    
    def _prepare_content_for_review(self, content: str, guidelines: str) -> str:
        """Prepare content for review, truncating if necessary to fit context window"""
        guidelines_tokens = self._estimate_tokens(guidelines)
        content_tokens = self._estimate_tokens(content)
        total_tokens = guidelines_tokens + content_tokens
        
        if total_tokens <= self.max_content_tokens:
            # Content fits, return as-is with guidelines at the end
            return f"{content}\n\n{guidelines}"
        
        # Content too large, need to truncate
        available_content_tokens = self.max_content_tokens - guidelines_tokens
        target_char_count = available_content_tokens * 4  # Convert back to characters
        
        if target_char_count <= 0:
            raise ValueError("Guidelines are too long to fit in context window")
        
        # Truncate content and add indication of truncation
        truncated_content = content[:target_char_count]
        
        # Try to truncate at a reasonable boundary (end of line)
        last_newline = truncated_content.rfind('\n')
        if last_newline > target_char_count * 0.8:  # If we can find a newline in the last 20%
            truncated_content = truncated_content[:last_newline]
        
        print(f"⚠️  Content truncated due to context window limits. Original: {content_tokens} tokens, Truncated: {self._estimate_tokens(truncated_content)} tokens")
        
        # Add truncation notice and guidelines
        result = f"{truncated_content}\n\n[... Content truncated due to length ...]\n\n{guidelines}"
        return result
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text string"""
        # Rough estimate: 4 characters per token on average
        return len(text) // 4
