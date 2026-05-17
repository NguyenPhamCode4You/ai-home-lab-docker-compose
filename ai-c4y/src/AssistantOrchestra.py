import asyncio
import re
import json
from .agents.Task import Task
from .agents.QuestionForwarder import QuestionForwarder
from .agents.FinalThoughtSummarizer import FinalThoughtSummarizer
from .agents.AnswerEvaluator import AnswerEvaluator
from .agents.IterationSummarizer import IterationSummarizer


def _parse_agent_routing(routing_text: str, valid_agent_names: list) -> list:
    """Parse JSON routing block from LLM output. Returns list of (agent_name, question) tuples."""
    # Try ```json ... ``` block
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', routing_text)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            if isinstance(data, list):
                return [
                    (item["agent"], item["question"])
                    for item in data
                    if item.get("agent") in valid_agent_names and item.get("question")
                ]
        except (json.JSONDecodeError, KeyError):
            pass

    # Try bare JSON array anywhere in text
    try:
        start, end = routing_text.find('['), routing_text.rfind(']') + 1
        if start != -1 and end > start:
            data = json.loads(routing_text[start:end])
            if isinstance(data, list):
                result = [
                    (item["agent"], item["question"])
                    for item in data
                    if item.get("agent") in valid_agent_names and item.get("question")
                ]
                if result:
                    return result
    except (json.JSONDecodeError, KeyError, ValueError):
        pass

    # Fallback: legacy bold-name regex (backward compat)
    def strip_non_alpha(t):
        return re.sub(r"[^a-zA-Z]+", ' ', t)
    found = []
    for name in valid_agent_names:
        tag = f"**{strip_non_alpha(name)}**"
        for m in re.finditer(re.escape(tag), routing_text):
            after = routing_text[m.end():]
            q = after.split("👋")[0]
            if ":" in q and "?" in q:
                found.append((name, q.strip(), m.start()))
    found.sort(key=lambda x: x[2])
    return [(n, q) for n, q, _ in found]


def _parse_eval_result(text: str):
    """Returns (satisfied: bool, follow_up: str | None)."""
    try:
        start, end = text.find('{'), text.rfind('}') + 1
        if start != -1 and end > start:
            data = json.loads(text[start:end])
            return bool(data.get("satisfied", False)), data.get("follow_up")
    except (json.JSONDecodeError, ValueError):
        pass
    upper = text.upper()
    if "TRUE" in upper or '"SATISFIED": TRUE' in upper.replace(" ", ""):
        return True, None
    return False, None

class AssistantOrchestra:
    def __init__(
        self,
        llm_question_forwarder: Task = None,
        llm_final_thought_summarizer: Task = None,
        llm_answer_evaluator: Task = None,
        llm_iteration_summarizer: Task = None,
        agents: dict = None,
        max_iterations: int = 3,
        compact_threshold_tokens: int = 24000,
        also_include_original_question_from_user: bool = False,
    ):
        self.agents = agents or {}
        self.question_forwarder = llm_question_forwarder or QuestionForwarder()
        self.final_thought_summarizer = llm_final_thought_summarizer or FinalThoughtSummarizer()
        self.answer_evaluator = llm_answer_evaluator or AnswerEvaluator()
        self.iteration_summarizer = llm_iteration_summarizer or IterationSummarizer()
        self.max_iterations = max_iterations
        self.compact_threshold_tokens = compact_threshold_tokens
        self.also_include_original_question_from_user = also_include_original_question_from_user

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        is_silent = "--silent" in question
        valid_agent_names = list(self.agents.keys())
        all_agent_responses = ""
        current_question = question
        dispatched_agents = []

        for iteration in range(1, self.max_iterations + 1):

            # ---- Step 1: Route the question — stream reasoning live inside <think>, hide JSON block ----
            routing_context = self.get_agents_description()
            if iteration > 1 and all_agent_responses:
                routing_context += f"\n\nPrevious answers so far:\n{all_agent_responses}"

            routing_output = ""
            in_json_block = False  # suppress the ```json ... ``` routing block from display
            prev_safe_display = ""  # track what has already been yielded (after stripping model think)
            if not is_silent:
                if iteration > 1:
                    yield f"<think>\n🔄 **Iteration {iteration}** — refining the answer...\n"
                else:
                    yield "<think>\n"
            async for chunk in self.question_forwarder.stream(
                context=routing_context,
                question=current_question,
                conversation_history=conversation_history,
            ):
                routing_output += chunk
                if not is_silent and not in_json_block:
                    # Strip complete model <think>...</think> blocks, hold back incomplete ones
                    safe = re.sub(r'<think>[\s\S]*?</think>\s*', '', routing_output)
                    open_pos = safe.find('<think>')
                    if open_pos != -1:
                        safe = safe[:open_pos]  # suppress until think block closes

                    # Stop displaying at the json routing block (suppress at ``` to avoid
                    # yielding stray backticks before 'json' arrives in the next chunk)
                    json_pos = safe.find('```')
                    if json_pos != -1:
                        safe = safe[:json_pos]
                        in_json_block = True

                    # Yield only the new delta since last iteration
                    if safe.startswith(prev_safe_display):
                        new_part = safe[len(prev_safe_display):]
                        if new_part:
                            yield new_part
                    prev_safe_display = safe

            agent_questions = _parse_agent_routing(routing_output, valid_agent_names)

            # ---- Step 2: No agents → forwarder answered directly, close think and emit answer ----
            if not agent_questions:
                if not is_silent:
                    yield "\n</think>\n\n"
                break

            # ---- Agents found → close <think> block ----
            if not is_silent:
                yield "\n</think>\n\n"

            # ---- Step 3: Execute each agent ----
            dispatched_agents = [name for name, _ in agent_questions]
            total_agents = len(agent_questions)
            for agent_idx, (agent_name, agent_question) in enumerate(agent_questions, start=1):
                agent_details = self.agents.get(agent_name, {})
                agent = agent_details.get("agent")

                if not agent:
                    yield f"\n\n⚠️ Agent '{agent_name}' not found or unavailable.\n\n"
                    continue

                additional_context = ""
                if agent_details.get("context_awareness", True):
                    additional_context = all_agent_responses or routing_output

                if self.also_include_original_question_from_user:
                    agent_question += f"\n\n**Original user question:** {question}"

                if not is_silent:
                    yield f"\n\n### Hey 🤖 {agent_name} ({agent_idx}/{total_agents}), {agent_question.strip().rstrip('?')}?\n\n"
                else:
                    yield "\n\n"

                await asyncio.sleep(1)
                try:
                    async for chunk in agent.stream(
                        question=agent_question,
                        context=additional_context,
                        conversation_history=conversation_history,
                    ):
                        all_agent_responses += chunk
                        yield chunk
                except Exception as e:
                    yield f"\n\n⚠️ Agent '{agent_name}' error: {e}\n\n"

            # ---- Step 4: Evaluate — stop loop if satisfied or on last iteration ----
            if iteration >= self.max_iterations:
                break

            eval_result = await self.answer_evaluator.run(
                context=all_agent_responses,
                question=question,
            )
            satisfied, follow_up = _parse_eval_result(eval_result)
            if satisfied:
                break

            # Compact accumulated responses via summarization before next iteration
            # Only compact when context exceeds the threshold (approx 4 chars per token)
            context_too_long = len(all_agent_responses) > self.compact_threshold_tokens * 4
            if self.iteration_summarizer is not None and context_too_long:
                if not is_silent:
                    yield "<think>\n🗜️ Compacting previous answers...\n"
                compacted = ""
                async for chunk in self.iteration_summarizer.stream(
                    context=all_agent_responses,
                    question=question,
                ):
                    compacted += chunk
                    if not is_silent:
                        yield chunk
                if not is_silent:
                    yield "\n</think>\n\n"
                all_agent_responses = f"## Summary of previous iterations:\n{compacted}"
            # else: keep all_agent_responses as-is for the next iteration

            current_question = follow_up or question

        # ---- Step 5: Final summarizer if multiple agents responded ----
        if all_agent_responses and len(dispatched_agents) > 1:
            await asyncio.sleep(1)
            agent_names_string = ", ".join(dispatched_agents)
            yield f"\n\n### 🤖 Thanks {agent_names_string}, lets recap on the answers...\n\n"
            await asyncio.sleep(1)
            async for chunk in self.final_thought_summarizer.stream(
                context=all_agent_responses, question=question
            ):
                yield chunk

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