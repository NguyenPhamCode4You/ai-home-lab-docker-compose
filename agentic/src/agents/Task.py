import datetime
import os
from typing import List
from .models.Ollama import Ollama

class Task:
    def __init__(self, instruction_template: str, task_name: str = None, llm_model = None, max_context_tokens: int = 5000, context_chunk_size: int = None, user_instruction: str = None):
        self.task_name = task_name or "GenericTask"
        self.llm_model = llm_model or Ollama()
        self.instruction_template = instruction_template
        self.context_chunk_size = context_chunk_size
        self.max_context_tokens = max_context_tokens
        self.user_instruction = user_instruction or None
        self.state = { "context": "", "question": "", "response": "" }

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        context = str(context)[:self.max_context_tokens] if context else None
        self.state["context"] = context
        self.state["question"] = question
        self.state["response"] = ""
        chunks = HardSplitContextChunks(context, self.context_chunk_size)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(os.getcwd(), "logs", self.task_name, date_str)
        os.makedirs(folder_path, exist_ok=True)
        time_str = datetime.datetime.now().strftime("%H-%M-%S-%f")[:-3]
        max_history_tokens = self.max_context_tokens - len(context or "")
        histories = get_chat_history_string(conversation_history, max_history_tokens)
        
        with open(os.path.join(folder_path, f"{time_str}.md"), "w", encoding="utf-8") as file:
            for index, chunk in enumerate(chunks):
                if len(chunks) > 1:
                    next_iteration_header = get_iteration_name(index)
                    yield next_iteration_header
                    self.state["response"] += next_iteration_header
                    file.write(next_iteration_header)
                    file.flush()
                instruction = self.instruction_template
                if self.user_instruction:
                    instruction += f"\n\n{self.user_instruction}"
                final_prompt = instruction.format(context=chunk, question=question, histories=histories)
                if len(chunks) > 1:
                    final_prompt += "\n\nBe direct with your answer!\n\n"
                async for response_chunk in self.llm_model.stream(final_prompt):
                    yield response_chunk
                    self.state["response"] += response_chunk
                    file.write(response_chunk)
                    file.flush()

    async def run(self, context: str = None, question: str = None, conversation_history: list = None):
        final_text = ""
        async for response_chunk in self.stream(context, question, conversation_history):
            print(response_chunk, end="", flush=True)
            final_text += response_chunk
        return final_text
    
def get_iteration_name(iteration_index: int = 0):
    count_strings = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]
    return f"\n\n #### 🧠 {count_strings[iteration_index]} recall from Memory to answer the question: \n\n"

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