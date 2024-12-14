import asyncio
import json
import httpx
import requests
from typing import List

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

def clean_config_string(config_string: str) -> str:
    return config_string.strip().replace("\n", "").replace("\r", "").replace(" ", "")

# Main assistant class
class SwaggerApiCaller:
    def __init__(
        self,
        url: str = "http://localhost:11434",
        model: str = "gemma2:9b-instruct-q8_0",
        api_url: str = None,
        bearer_token: str = None,
        user_instructions: str = None,
        allowed_api_paths: List[str] = [],
    ):
        self.url = f"{url}/api/generate"
        self.model = model
        self.api_url = api_url
        self.bearer_token = bearer_token
        self.user_instructions = user_instructions
        self.allowed_api_paths = allowed_api_paths

    def convert_json_into_markdown(self, json_data: dict) -> str:
        result = ""
        for key, value in json_data.items():
            if isinstance(value, dict):
                # Use the first key of the object as a header
                first_key = next(iter(value.keys()), None)
                if first_key:
                    result += f"## {first_key}\n"
                result += self.convert_json_into_markdown(value)
            elif isinstance(value, list):
                # Skip large lists to avoid verbosity
                if len(value) > 5:
                    continue
                result += f"# {key}\n"
                for item in value:
                    if isinstance(item, dict):
                        # Use the first key of each object in the list as a header
                        first_key = next(iter(item.keys()), None)
                        if first_key:
                            result += f"## {first_key}\n"
                        result += self.convert_json_into_markdown(item)
                    else:
                        result += f"- {item}\n"
            else:
                result += f"- {key}: {value}\n"
        return result
    
    async def stream(self, question: str, messages: List[Message] = None):
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            yield json.dumps({"response": f"\n\n🧮 Looking up for the correct API to call ...\n\n"})
            api_paths = self.get_swagger_apis_to_call(question)
            self_awareness_context = ""
            api_paths = [api_path for api_path in api_paths.split("\n") if api_path.strip()]
            yield json.dumps({"response": f"\n\n🔍 Need to call these apis: {','.join([f"`{path}`" for path in api_paths])}\n\n"})
            for index, api_path in enumerate(api_paths):
                mention_id_prompt = ""
                if index + 1 < len(api_paths):
                    next_api_path = api_paths[index + 1]
                    if "id}" in next_api_path.lower() or "guid}" in next_api_path.lower():
                        mention_id_prompt = "Firsly, extract the unique identifier (GUID or ID) using this format: **Record Name**: **GUID**"
                api_path = clean_config_string(api_path)
                yield json.dumps({"response": f"\n\n- Creating request body for API: `{self.api_url}{api_path}`\n\n"})
                await asyncio.sleep(2)
                final_question = f"Some additional context for the question: {self_awareness_context}\n\nFinal User Question: {question}"
                method, api_path, request_body = self.get_request_configuration(final_question, api_path)
                method = clean_config_string(method)
                api_path = clean_config_string(api_path)
                yield json.dumps({"response": f"\n\n- `{method.upper()}` - `{api_path}` - Body: `{request_body}`\n\n"})
                await asyncio.sleep(1)
                try:
                    response = await client.request(
                        method=method,
                        url=f"{self.api_url}{api_path}",
                        headers={"Authorization": f"Bearer {self.bearer_token}"},
                        json=json.loads(request_body)
                    )
                    response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses
                except httpx.HTTPStatusError as e:
                    yield json.dumps({"response": f"\n\n❌ API call failed: {e}\n\n"})
                    continue
                except Exception as e:
                    yield json.dumps({"response": f"\n\n❌ Unexpected error: {str(e)}\n\n"})
                    continue
                yield json.dumps({"response": f"\n\n✅ API call successful! Parsing response...\n\n"})
                api_response = response.json()
                
                prompt = f"""
                Given the following response:
                -------------------
                {api_response}
                -------------------
                
                {mention_id_prompt}

                Instruction from user:
                -------------------
                {self.user_instructions}
                -------------------

                User Question: 
                -------------------
                {question}
                -------------------

                Describe the response in plain text format, conform to the user's question. 
                Be concise, accurate and produce a well-structured response with bullet points.
                DO NOT make up information not present in the response.

                Important:
                - Provide minimal details and avoid verbosity unless user asks for it.

                """
                async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                    async for chunk in response.aiter_bytes():
                        if (len(chunk) > 1000):
                            continue
                        self_awareness_context += json.loads(chunk)["response"]
                        yield chunk

    def get_swagger_apis_to_call(self, question: str):
        api_definitions = [f"{path}: {details}" for path, details in self.allowed_api_paths]
        prompt = f"""
        Given the following API definitions:
        -------------------
        {'\n'.join(api_definitions)}
        -------------------

        User instruction on how to use the API:
        -------------------
        {self.user_instructions}
        -------------------

        User is asking for the following:
        -------------------
        {question}
        -------------------

        Paycareful attention to the instruction to select the correct APIs to call.
        Multiple APIs can be called in sequence to get the desired information.
        Seperate multiple APIs with a new line, and return the API path only, as plain text, no quotes or code blocks.
        
        Example: 
        /Search1
        /Search2

        """
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        api_path = self._clean_json_response(response.json())
        return api_path.strip()
    
    def get_request_configuration(self, question: str, api_path: str):
        documenation = ""
        # Prepare the prompt for the AI model
        for path, details in self.allowed_api_paths:
            if path == api_path:
                documenation = details
                break
        if not documenation:
            raise Exception(f"API Path {api_path} not found in the allowed API paths")
        
        prompt = f"""
        Given the following API documentation:
        -------------------
        API Path: {api_path}
        Documentation: {documenation}
        -------------------
        
        -------------------
        User question: {question}
        -------------------

        Return the correct method (1st), api path (2nd) and request body (3rd), reperated by new line to make the API call.
        Method, api apth and request body (as json object) should be returned as plain text. Do not wrap in quotes or code blocks.

        For search related APIs, the keyword to search should be less than 3 words.
        - if the search keyword is "port hamburg", use "hamburg" only
        - if the search keyword is "vessel BBC Hamburg", use "BBC Hamburg" only
        
        For GET API with GUIDs or IDs, exact GUIDs or IDs from the conversation and make the correct API path from it.

        If request body is not mentioned, always return an empty object.
        Always use double quotes for keys and values.

        Example:
        Question: What is the detailed information about port hamburg including country, city, and port code?
        Result:
        Method: search
        API Path: /Vessel/Search
        Request Body: {{"search": "hamburg"}}
        """
        
        # Send the prompt to the AI model and get the response
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        
        # Check for successful response
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        
        # Get the clean response and append the Bearer Token
        result = self._clean_json_response(response.json())
        lines = result.strip().split("\n")
        # Extract and process each line
        method = lines[0].split(":", 1)[1].strip().lower()
        api_path = lines[1].split(":", 1)[1].strip()
        body = ":".join(lines[2].split(":", 1)[1:]).strip()

        return method, api_path, body
    
    def _clean_json_response(self, response_data: dict) -> str:
        return response_data.get("response", "")