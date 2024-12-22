import datetime
import os
from typing import List

class Task:
    def __init__(self, task_name: str, instruction_template: str, llm_model, context_chunk_size: int = 8000, max_histories_tokens: int = 1000):
        self.task_name = task_name or "GenericTask"
        self.llm_model = llm_model
        self.instruction_template = instruction_template
        self.context_chunk_size = context_chunk_size
        self.max_histories_tokens = max_histories_tokens

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        chunks = HardSplitChar(context, self.context_chunk_size)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(os.getcwd(), "logs", self.task_name, date_str)
        os.makedirs(folder_path, exist_ok=True)
        time_str = datetime.datetime.now().strftime("%H-%M-%S")
        histories = get_chat_history_string(conversation_history, self.max_histories_tokens)
        
        with open(os.path.join(folder_path, f"{time_str}.md"), "w", encoding="utf-8") as file:
            for index, chunk in enumerate(chunks):
                final_prompt = self.instruction_template.format(context=chunk, question=question, histories=histories)
                if len(chunks) > 1:
                    final_prompt += f"\nThis is a continuation answers number: {index + 1}/{len(chunks)}, so be direct with your answer."
                if index > 0:
                    yield "\n**Continues...**\n"
                    file.write("\n")
                async for response_chunk in self.llm_model.stream(final_prompt):
                    yield response_chunk
                    file.write(response_chunk)
                    file.flush()

    async def run(self, context: str = None, question: str = None, conversation_history: list = None):
        final_text = ""
        async for response_chunk in self.stream(context, question, conversation_history):
            print(response_chunk, end="", flush=True)
            final_text += response_chunk
        return final_text

def HardSplitChar(text: str, max_length: int = 8000):
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
        if histories is None:
            histories = []
        accumulated_tokens = 0
        selected_messages = []
        for message in reversed(histories):
            # Get the last 3000 tokens of the message content
            truncated_content = message.content[-3000:]
            content_length = len(truncated_content)
            # Stop adding messages if the token limit would be exceeded
            if accumulated_tokens + content_length > max_histories_token:
                break
            # Append the formatted message
            selected_messages.append(f"\n >> {message.role}: {truncated_content}\n\n")
            accumulated_tokens += content_length
        # Return the messages in chronological order
        return "".join(reversed(selected_messages))