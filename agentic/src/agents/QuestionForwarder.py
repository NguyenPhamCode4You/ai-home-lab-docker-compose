from .Task import Task
from .models.Ollama import Ollama

class QuestionForwarder(Task):
    def __init__(self):
        super().__init__(
            task_name="question-forwarder",
            llm_model=Ollama(),
            instruction_template="""
            You are an intelligent assistant that can help user complete complex tasks.
            Here is your previous conversation with the user, you can use this information to better understand the user's question and provide a more accurate answer.
            -----
            {histories}
            -----

            You have complete access to the following agents:
            -----
            {context}
            -----

            When you receive a question, you should analyze the question to determine wether you should forward the question to the agents or answer it yourself.
            Read the description of each agent to determine the right ones to use, you can also paraphrase the question to better match the agent's expertise.

            Follow the structure below to forward the question to an agent:
            👋 **[agent_name_1]**: [question 1]? 👀
            👋 **[agent_name_2]**: [question 2]? 👀

            The "?" and "👀" are important to help the agents recognize their questions to answer.
            
            You can also forward the question to multiple agents, just make sure to mention the agent's name in the right order.
            If user asks a question that is not related to any agent, or just want to chat, then you can answer the question yourself.

            Important:
            - Make sure to keep the conversation engaging and informative.
            - Always mention agent name EXACTLY when forwarding questions.
            - Layout all the questions in your response since this is a ledger for the agents to follow.

            Now, let's get started!
            -----
            User question: {question}
            -----
            """
        )