"""ProgressiveAgentSLM — core hybrid orchestration loop.

Execution flow (modeled on AssistantOrchestra.stream, extended with
worklog + reflection):

  1. Forwarder routes the question to delegates (agents / tools).
  2. Execute each delegate sequentially, streaming chunks live.
  3. Append each delegate's compact output to the shared worklog.
  4. Reflector revises the worklog (compact + non-redundant).
  5. AnswerEvaluator decides if the goal is satisfied.
  6. If not satisfied (and iterations remain): re-route with follow-up.
  7. FinalThoughtSummarizer recaps when multiple delegates contributed.

All events are logged via RunLogger (events.jsonl + transcript.md).
The stream yields str chunks compatible with create_chat_backend.
"""
from __future__ import annotations

import asyncio
import re
from typing import Any, Dict

from .AgentConfig import AgentConfig
from .ModelRegistry import ModelRegistry
from .ToolRegistry import Tool, ToolRegistry
from .Worklog import Worklog
from .agents.Forwarder import Forwarder
from .agents.Reflector import Reflector
from .logging.RunLogger import RunLogger
from ..AssistantOrchestra import _parse_agent_routing, _parse_eval_result
from ..agents.AnswerEvaluator import AnswerEvaluator
from ..agents.FinalThoughtSummarizer import FinalThoughtSummarizer
from ..agents.IterationSummarizer import IterationSummarizer

# Characters per token approximation (matches Task defaults)
_CHARS_PER_TOKEN = 3


class ProgressiveAgentSLM:
    """
    Fully configurable agentic orchestrator optimised for local/SLM.

    Drop-in replacement for AssistantOrchestra — compatible with
    ``create_chat_backend`` (yields str chunks from ``stream()``).

    Quick start::

        agent = ProgressiveAgentSLM()
        agent.add_agent("BVMS", "Domain expert.", bvms_assistant, context_awareness=True)
        agent.add_tool(ReadFileTool())
        # uvicorn.run(create_chat_backend(agent), ...)
    """

    def __init__(
        self,
        config: AgentConfig = None,
        model_registry: ModelRegistry = None,
        tool_registry: ToolRegistry = None,
        forwarder: Forwarder = None,
        reflector: Reflector = None,
        answer_evaluator: AnswerEvaluator = None,
        final_summarizer: FinalThoughtSummarizer = None,
        iteration_summarizer: IterationSummarizer = None,
        runs_dir: str = "runs",
    ) -> None:
        self.config = config or AgentConfig()
        self._model_registry = model_registry or self.config.model_registry or ModelRegistry()
        self._tool_registry = tool_registry or ToolRegistry()

        # Unified delegate registry: name → {kind, agent, description, context_awareness}
        self._delegates: Dict[str, Dict[str, Any]] = {}

        # Internal agents wired to specific model roles
        reflection_model = self._model_registry.get("reflection")
        chat_model = self._model_registry.get("chat")

        self._forwarder = forwarder or Forwarder(llm_model=chat_model)
        self._reflector = reflector or Reflector(llm_model=reflection_model)
        self._answer_evaluator = answer_evaluator or AnswerEvaluator(llm_model=reflection_model)
        self._final_summarizer = final_summarizer or FinalThoughtSummarizer(llm_model=chat_model)
        self._iteration_summarizer = iteration_summarizer or IterationSummarizer(llm_model=reflection_model)

        self._runs_dir = runs_dir

        # Seed from AgentConfig
        for name, info in self.config.sub_agents.items():
            self._delegates[name] = {"kind": "agent", **info}
        for tool in self.config.tools:
            self._register_tool_delegate(tool)

    # ── Public registration API (mirrors AssistantOrchestra) ───────────────

    def add_agent(
        self,
        name: str,
        description: str,
        agent: Any,
        context_awareness: bool = False,
    ) -> "ProgressiveAgentSLM":
        """Register a sub-agent delegate. Returns self for chaining."""
        self._delegates[name] = {
            "kind": "agent",
            "agent": agent,
            "description": description,
            "context_awareness": context_awareness,
        }
        return self

    def add_tool(self, tool: Tool) -> "ProgressiveAgentSLM":
        """Register a tool delegate. Returns self for chaining."""
        self._tool_registry.register(tool)
        self._register_tool_delegate(tool)
        return self

    def _register_tool_delegate(self, tool: Tool) -> None:
        self._delegates[tool.name] = {
            "kind": "tool",
            "agent": tool,
            "description": tool.description,
            "context_awareness": False,
        }

    # ── Delegate descriptions for routing prompt ────────────────────────────

    def _get_delegate_descriptions(self) -> str:
        if not self._delegates:
            return "(no delegates registered — answer directly)"
        return "\n".join(
            f"**{name}** [{info.get('kind', 'agent')}]: {info.get('description', '')}"
            for name, info in self._delegates.items()
        )

    # ── Main streaming loop ─────────────────────────────────────────────────

    async def stream(
        self,
        context: str = None,
        question: str = None,
        conversation_history: list = None,
    ):
        """
        Stream a full agentic response for *question*.

        Yields str chunks compatible with FastAPI StreamingResponse /
        create_chat_backend.
        """
        is_silent = bool(question and "--silent" in question)
        logger = RunLogger(self._runs_dir)

        valid_names = list(self._delegates.keys())
        all_responses: str = ""
        current_question: str = question or ""
        had_delegates: bool = False
        delegate_calls: list = []

        logger.log_event(
            "root", "plan", "progressive-agent-slm",
            input_text=current_question, output_text="",
        )

        for iteration in range(1, self.config.max_steps + 1):

            # ── 1. Route via Forwarder ──────────────────────────────────────
            routing_ctx = self._get_delegate_descriptions()
            if iteration > 1 and all_responses:
                routing_ctx += f"\n\nWorklog so far:\n{logger.worklog.read()}"

            routing_output: str = ""
            in_json_block: bool = False
            prev_safe: str = ""

            if not is_silent:
                if iteration > 1:
                    header = f"<think>\n🔄 **Iteration {iteration}** — refining...\n"
                else:
                    header = "<think>\n"
                yield header
                logger.append_transcript(header)

            async for chunk in self._forwarder.stream(
                context=routing_ctx,
                question=current_question,
                conversation_history=conversation_history,
            ):
                routing_output += chunk
                if not is_silent and not in_json_block:
                    # Strip complete <think>...</think> blocks, hold incomplete ones
                    safe = re.sub(r"<think>[\s\S]*?</think>\s*", "", routing_output)
                    open_pos = safe.find("<think>")
                    if open_pos != -1:
                        safe = safe[:open_pos]

                    # Stop display at the JSON routing block (suppress at ```)
                    json_pos = safe.find("```")
                    if json_pos != -1:
                        safe = safe[:json_pos]
                        in_json_block = True

                    if safe.startswith(prev_safe):
                        new_part = safe[len(prev_safe):]
                        if new_part:
                            yield new_part
                            logger.append_transcript(new_part)
                    prev_safe = safe

            delegate_calls = _parse_agent_routing(routing_output, valid_names)
            logger.log_event(
                f"iter-{iteration}", "plan", "forwarder",
                input_text=current_question, output_text=routing_output[:400],
            )

            # ── 2. No delegates → forwarder answered directly ───────────────
            if not delegate_calls:
                close = "\n</think>\n\n" if not is_silent else ""
                if close:
                    yield close
                    logger.append_transcript(close)
                break

            if not is_silent:
                close = "\n</think>\n\n"
                yield close
                logger.append_transcript(close)

            # ── 3. Execute each delegate ────────────────────────────────────
            had_delegates = True
            total = len(delegate_calls)

            for idx, (dname, dquestion) in enumerate(delegate_calls, 1):
                info = self._delegates.get(dname)
                if not info:
                    warn = f"\n\n⚠️ Delegate '{dname}' not found.\n\n"
                    yield warn
                    logger.append_transcript(warn)
                    continue

                agent = info["agent"]
                ctx_aware: bool = info.get("context_awareness", False)
                additional_ctx = logger.worklog.read() if ctx_aware else (context or "")

                if self.config.goal:
                    dquestion = dquestion + f"\n\n**Overall goal:** {self.config.goal}"

                if not is_silent:
                    label = info.get("kind", "agent").upper()
                    header = f"\n\n### 🤖 [{label}] {dname} ({idx}/{total})\n> {dquestion.strip()}\n\n"
                    yield header
                    logger.append_transcript(header)
                else:
                    yield "\n\n"

                await asyncio.sleep(0)  # yield control to event loop

                response: str = ""
                status: str = "ok"
                try:
                    async for chunk in agent.stream(
                        question=dquestion,
                        context=additional_ctx,
                        conversation_history=conversation_history,
                    ):
                        all_responses += chunk
                        response += chunk
                        yield chunk
                        logger.append_transcript(chunk)
                except Exception as exc:
                    status = "error"
                    err_msg = f"\n\n⚠️ {dname} error: {exc}\n\n"
                    yield err_msg
                    logger.append_transcript(err_msg)
                    response = err_msg

                # Append compact worklog entry (first 800 chars as proxy)
                compact = response[:800].strip()
                logger.worklog.append(dname, compact)
                logger.log_event(
                    f"iter-{iteration}", "delegate",
                    f"{info['kind']}:{dname}",
                    input_text=dquestion[:300],
                    output_text=response[:300],
                    status=status,
                )

            # ── 4. Reflect: compact worklog ────────────────────────────────
            if self.config.reflection.enabled:
                if not is_silent:
                    think_open = "\n\n<think>\n✨ Reflecting on worklog...\n"
                    yield think_open
                    logger.append_transcript(think_open)
                try:
                    revised = await self._reflector.run(
                        context=logger.worklog.read(),
                        question=question,
                    )
                    if revised and revised.strip():
                        logger.worklog.revise(revised)
                    logger.log_event(
                        f"iter-{iteration}", "reflect", "reflector",
                        output_text=revised[:300] if revised else "",
                    )
                except Exception as exc:
                    print(f"[ProgressiveAgentSLM] reflector error: {exc}", flush=True)

                if not is_silent:
                    think_close = "\n</think>\n\n"
                    yield think_close
                    logger.append_transcript(think_close)

                # Compact in-memory accumulator if over token threshold
                approx_tokens = len(all_responses) // _CHARS_PER_TOKEN
                if approx_tokens > self.config.compact_threshold_tokens:
                    try:
                        compacted = await self._iteration_summarizer.run(
                            context=all_responses,
                            question=question,
                        )
                        all_responses = compacted
                        logger.log_event(
                            f"iter-{iteration}", "reflect", "iteration-summarizer",
                            output_text=compacted[:300],
                        )
                    except Exception as exc:
                        print(f"[ProgressiveAgentSLM] summarizer error: {exc}", flush=True)

            # ── 5. Evaluate ────────────────────────────────────────────────
            if iteration >= self.config.max_steps:
                break

            try:
                eval_result = await self._answer_evaluator.run(
                    context=all_responses,
                    question=question,
                )
                satisfied, follow_up = _parse_eval_result(eval_result)
                logger.log_event(
                    f"iter-{iteration}", "evaluate", "answer-evaluator",
                    input_text=question or "",
                    output_text=eval_result[:200],
                )
                if satisfied:
                    break
                if follow_up:
                    current_question = follow_up
            except Exception as exc:
                print(f"[ProgressiveAgentSLM] evaluator error: {exc}", flush=True)
                break

        # ── 6. Final recap ──────────────────────────────────────────────────
        if had_delegates and all_responses:
            sep = "\n\n---\n\n"
            yield sep
            logger.append_transcript(sep)
            async for chunk in self._final_summarizer.stream(
                context=all_responses,
                question=question,
            ):
                yield chunk
                logger.append_transcript(chunk)
            logger.log_event("final", "final", "final-summarizer", input_text=question or "")

        logger.log_event("root", "final", "progressive-agent-slm", status="ok")
