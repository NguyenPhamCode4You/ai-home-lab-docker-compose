import asyncio
import re
from .agents.Task import Task
from .agents.QuestionForwarder import QuestionForwarder
from .agents.FinalThoughtSummarizer import FinalThoughtSummarizer

def remove_special_chars(text):
    return re.sub(r"[^a-zA-Z]+", ' ', text)

class AssistantOrchestra:
    def __init__(
        self,
        llm_question_forwarder: Task = None,
        llm_final_thought_summarizer: Task = None,
        agents: dict = None,
    ):
        self.agents = agents or {}
        self.question_forwarder = llm_question_forwarder or QuestionForwarder()
        self.final_thought_summarizer = llm_final_thought_summarizer or FinalThoughtSummarizer()
    
    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        is_verbose = "--verbose" in question
        agent_self_questions  = ""
        async for question_chunk in self.question_forwarder.stream(context=self.get_agents_description(), question=question, conversation_history=conversation_history):
            agent_self_questions += question_chunk
            if is_verbose:
                yield question_chunk
        
        agent_questions = []
        # ---------------------------------------
        # 1. Find all agents mentioned and their questions
        # ----------------------------------------
        for agent_name, agent_details in self.agents.items():
            agent_name_formated = f"**{remove_special_chars(agent_name)}**"
            for match in re.finditer(re.escape(agent_name_formated), agent_self_questions):
                agent_mention_index = match.start()
                agent_question = agent_self_questions[agent_mention_index + len(agent_name_formated):].split("👋")[0]
                if ":" in agent_question and "?" in agent_question:
                    agent_questions.append((agent_name, agent_question.strip(), agent_mention_index))
        # ---------------------------------------
        # 2. Order the agents based on their mention index
        # ----------------------------------------
        agent_questions = sorted(agent_questions, key=lambda x: x[2])
        conversation_context = ""
        # ---------------------------------------
        # 3. Execute the agents in the order of their mention
        # ----------------------------------------
        for agent_name, agent_question, agent_mention_index in agent_questions:
            await asyncio.sleep(2)
            agent_details = self.agents.get(agent_name, {})
            agent = agent_details.get("agent")
            
            if not agent:
                yield f"\n\n⚠️ Agent '{agent_name}' not found or unavailable.\n\n"
                continue
            
            if (len(conversation_context) > 0):
                additional_context = conversation_context
            else:
                additional_context = agent_self_questions
            if agent_details.get("context_awareness") == False:
                additional_context = ""
                
            if is_verbose:
                yield f"\n\n### 🤖 {agent_name} {agent_question} ...\n\n"
            
            await asyncio.sleep(2)
            # ---------------------------------------
            # 4. Execute the agent and stream the response
            # ----------------------------------------
            try:
                async for agent_chunk in agent.stream(question=agent_question, context=additional_context, conversation_history=conversation_history):
                    conversation_context += agent_chunk
                    yield agent_chunk
            
            except Exception as e:
                yield f"\n\n⚠️ Agent '{agent_name}' error {e}\n\n"

        if len(agent_questions) > 1:
            await asyncio.sleep(2)
            agent_names_string = ", ".join([agent_name for agent_name, _, _ in agent_questions])
            yield f"\n\n### 🤖 Thanks {agent_names_string}, lets recap on the answers ... \n\n"
            await asyncio.sleep(1)

            async for final_thought_chunk in self.final_thought_summarizer.stream(context=conversation_context, question=question):
                yield final_thought_chunk

    async def write_analysis(self, question: str, log_file_path: str) -> None:
        if not log_file_path:
            return print("No log file specified. Please set a log file using the 'set_log_file' method.")
        try:
            with open(log_file_path, "w", encoding="utf-8") as file:
                file.write(f"\n\n## User question: {question}\n\n\n")
                async for agent_chunk in self.stream(question, []):
                    file.write(agent_chunk)
                    file.flush()
                    print(agent_chunk, end="", flush=True)
        except Exception as e:
            print(f"Error logging task: {e}")

    def add_agent(self, name: str, description: str, agent, context_awareness: bool = False):
        self.agents[name] = {"description": description, "agent": agent, "context_awareness": context_awareness}
        return self

    def get_agents_description(self):
        return "\n".join(
            [f"\n{agent_name}: {details['description']}\n" for agent_name, details in self.agents.items()]
        )