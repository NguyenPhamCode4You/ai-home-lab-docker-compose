import asyncio
import json
import re
from fastapi import Request
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
            # yield json.dumps({"response": f"![Generated Image](https://sandrasoft.app/banner.png)"})
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

                def remove_special_chars(text):
                    return re.sub(r"[^a-zA-Z]+", ' ', text)

                for agent_name, agent_details in self.agents.items():
                    agent_name_formated = f"**{remove_special_chars(agent_name)}**"
                    
                    # Find all occurrences of agent_name_formated in accumulated_response
                    for match in re.finditer(re.escape(agent_name_formated), accumulated_response):
                        agent_mention_index = match.start()
                        
                        # Extract the part of the text after the agent's mention
                        agent_question_part = accumulated_response[agent_mention_index + len(agent_name_formated):]
                        
                        # Extract the question until the first occurrence of "👀" or end of string
                        agent_question = agent_question_part.split("👀")[0]
                        
                        # Check if the extracted text qualifies as a valid question
                        if ":" in agent_question and "?" in agent_question:
                            agent_questions.append((agent_name, agent_question.strip(), agent_mention_index))
                
                agent_questions = sorted(agent_questions, key=lambda x: x[2])
                conversation_content = []

                # Identify agent responses in accumulated_response
                for agent_name, agent_question, agent_mention_index in agent_questions:
                    await asyncio.sleep(3)
                    agent_details = self.agents.get(agent_name, {})
                    agent = agent_details.get("agent")
                    agent_response_len = 0
                    
                    if not agent:
                        yield f"\n\n### ⚠️ Agent '{agent_name}' not found or unavailable.\n\n"
                        continue

                    real_agent_question = agent_question
                    
                    if len(conversation_content) > 0:
                        additional_agent_context = "".join(conversation_content)
                        real_agent_question = f"**Addtional context that might be useful:**\n{additional_agent_context}\n**Finally, here is your question:** {real_agent_question}"
                        print(real_agent_question)
                    
                    yield json.dumps({"response": f"\n\n### 🤖 {agent_name} {agent_question} ...\n\n"})
                    conversation_content.append(f"\n### 🤖 {agent_name} ")
                    await asyncio.sleep(3)

                    try:
                        async for agent_chunk in agent.stream(real_agent_question, messages):
                            agent_response_len += len(json.loads(agent_chunk)["response"])
                            conversation_content.append(json.loads(agent_chunk)["response"])
                            yield agent_chunk
                    
                    except Exception as e:
                        yield ""

                await asyncio.sleep(3) # Wait for the agents to respond completely

                conversation_content = "".join(conversation_content)

                if len(conversation_content) > 100:
                    final_thought_prompt = """
                    You are a final thought that validates if the agents have answered the user's question.
                    Your previous reasoning to the agents are as follow:
                    {your_questions}
                    Then, the Agents Responses: {answers}
                    User's original Question: {question}
                    Follow the instructions below to provide a final thought:
                    1. If the agents have completely answered the question:
                    - Then you should provide a summarize for the answers, but the summarize need to be less than 150 words!
                    - Be clear and concise in your response
                    2. If agents is NOT able to answer the question:
                    - Combine knowledge provided by the agent responses, you need to answer the question yourself!
                    - Pay careful attention to the user's question and the agent responses
                    - NO limits on the length of the response applied!
                    Your response:
                    """.format(question=question, answers=conversation_content, your_questions=accumulated_response)

                    await asyncio.sleep(2)
                    agent_names = ", ".join([agent_name for agent_name, _, _ in agent_questions])
                    yield json.dumps({"response": f"\n\n### 🤖 Thanks {agent_names}, lets recap on the answers ... \n\n"})
                    await asyncio.sleep(1)

                    async with httpx.AsyncClient() as client:
                        async with client.stream("POST", self.url, json={"model": self.model, "prompt": final_thought_prompt}) as response:
                            async for chunk in response.aiter_bytes():
                                yield chunk

