import datetime
import os
from .agents.MathplotCodeWriter import MathplotCodeWriter
from .agents.tools.PythonCodeExecute import PythonCodeExecute

class ChartVisualizerAssistant():
    def __init__(self,
            llm_mathplot_code_writer: MathplotCodeWriter = None,
            python_code_executor: PythonCodeExecute = None,
            max_history_tokens_length: int = 8000,
            public_hosting_url: str = None):
        
        self.mathplot_code_writer = llm_mathplot_code_writer or MathplotCodeWriter()
        self.python_code_executor = python_code_executor or PythonCodeExecute()
        self.max_history_tokens_length = max_history_tokens_length
        self.public_hosting_url = public_hosting_url or os.getenv("PUBLIC_HOSTING_URL")

    async def stream(self, question: str = None, conversation_history: list = None):
        base_file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        python_file_name = f"{base_file_name}.py"
        image_file_name = f"{base_file_name}.png"
        image_file_path = os.path.join(self.python_code_executor.temp_file_path, image_file_name)
        
        code_context = self.get_chat_history_string(conversation_history)
        code_string = ""
        async for code_chunk in self.mathplot_code_writer.stream(question=question, context=code_context):
            code_string += code_chunk
            yield code_chunk

        code_string += f"\n\nplt.savefig(r'{image_file_path}')\n\n"
        await self.python_code_executor.run(python_code=code_string, save_file_name=python_file_name)
        yield f"\n\n🔗 **Chart Generated:** ![Generated Chart]({self.public_hosting_url}/{image_file_name})\n\n"

    def get_chat_history_string(self, histories = None) -> str:
        if histories is None:
            histories = []  # Default to an empty list if no histories are provided

        accumulated_tokens = 0
        max_length = self.max_history_tokens_length
        selected_messages = []

        # Traverse the history in reverse to start from the latest messages
        for message in reversed(histories):
            # Get the last 3000 tokens of the message content
            truncated_content = message.content[-3000:]
            content_length = len(truncated_content)

            # Stop adding messages if the token limit would be exceeded
            if accumulated_tokens + content_length > max_length:
                break

            # Append the formatted message
            selected_messages.append(f"\n >> {message.role}: {truncated_content}\n\n")
            accumulated_tokens += content_length

        # Return the messages in chronological order
        return "".join(reversed(selected_messages))
        