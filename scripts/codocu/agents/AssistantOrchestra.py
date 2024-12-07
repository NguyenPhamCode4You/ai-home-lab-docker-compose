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
        👋 **[agent_name_1]**: [question 1]? 👀
        👋 **[agent_name_2]**: [question 2]? 👀
        
        You can also forward the question to multiple agents, just make sure to mention the agent's name in the right order.
        If user asks a question that is not related to any agent, or just want to chat, then you can answer the question yourself.

        Here are the previous questions and answers:
        {histories}

        Important:
        - Make sure to keep the conversation engaging and informative.
        - Always mention agent name EXACTLY when forwarding questions.

        Now, let's get started!
        -----
        User question: {question}
        -----

        """
        # Given the above context of previous QAs, you can also perform reasoning to break down the question into sub-questions and forward each of them to the appropriate agent. Remember to mention their name correctly.

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

                agent_questions = []

                for agent_name, agent_details in self.agents.items():
                    agent_mention_index = accumulated_response.find(f"{agent_name}")
                    if agent_mention_index == -1:
                        continue

                    agent_question = accumulated_response.split(f"{agent_name}")[-1].split("👀")[0]
                    if ":" not in agent_question or "?" not in agent_question:
                        continue

                    agent_questions.append((agent_name, agent_question, agent_mention_index))
                
                agent_questions = sorted(agent_questions, key=lambda x: x[2])
                conversation_content = []

                # Identify agent responses in accumulated_response
                for agent_name, agent_question, agent_mention_index in agent_questions:
                    agent_details = self.agents.get(agent_name, {})
                    agent = agent_details.get("agent")
                    agent_response_len = 0
                    
                    if not agent:
                        yield f"\n\n### ⚠️ Agent '{agent_name}' not found or unavailable.\n\n"
                        continue

                    yield json.dumps({"response": f"\n\n### 🤖 {agent_name}: {agent_question} ...\n\n"})
                    conversation_content.append(f"\n\n### 🤖 {agent_name}: ")
                    await asyncio.sleep(1)

                    try:
                        async for agent_chunk in agent.stream(agent_question, messages):
                            agent_response_len += len(json.loads(agent_chunk)["response"])
                            conversation_content.append(json.loads(agent_chunk)["response"])
                            yield agent_chunk
                    
                    except Exception as e:
                        yield ""

                conversation_content = "".join(conversation_content)

                if len(conversation_content) > 500:
                    final_thought_prompt = """
                    You are a final thought generator that validates wether the agents have answered the user's question correctly.
                    Dont need to give feedback on agent response structure, focus on validating the usefulness of the response.
                    User: {question}
                    Agents answer: {answers}
                    1. If the agents have answered the question correctly:
                    - Then you should provide a final thought to summarize the answers, no more than 150 words
                    - Be clear and concise in your response
                    2. f agents is not able to answer the question:
                    - You need to take responsibility and apologize to the user.
                    - Then go head and try to answer the question yourself.
                    Your response:
                    """.format(question=question, answers=conversation_content)

                    print(conversation_content)

                    await asyncio.sleep(2)
                    agent_names = ", ".join([agent_name for agent_name, _, _ in agent_questions])
                    yield json.dumps({"response": f"\n\n### 🤖 Thanks {agent_names}, lets recap on the answers ... \n\n"})
                    await asyncio.sleep(1)

                    async with httpx.AsyncClient() as client:
                        async with client.stream("POST", self.url, json={"model": self.model, "prompt": final_thought_prompt}) as response:
                            async for chunk in response.aiter_bytes():
                                yield chunk

