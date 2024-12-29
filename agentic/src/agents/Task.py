import asyncio
import datetime
import os
from typing import List
from .models.Ollama import Ollama

final_thought_prompt_template = """
You are the final thought that reflect your previous answers to the user questions.
Here is the user question: {question}
Your previous answers to the user questions:
{context}
Generate one final answer that combines all the previous answers to the user questions as your best answer to the user question.
"""

class Task:
    def __init__(self, task_name: str, instruction_template: str, llm_model = None, max_context_tokens: int = 5000, context_chunk_size: int = None, allow_reflection: bool = False):
        self.task_name = task_name or "GenericTask"
        self.llm_model = llm_model or Ollama()
        self.instruction_template = instruction_template
        self.context_chunk_size = context_chunk_size
        self.allow_reflection = allow_reflection
        self.max_context_tokens = max_context_tokens

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        chunks = HardSplitContextChunks(context, self.context_chunk_size)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(os.getcwd(), "logs", self.task_name, date_str)
        os.makedirs(folder_path, exist_ok=True)
        time_str = datetime.datetime.now().strftime("%H-%M-%S")
        max_history_tokens = self.max_context_tokens - len(context or "")
        histories = get_chat_history_string(conversation_history, max_history_tokens)
        
        with open(os.path.join(folder_path, f"{time_str}.md"), "w", encoding="utf-8") as file:
            response_iterations = ""
            for index, chunk in enumerate(chunks):
                if len(chunks) > 1:
                    next_iteration_header = get_iternation_name(index)
                    yield next_iteration_header
                    file.write(next_iteration_header)
                    file.flush()
                final_prompt = self.instruction_template.format(context=chunk, question=question, histories=histories)
                if len(chunks) > 1:
                    final_prompt += "\n\nBe direct with your answer!\n\n"
                async for response_chunk in self.llm_model.stream(final_prompt):
                    yield response_chunk
                    response_iterations += response_chunk
                    file.write(response_chunk)
                    file.flush()

            if len(chunks) > 1 and self.allow_reflection:
                final_thought_header = f"\n\n ### 🎯 Lets have one final revise on the question ...\n\n"
                await asyncio.sleep(1)
                yield final_thought_header
                file.write(final_thought_header)
                file.flush()
                final_thought_prompt = final_thought_prompt_template.format(context=response_iterations, question=question)
                async for response_chunk in self.llm_model.stream(final_thought_prompt):
                    yield response_chunk
                    file.write(response_chunk)
                    file.flush()

    async def run(self, context: str = None, question: str = None, conversation_history: list = None):
        final_text = ""
        async for response_chunk in self.stream(context, question, conversation_history):
            print(response_chunk, end="", flush=True)
            final_text += response_chunk
        return final_text
    
def get_iternation_name(iteration_index: int = 0):
    recal_name = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]
    return f"\n\n #### 🧠 {recal_name[iteration_index]} Recall from Memory ... \n\n"

def HardSplitContextChunks(text: str, max_length: int = None):
    if text is None:
        return ["No context provided."]
    if max_length is None:
        return [text]
    chunks = []
    while len(text) > max_length:
        chunks.append(text[:max_length])
        text = text[max_length:]
    chunks.append(text)
    return chunks

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

def get_chat_history_string(histories: List[Message] = None, max_histories_token: int = 1000) -> str:
        if histories is None or len(histories) == 0 or max_histories_token is None or max_histories_token <= 0:
            return ""
        accumulated_tokens = 0
        selected_messages = []
        for message in reversed(histories):
            # Get the last 3000 tokens of the message content
            truncated_content = message.content[-2500:]
            content_length = len(truncated_content)
            # Stop adding messages if the token limit would be exceeded
            if accumulated_tokens + content_length > max_histories_token:
                break
            # Append the formatted message
            selected_messages.append(f"\n >> {message.role}: {truncated_content}\n\n")
            accumulated_tokens += content_length
        # Return the messages in chronological order
        return "".join(reversed(selected_messages))