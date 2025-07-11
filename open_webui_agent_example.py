import json
from typing import Optional, Callable, Awaitable, Union, AsyncGenerator, Dict, Any
from pydantic import BaseModel, Field
import httpx


class Pipe:
    class Valves(BaseModel):
        bvms_rag_url: str = Field(
            default="http://10.13.13.12:8001/api/answer/stream",
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "bvms-be-rag-pipe"
        self.name = "BVMS BE RAG Pipe"
        self.valves = self.Valves()

    async def pipe(
        self,
        body: Dict[str, Any],
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Awaitable[None]]] = None,
        __event_call__: Optional[Callable[[dict], Awaitable[dict]]] = None,
    ) -> AsyncGenerator[str, None]:
        messages = body.get("messages", [])
        # Set a custom timeout value
        timeout = httpx.Timeout(
            connect=20.0,  # Maximum time to establish a connection (in seconds)
            read=80.0,  # Maximum time to read data from the connection (in seconds)
            write=30.0,  # Maximum time to write data to the connection (in seconds)
            pool=60.0,  # Maximum time for acquiring a connection from the pool (in seconds)
        )
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream(
                "POST", self.valves.bvms_rag_url, json={"messages": messages}
            ) as response:
                response.raise_for_status()  # Raise exception for HTTP errors
                async for chunk in response.aiter_bytes():
                    yield chunk
