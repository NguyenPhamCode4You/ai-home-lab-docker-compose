import json
from typing import List
from .agents.JSONSummarizer import JSONSummarizer
from .agents.ApiConfigWritter import ApiConfigWritter
from .agents.tools.ApiCaller import ApiCaller

class ApiCallerAssistant():
    def __init__(self,
            llm_api_config_writter: ApiConfigWritter = None,
            llm_json_summarizer: JSONSummarizer = None,
            api_caller: ApiCaller = None,
            base_url: str = None,
            bearer_token: str = None,
            api_instructions: List[str] = []):
        
        self.api_config_writter = llm_api_config_writter or ApiConfigWritter()
        self.json_summarizer = llm_json_summarizer or JSONSummarizer()
        self.api_caller = api_caller or ApiCaller(base_url=base_url, bearer_token=bearer_token)
        self.api_instructions = api_instructions

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        api_instructions_string = "\n".join(self.api_instructions)
        api_config_string = await self.api_config_writter.run(question=question, context=api_instructions_string)
        api_config_lines = api_config_string.strip().split("\n")
        method = api_config_lines[0].lower().strip()
        api_path = api_config_lines[1].strip()
        body_object = json.loads(api_config_lines[2].strip())
        yield f"\n\n🔗 **Executing API:** `{method.upper()}`-`{api_path}` Body `{json.dumps(body_object)}`\n\n"
        api_response = await self.api_caller.run(api_path=api_path, method=method, body_object=body_object)
        async for summary_chunk in self.json_summarizer.stream(question=question, context=api_response):
            yield summary_chunk

