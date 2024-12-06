import asyncio
import json
import re
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
        You are an intelligent assistant that can help user complete complex tasks.
        To archeive this, you have access to the following agents:
        -----
        {agents}
        -----
        When you receive a question, you should anaylzye the question to determine which agents you should forward the question to.
        Read the description of each agent to determine the right ones to use, you can also paraphrase the question to better match the agent's expertise.

        Follow the structure below to forward the question to an agent:
        👋 **[agent_name_1]**: [question 1] 👀
        👋 **[agent_name_2]**: [question 2] 👀
        
        You can also forward the question to multiple agents, just make sure to mention the agent's name in the right order.
        If user asks a question that is not related to any agent, then you can answer the question yourself.

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

                # Split the response by the delimiter
                chunks = accumulated_response.split("👀")
                agent_questions = []
                for chunk in chunks:
                    if ":" in chunk:  # Ensure the chunk contains an agent and a question
                        parts = chunk.split(":", 1)  # Split into two parts: agent name and question
                        agent_name = parts[0].strip()  # Strip whitespace from the agent name
                        question = parts[1].strip()   # Strip whitespace from the question

                        for aname, adetails in self.agents.items():
                            if aname in agent_name:
                                agent_name = aname
                                agent_questions.append((agent_name, question))
                                break

                print(f"Agent questions: {agent_questions}")
                
                # Identify agent responses in accumulated_response
                for agent_name, agent_question in agent_questions:
                    agent_details = self.agents.get(agent_name, {})
                    agent = agent_details.get("agent")
                    
                    if not agent:
                        yield f"\n\n### ⚠️ Agent '{agent_name}' not found or unavailable.\n\n"
                        continue

                    yield json.dumps({"response": f"\n\n### 🤖 {agent_name} answering to: {agent_question} ...\n\n"})
                    await asyncio.sleep(1)

                    try:
                        async for agent_chunk in agent.stream(agent_question, messages):
                            yield agent_chunk
                    
                    except Exception as e:
                        print(f"Error streaming from agent '{agent_name}': {e}")
                        yield f"\n\n### ⚠️ Error while '{agent_name}' was responding.\n\n"
                    
                    except Exception as e:
                        print(f"Error in main stream method: {e}")
                        yield ""
                    
                
