import json
from typing import Optional, Callable, Awaitable, Union, AsyncGenerator, Dict, Any
from pydantic import BaseModel, Field
import httpx

class Pipe:
    class Valves(BaseModel):
        bvms_rag_url: str = Field(
            default="http://10.13.13.2:8000/api/answer/stream",
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "bvms-rag-pipe"
        self.name = "BVMS RAG Pipe"
        self.valves = self.Valves()

    async def pipe(
        self,
        body: Dict[str, Any],
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Awaitable[None]]] = None,
        __event_call__: Optional[Callable[[dict], Awaitable[dict]]] = None,
    ) -> AsyncGenerator[str, None]:
        messages = body.get("messages", [])
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", self.valves.bvms_rag_url, json={"messages": messages}) as response:
                response.raise_for_status()  # Raise exception for HTTP errors
                async for chunk in response.aiter_bytes():
                    if chunk:
                        try:
                            # Try to decode the chunk as JSON
                            chunk_str = chunk.decode("utf-8")  # Decode bytes to string
                            json_chunk = json.loads(chunk_str)  # Parse the JSON string
                            
                            # # Extract the desired part of the JSON, e.g., 'response'
                            response_text = json_chunk.get("response", "")
                            yield response_text
                            
                        except json.JSONDecodeError as e:
                            # yield f"Error parsing chunk: {str(e)}"
                            yield f""
            
