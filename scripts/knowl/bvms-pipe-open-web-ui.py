"""
title: BVMS Knowledge Pipe
author: Nguyen Pha,
author_url: https://github.com/NguyenPhamCode4You
version: 0.1.0

This module defines a Pipe class that call BVMS RAG model to answer questions from the user.
"""

from typing import Optional, Callable, Awaitable, Union, Generator, Iterator, List
from pydantic import BaseModel, Field
import requests

class Pipe:
    class Valves(BaseModel):
        bvms_rag_url: str = Field(
            default="http://10.13.13.2:8000/api/answer",
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "bvms-rag-pipe"
        self.name = "BVMS RAG Pipe"
        self.valves = self.Valves()
        pass

    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
        __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Union[str, Generator, Iterator]:
        
        messages = body.get("messages", [])
        response = requests.post(self.valves.bvms_rag_url, json={"messages": messages})
        yield response.json()["answer"]