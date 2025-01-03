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
            allowed_fields: List[str] = None,
            api_instructions: List[str] = []):
        
        self.api_config_writter = llm_api_config_writter or ApiConfigWritter()
        self.json_summarizer = llm_json_summarizer or JSONSummarizer()
        self.api_caller = api_caller or ApiCaller(base_url=base_url, bearer_token=bearer_token)
        self.api_instructions = api_instructions or []
        self.allowed_fields = allowed_fields or None

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        api_instructions_string = "\n".join(self.api_instructions)
        api_config_string = await self.api_config_writter.run(question=question, context=api_instructions_string)
        api_config_lines = api_config_string.strip().split("\n")
        method = api_config_lines[0].lower().strip()
        api_path = api_config_lines[1].strip()
        body_object = json.loads(api_config_lines[2].strip())
        yield f"\n\n🔗 **Executing API:** `{method.upper()}`-`{api_path}` Body `{json.dumps(body_object)}`\n\n"
        api_response = await self.api_caller.run(api_path=api_path, method=method, body_object=body_object)
        if self.allowed_fields is not None:
            api_response = filter_json(api_response, self.allowed_fields)
            print(f"filtered_response: {api_response}")
        async for summary_chunk in self.json_summarizer.stream(question=question, context=api_response):
            yield summary_chunk

def filter_json(data, allowed_fields):
    """
    Recursively filters a JSON-like object, keeping only the fields in the allowed_fields list.
    Supports wildcard matching for including all fields of a child object.
    
    :param data: The JSON-like object (dictionary, list, or primitive).
    :param allowed_fields: A set or list of allowed field names or patterns (e.g., "object.*").
    :return: Filtered JSON-like object.
    """
    def is_allowed(key):
        """
        Check if a key is explicitly allowed or matches a wildcard pattern (e.g., "object.*").
        """
        if key in allowed_fields:
            return True
        for field in allowed_fields:
            if field.endswith(".*") and key == field[:-2]:
                return True
        return False

    if isinstance(data, dict):  # If data is an object
        filtered_data = {}
        for key, value in data.items():
            if key in allowed_fields:  # Explicitly allowed field
                filtered_data[key] = filter_json(value, allowed_fields)
            elif is_allowed(key):  # Include all fields if it matches "key.*"
                filtered_data[key] = value  # Include all child fields as-is
        return filtered_data
    elif isinstance(data, list):  # If data is an array
        return [filter_json(item, allowed_fields) for item in data]
    else:  # If data is a primitive
        return data

