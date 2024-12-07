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
        self.max_history_tokens_length = 6000
        self.agents = {}
        self.base_prompt = """
        You are an intelligent assistant that can help user complete complex tasks.
        To archeive this, you have access to the following agents:
        -----
        {agents}
        -----
        When you receive a question, you should anaylzye the question to determine wether you should forward the question to the agents or answer it yourself.
        Read the description of each agent to determine the right ones to use, you can also paraphrase the question to better match the agent's expertise.

        Follow the structure below to forward the question to an agent:
        👋 **[agent_name_1]**: [question 1] 👀
        👋 **[agent_name_2]**: [question 2] 👀
        
        You can also forward the question to multiple agents, just make sure to mention the agent's name in the right order.
        If user asks a question that is not related to any agent, or just want to chat, then you can answer the question yourself.

        Here are the previous questions and answers:
        {histories}

        Now, let's get started!
        -----
        User question: {question}
        -----

        """
    def set_max_history_tokens_length(self, max_history_tokens_length: int):
        self.max_history_tokens_length = max_history_tokens_length
        return self

    def add_agent(self, agent_name: str, agent_description: str, agent):
        self.agents[agent_name] = {"description": agent_description, "agent": agent}
        return self

    def get_agents_description(self):
        return "\n".join(
            [f"\n{agent_name}: {details['description']}\n" for agent_name, details in self.agents.items()]
        )
    
    def get_chat_history_string(self, histories: List[Message] = None) -> str:
        """
        Returns a string representation of the chat history, limited to the last N tokens.
        Each entry includes the role and the first 1800 characters of content.
        """
        histories = histories or []  # Use an empty list if histories is None

        # Calculate how many tokens we can extract starting from the end
        accumulated_tokens = 0
        selected_messages = []
        for message in reversed(histories):  # Start from the last message
            content_length = len(message.content[:1800])  # Restrict each message to 1800 characters
            if accumulated_tokens + content_length > self.max_history_tokens_length:
                break  # Stop adding messages when the limit is reached

            selected_messages.append(f"\n >> {message.role}: {message.content[:1800]}\n\n")
            accumulated_tokens += content_length

        # Reverse again to preserve the original chronological order
        return "".join(reversed(selected_messages))
    
    async def stream(self, question: str, messages: List[Message] = None):
        histories = self.get_chat_history_string(messages)
        print(f"Chat history: {histories}")
        prompt = self.base_prompt.format(agents=self.get_agents_description(), question=question, histories=histories)

        accumulated_response  = ""
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    try:
                        chunk_str = chunk.decode("utf-8")
                        accumulated_response += json.loads(chunk_str)["response"]
                        yield chunk
                    except Exception as e:
                        yield ""
                        continue

                # Split the response by the delimiter
                chunks = accumulated_response.split("👀")
                agent_questions = []
                for chunk in chunks:
                    if ":" in chunk:  # Ensure the chunk contains an agent and a question
                        parts = chunk.split(":", 1)  # Split into two parts: agent name and question
                        agent_name = parts[0].strip()  # Strip whitespace from the agent name
                        agent_question = parts[1].strip()   # Strip whitespace from the question

                        for aname, adetails in self.agents.items():
                            if aname in agent_name:
                                agent_name = aname
                                agent_questions.append((agent_name, agent_question))
                                break

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
                            accumulated_response += json.loads(agent_chunk)["response"]
                            yield agent_chunk
                    
                    except Exception as e:
                        yield ""
