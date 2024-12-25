import asyncio
from asyncio import subprocess
import datetime
import os
import sys

class PythonCodeExecute:
    def __init__(self, temp_file_path: str = None):
        self.temp_file_path = temp_file_path or "temp"
        os.makedirs(self.temp_file_path, exist_ok=True)

    async def run(self, python_code: str, save_file_name: str = None):
        filename = save_file_name or f"{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.py"
        python_file_path = os.path.join(self.temp_file_path, filename)
        try:
            python_code = python_code.strip().replace("```python", "").replace("```", "")
            with open(python_file_path, "w", encoding="utf-8") as python_file:
                python_file.write(python_code)

        except Exception as e:
            return f"\n\n❌ Error saving Python code to file: {e}\n\n"

        try:
            python_path = sys.executable
            process = await asyncio.create_subprocess_exec(
                python_path, python_file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if stdout:
                return f"\n\n✅ Code Execution Output: {stdout.decode()}"
            if stderr:
                return f"\n\n❌ Code Execution Error: {stderr.decode()}"
            
        except Exception as e:
            return f"\n\n❌ Code Execution failed: {e}\n\n"
        
        

