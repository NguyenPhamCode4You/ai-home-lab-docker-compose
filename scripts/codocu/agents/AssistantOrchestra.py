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

def remove_special_chars(text):
    return re.sub(r"[^a-zA-Z]+", ' ', text)

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
        Here is your previous conversation with the user, you can use this information to better understand the user's question and provide a more accurate answer.
        -----
        {histories}
        -----

        You have complete access to the following agents:
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
    
    async def stream(self, question: str, messages: List[Message] = None):
        histories = self.get_chat_history_string(messages)
        prompt = self.base_prompt.format(agents=self.get_agents_description(), question=question, histories=histories)
        
        agent_self_questions  = ""
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk_str in response.aiter_bytes():
                    if (len(chunk_str) > 1000):
                        continue
                    agent_self_questions += json.loads(chunk_str)["response"]
                    yield chunk_str

                agent_questions = []
                # ---------------------------------------
                # 1. Find all agents mentioned and their questions
                # ----------------------------------------
                for agent_name, agent_details in self.agents.items():
                    agent_name_formated = f"**{remove_special_chars(agent_name)}**"
                    
                    for match in re.finditer(re.escape(agent_name_formated), agent_self_questions):
                        agent_mention_index = match.start()
                        
                        # Extract the part of the text after the agent's mention
                        agent_question_part = agent_self_questions[agent_mention_index + len(agent_name_formated):]
                        
                        # Extract the question until the first occurrence of "👀" or end of string
                        agent_question = agent_question_part.split("👀")[0]
                        
                        # Check if the extracted text qualifies as a valid question
                        if ":" in agent_question and "?" in agent_question:
                            agent_questions.append((agent_name, agent_question.strip(), agent_mention_index))
                # ---------------------------------------
                # 2. Order the agents based on their mention index
                # ----------------------------------------
                agent_questions = sorted(agent_questions, key=lambda x: x[2])
                conversation_content = []
                # ---------------------------------------
                # 3. Execute the agents in the order of their mention
                # ----------------------------------------
                for agent_name, agent_question, agent_mention_index in agent_questions:
                    await asyncio.sleep(2)
                    agent_details = self.agents.get(agent_name, {})
                    agent = agent_details.get("agent")
                    
                    if not agent:
                        yield f"\n\n### ⚠️ Agent '{agent_name}' not found or unavailable.\n\n"
                        continue
                    
                    if (len(conversation_content) > 0):
                        additional_context = "".join(conversation_content)
                    else:
                        additional_context = "".join(agent_self_questions)

                    real_agent_question = f"**Addtional context that might be useful:**\n{additional_context}\n**Finally, here is your question:** {agent_question}"
                    
                    yield json.dumps({"response": f"\n\n### 🤖 {agent_name} {agent_question} ...\n\n"})
                    conversation_content.append(f"\n### 🤖 {agent_name} ")
                    await asyncio.sleep(2)
                    # ---------------------------------------
                    # 4. Excetute the agent and stream the response
                    # ----------------------------------------
                    try:
                        async for agent_chunk in agent.stream(real_agent_question, messages):
                            if (len(agent_chunk) > 1000):
                                continue
                            agent_response = json.loads(agent_chunk)["response"]
                            conversation_content.append(agent_response)
                            yield agent_chunk
                    
                    except Exception as e:
                        yield ""

                await asyncio.sleep(3) # Wait for the agents to respond completely

                conversation_content = "".join(conversation_content)
                # ---------------------------------------
                # 5. Final thought prompt to wrap up the conversation
                # ----------------------------------------
                final_thought_prompt = """
                You are a final reflection that validates if the user's question have been answered correctly or not.
                Here are your previous conversations with user:
                -------------------------
                {histories}
                -------------------------


                Here are your questions to the agents:
                -------------------------
                {agent_self_questions}
                -------------------------


                Here are the knowledge the agents provided: 
                -------------------------
                {agents_answers}
                -------------------------


                User's original Question: 
                -------------------------
                {user_question}
                -------------------------

                - Combine knowledge provided by the agent responses, you need to provide a final answer the user's question.
                - Pay careful attention to the user's question and the agent responses, and provide a complete and accurate answer to the user's question.
                """.format(user_question=question, agents_answers=conversation_content, agent_self_questions=agent_self_questions, histories=histories)

                await asyncio.sleep(2)
                agent_names = ", ".join([agent_name for agent_name, _, _ in agent_questions])
                yield json.dumps({"response": f"\n\n### 🤖 Thanks {agent_names}, lets recap on the answers ... \n\n"})
                await asyncio.sleep(1)

                async with httpx.AsyncClient() as client:
                    async with client.stream("POST", self.url, json={"model": self.model, "prompt": final_thought_prompt}) as response:
                        async for final_thought_chunk in response.aiter_bytes():
                            yield final_thought_chunk

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
            content_length = len(message.content[:6000])  # Restrict each message to 1800 characters
            if accumulated_tokens + content_length > self.max_history_tokens_length:
                break  # Stop adding messages when the limit is reached

            selected_messages.append(f"\n >> {message.role}: {message.content[:1800]}\n\n")
            accumulated_tokens += content_length

        # Reverse again to preserve the original chronological order
        return "".join(reversed(selected_messages))
