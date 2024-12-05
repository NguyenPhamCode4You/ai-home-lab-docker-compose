import asyncio
import json
import httpx
import requests
from typing import List, Optional

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class AssistantOrchestra:
    def __init__(
        self,
        url: str = "http://localhost:11434/api/generate",
        model: str = "gemma2:9b-instruct-q8_0"
    ):
        
        self.url = url
        self.model = model
        self.agents = {}
        self.base_prompt = """
        You are an intelligent assistant that can help with a variety of tasks.
        You have access to the following agents:
        -----
        {agents}
        -----
        When you receive a question, you should anaylzye the question to determine if you should forward it to the appropriate agent.
        Read the description of each agent to determine which one to use, base on user's question.
        
        If an agent should be use, include the agent's name in your answer.
        If user asks a question that is not related to any agent, you can answer the question yourself

        Now, let's get started!
        -----
        User question: {question}
        -----

        """

    def add_agent(self, agent_name: str, agent_description: str, agent):
        self.agents[agent_name] = {"description": agent_description, "agent": agent}

    def get_agents_description(self):
        return "\n".join(
            [f"\n{agent_name}: {details['description']}\n" for agent_name, details in self.agents.items()]
        )
    
    async def stream(self, question: str, messages: List[Message] = None):
        prompt = self.get_final_prompt(question, messages)
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    async def stream(self, question: str, messages: List[Message] = None):
        prompt = self.base_prompt.format(agents=self.get_agents_description(), question=question)

        print(f"Prompt: {prompt}")

        accumulated_response  = ""
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    try:
                        chunk_str = chunk.decode("utf-8")
                        accumulated_response += json.loads(chunk_str)["response"]
                        yield chunk
                    except Exception as e:
                        print(f"Error parsing chunk: {str(e)}")
                        yield ""
                        continue

                for agent_name, details in self.agents.items():
                    if agent_name in accumulated_response:
                        yield json.dumps({"response": f"\n\n### 🤖 {agent_name} agent answering ... \n\n\n"} )
                        await asyncio.sleep(1)
                        agent = details.get("agent")  # Safely get the agent object
                        if not agent:
                            yield ""  # If agent is missing, yield an empty string and continue
                            continue
                        
                        try:
                            async for agent_chunk in agent.stream(question, messages):
                                yield agent_chunk
                        except Exception as e:
                            yield ""  # Log or handle the exception if needed
                            continue
                    
                
