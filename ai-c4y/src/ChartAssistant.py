import datetime
import os
from .agents.MathplotCodeWriter import MathplotCodeWriter
from .agents.tools.PythonCodeExecute import PythonCodeExecute

class ChartAssistant():
    def __init__(self,
            llm_mathplot_code_writer: MathplotCodeWriter = None,
            python_code_executor: PythonCodeExecute = None,
            show_code_stream: bool = True,
            public_hosting_url: str = None):
        
        self.mathplot_code_writer = llm_mathplot_code_writer or MathplotCodeWriter()
        self.python_code_executor = python_code_executor or PythonCodeExecute()
        self.public_hosting_url = public_hosting_url or os.getenv("PUBLIC_HOSTING_URL")
        self.show_code_stream = show_code_stream or False

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        base_file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        python_file_name = f"{base_file_name}.py"
        image_file_name = f"{base_file_name}.png"
        image_file_path = os.path.join(self.python_code_executor.temp_file_path, image_file_name)
        code_string = ""
        async for code_chunk in self.mathplot_code_writer.stream(question=question, context=context, conversation_history=conversation_history):
            code_string += code_chunk
            if self.show_code_stream:
                yield code_chunk
        code_string += f"\n\nplt.savefig(r'{image_file_path}')\n\n"
        await self.python_code_executor.run(python_code=code_string, save_file_name=python_file_name)
        yield f"\n\n🔗 **Chart Generated:** ![Generated Chart]({self.public_hosting_url}/{image_file_name})\n\n"