import asyncio
from asyncio import subprocess
import datetime
import json
import os
import sys
import httpx
from typing import List

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class ChartVisualizer:
    def __init__(
        self,
        url: str = "http://localhost:11434",
        model: str = "gemma2:9b-instruct-q8_0",
        hosting_url: str = "http://localhost:11434",
        max_history_tokens_length: int = 10000,
        temp_file_path: str = "temp",
    ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.hosting_url = hosting_url
        self.max_history_tokens_length = max_history_tokens_length
        self.temp_file_path = temp_file_path

    async def stream(self, question: str, messages: List[Message] = None):
        history_string = self.get_chat_history_string(messages)
        full_conversation_context = f"Conversation history: {history_string}\n\n" if history_string else ""
        full_conversation_context += f"User question: {question}"
        # Format datetime as a string suitable for filenames
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        file_path = os.path.join(self.temp_file_path, f"{filename}.png")
        python_file_path = os.path.join(self.temp_file_path, f"{filename}.py")
        image_hosting_url = f"{self.hosting_url}/{filename}.png"

        prompt = """
        You are an intelligent matplotlib python assistant that can help user create simple charts basing on a given data.
        Full Conversation: {full_conversation_context}
        Save path: {file_path}
        Provide the code to create a chart that best answers the user question, in python using matplotlib.
        DO NOT include plt.show() in the code.
        TRY to be as simple in your code as possible.
        Return code wrapped in ```python ``` block, no explaination needed
        Your code:
        """.format(full_conversation_context=full_conversation_context, file_path=file_path)

        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            python_code = ""
            try:
                async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                    async for chunk_str in response.aiter_bytes():
                        if (len(chunk_str) > 1000):
                            continue
                        python_code += json.loads(chunk_str)["response"]
                        yield chunk_str
            except Exception as e:
                yield json.dumps({"response": f"\n\n❌ Error generating Python code: {e}\n\n"})
                return
            
            await asyncio.sleep(1) # Wait for the agents to respond completely
            python_code = python_code.strip().replace("```python", "").replace("```", "")
            yield json.dumps({"response": f"\n\n### 🤖 Generating charts ...\n\n"})
            
            try:
                os.makedirs(self.temp_file_path, exist_ok=True)  # Ensure directory exists
                with open(python_file_path, "w", encoding="utf-8") as python_file:
                    python_file.write(python_code)
            
            except Exception as e:
                yield json.dumps({"response": f"\n\n❌ Error saving Python code to file: {e}\n\n"})
                return
            
            await asyncio.sleep(1)  # Wait for the file to be saved
            # Step 3: Execute the Python file
            try:
                python_path = sys.executable
                process = await asyncio.create_subprocess_exec(
                    python_path, python_file_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                if stdout:
                    yield json.dumps({"response": f"\n\n✅ Execution Output: {stdout.decode()}"})
                if stderr:
                    yield json.dumps({"response": f"\n\n❌ Execution Error: {stderr.decode()}"})
            
            except subprocess.CalledProcessError as e:
                yield json.dumps({"response": f"\n\n❌ Execution failed: {e.stderr}\n\n"})

            except Exception as e:
                yield json.dumps({"response": f"\n\n❌ An unexpected error occurred during execution: {str(e)}\n\n"})
            
            yield json.dumps({"response": f"![Generated Chart]({image_hosting_url})"})

    def get_chat_history_string(self, histories: List[Message] = None) -> str:
        """
        Returns a string representation of the chat history, limited to the last N tokens.
        Each entry includes the role and the last 3000 tokens of content.
        """
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
                
        

