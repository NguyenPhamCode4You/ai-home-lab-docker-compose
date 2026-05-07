from .Task import Task
from .models.Ollama import Ollama

class QuestionForwarder(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "question-forwarder")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            You are an intelligent orchestrator that routes user questions to the right specialist agents.

            Previous conversation:
            -----
            {histories}
            -----

            Available agents:
            -----
            {context}
            -----

            Your job:
            1. Read the user question carefully.
            2. Decide which agent(s) are best suited to answer it based on their descriptions.
            3. You may rephrase the question to better match each agent's expertise.
            4. You can forward the question to multiple agents if the question spans multiple topics.
            5. If the question is simple chit-chat or unrelated to any agent, answer it yourself.

            After your brief reasoning, output a JSON routing block at the very end of your response:

            For one or more agents:
            ```json
            [
              {{"agent": "Exact Agent Name", "question": "specific question tailored for this agent?"}},
              {{"agent": "Another Agent Name", "question": "specific question tailored for this agent?"}}
            ]
            ```

            If no agent is needed (answer yourself):
            ```json
            []
            ```

            Rules:
            - Agent names in the JSON MUST match exactly the names listed above.
            - Always end your response with the ```json block.
            - The JSON must be valid.

            User question: {question}
        """)
        super().__init__(**kwargs)