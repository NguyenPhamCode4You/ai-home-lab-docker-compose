import asyncio
from asyncio import subprocess
from datetime import datetime
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
        Return code wrapped in ```python ``` block, no explaination needed
        Your code:
        """.format(question=question, file_path=file_path)

        async with httpx.AsyncClient() as client:
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
                with open(python_file_path, "w") as python_file:
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
            
            yield json.dumps({"response": f"![Generated Chart]({image_host_url})"})
                
        

