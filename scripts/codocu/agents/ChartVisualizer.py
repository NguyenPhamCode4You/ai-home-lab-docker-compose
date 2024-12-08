import asyncio
from asyncio import subprocess
import contextlib
from datetime import datetime
import io
import json
import os
import re
import sys
from fastapi import Request
import httpx
import requests
from typing import List, Optional

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class ChartVisualizer:
    def __init__(
        self,
        url: str = "http://localhost:11434/api/generate",
        model: str = "gemma2:9b-instruct-q8_0"
    ):
        self.url = url
        self.model = model
        self.temp_file_path = None
        self.host_url = None

    def set_host_url(self, host_url: str):
        self.host_url = host_url
        return self

    def set_temp_file_path(self, file_path: str):
        self.temp_file_path = file_path
        return self

    async def stream(self, question: str, messages: List[Message] = None):
        # Format datetime as a string suitable for filenames
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        file_path = os.path.join(self.temp_file_path, f"{filename}.png")
        python_file_path = os.path.join(self.temp_file_path, f"{filename}.py")
        image_host_url = f"{self.host_url}/{filename}.png"

        prompt = """
        You are an intelligent matplotlib python assistant that can help user create simple charts basing on a given data.
        Context: {question}
        Save path: {file_path}
        Provide the code to create a chart that best answers the user question, in python using matplotlib.
        DO NOT include plt.show() in the code.
        Return code as plain text, DO NOT wrapping in code blocks, no explaination.
        Your code:
        """.format(question=question, file_path=file_path)
        async with httpx.AsyncClient() as client:
            python_code = ""
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    try:
                        chunk_str = chunk.decode("utf-8")
                        python_code += json.loads(chunk_str)["response"]
                        yield chunk
                    except Exception as e:
                        yield ""
                        continue
            
            await asyncio.sleep(1) # Wait for the agents to respond completely
            python_code = python_code.strip().replace("```python", "").replace("```", "")
            yield json.dumps({"response": f"\n\n### 🤖 Generating charts ...\n\n"})
            
            try:
                os.makedirs(self.temp_file_path, exist_ok=True)  # Ensure directory exists
                with open(python_file_path, "w") as python_file:
                    python_file.write(python_code)
            
            except Exception as e:
                yield json.dumps({"response": f"❌ Error saving Python code to file: {e}\n\n"})
                return
            
            await asyncio.sleep(1)  # Wait for the file to be saved
            print(f"Python code saved to: {python_file_path}")
            
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
                    yield json.dumps({"response": f"✅ Execution Output: {stdout.decode()}"})
                if stderr:
                    yield json.dumps({"response": f"❌ Execution Error: {stderr.decode()}"})
            
            except subprocess.CalledProcessError as e:
                yield json.dumps({"response": f"❌ Execution failed: {e.stderr}\n\n"})
            except Exception as e:
                yield json.dumps({"response": f"❌ An unexpected error occurred during execution: {str(e)}\n\n"})
            
            yield json.dumps({"response": f"![Generated Chart]({image_host_url})"})
                
        

