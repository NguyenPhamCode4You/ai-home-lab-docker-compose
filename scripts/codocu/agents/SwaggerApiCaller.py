import asyncio
from http import client
import json
import re
from fastapi import Request
import httpx
import requests
from typing import List, Optional

class Message():
    role: str  # e.g., "user", "assistant"
    content: str  # Message text

# Main assistant class
class SwaggerApiCaller:
    def __init__(
        self,
        url: str = "http://localhost:11434/api/generate",
        model: str = "gemma2:9b-instruct-q8_0"
    ):
        self.url = url
        self.model = model
        self.swagger_json = None
        self.api_url = None
        self.bearer_token = None
        self.allowed_api_paths = []

    def set_swagger_json(self, swagger_json: str):
        self.swagger_json = json.loads(swagger_json)
        return self

    def set_allowed_api_paths(self, allowed_api_paths: List[str]):
        self.allowed_api_paths = allowed_api_paths
        return self

    def set_bearer_token(self, bearer_token: str):
        self.bearer_token = bearer_token
        return self

    def set_api_url(self, api_url: str):
        self.api_url = api_url
        return self
    
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
        def clean_config_string(config_string: str) -> str:
            return config_string.strip().replace("\n", "").replace("\r", "").replace(" ", "")
        async with httpx.AsyncClient() as client:
            yield json.dumps({"response": f"🧮 Looking up for the correct API to call ...\n\n"})
            api_path = self.get_swagger_api_to_call(question)
            yield json.dumps({"response": f"1. Creating request body for API: `{self.api_url}{api_path}`\n\n"})
            await asyncio.sleep(1)
            method, api_path, request_body = self.get_request_configuration(question, api_path)
            method = clean_config_string(method)
            api_path = clean_config_string(api_path)
            yield json.dumps({"response": f"2. `{method.upper()}` - `{api_path}` - Body: `{request_body}`\n\n"})
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
                yield json.dumps({"response": f"❌ API call failed: {e}\n\n"})
                return
            except Exception as e:
                yield json.dumps({"response": f"❌ Unexpected error: {str(e)}\n\n"})
                return
            yield json.dumps({"response": f"✅ API call successful! Parsing response...\n\n"})
            api_response = response.json()
            response_markdown = self.convert_json_into_markdown(api_response)
            prompt = f"""
            Given the following API response as json, describe in plain text format.
            Be concise, accurate and produce a well-structured response with bullet points.
            API Response: {response_markdown}
            User Question: {question}
            Your Response:
            """
            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def run(self, question: str) -> str:
        response = self.get_raw_json_response(question)

        prompt = f"""
        Given the following API response, produce a well-structured markdown table to demonstrate the response.
        API Response: {json.dumps(response)}
        User Question: {question}
        Your Response:
        """
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        return self._clean_json_response(response.json())
    
    def get_raw_json_response(self, question: str):
        api_path = self.get_swagger_api_to_call(question)
        request_body, method = self.get_request_configuration(question, api_path)
        response = requests.request(
            method=method,
            url=f"{self.api_url}{api_path}",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            json=json.loads(request_body)
        )
        return response.json()
    
    def get_swagger_api_to_call(self, question: str):
        prompt = f"""
        Given the following API paths, please select 01 api that best matches the question:
        {'\n'.join(self.allowed_api_paths)}
        Question: {question}
        Return only the selected API path as plain text, no code or formatting, no explanation.
        Example: /Vessel/Search
        Selected API path:
        """
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        api_path = self._clean_json_response(response.json())
        api_path = api_path.strip()
        api_path = api_path.split("\n")[-1].replace(" ", "")
        return api_path
    
    def get_schema_object_names_for_api_path(self, api_path: str):
        path = self.swagger_json["paths"].get(api_path)
        schemas = set()  # Use a set to avoid duplicates
        # Loop through all HTTP methods (e.g., GET, POST) for the path
        for method, details in path.items():
            # Look for parameters and extract schema from them
            request_body = details.get('requestBody', {}).get('content', {})
            for media_type, content in request_body.items():
                schema = content.get('schema', {})
                if schema:
                    schemas.add(schema.get('$ref').split("/")[-1])

        return list(schemas)
    
    def get_request_configuration(self, question: str, api_path: str):
        # Check if the API path exists in the Swagger JSON
        if "paths" not in self.swagger_json or api_path not in self.swagger_json["paths"]:
            raise ValueError(f"API path '{api_path}' not found in the Swagger JSON.")
        
        api_params = self.swagger_json["paths"][api_path]
        method = list(api_params.keys())[0]
        
        # Ensure that the get_schema_object_names_for_api_path method is implemented properly
        schema_object_names = self.get_schema_object_names_for_api_path(api_path)
        
        # Initialize schema_objects dictionary
        schema_objects = {}
        
        # Check if components and schemas are present
        if "components" not in self.swagger_json or "schemas" not in self.swagger_json["components"]:
            raise ValueError("Schemas are not defined in the Swagger JSON components section.")
        
        # Loop through schema object names and retrieve schema details
        for schema in schema_object_names:
            if schema in self.swagger_json["components"]["schemas"]:
                schema_info = self.swagger_json["components"]["schemas"][schema]
                schema_objects[schema] = schema_info
            else:
                raise ValueError(f"Schema '{schema}' not found in components/schemas.")

        # Prepare the prompt for the AI model
        prompt = f"""
        Given the following API documentation as json, please return the request body in json format:
        API path: {api_path}
        AI Parameters: {json.dumps(api_params)}
        Schema Objects: {json.dumps(schema_objects)}
        Page: 1 (Default)
        Limit: 1 (Default) - 5 (Maximum)
        Question: {question}
        Return the correct api path (1st) and request body (2nd) in json format, reperated by new line.
        Both api apth and request body should be plain text, in single line. Do not wrap in quotes or code blocks.
        For search related APIs, the keyword to search should NOT be modified, and should be less than 3 words.
        - if the search keyword is "port hamburg", use "hamburg" only
        - if the search keyword is "vessel BBC Hamburg", use "BBC Hamburg" only
        If body is not required, return empty object.
        Always use double quotes for keys and values.
        Example:
        Question: What is the detailed information about port hamburg including country, city, and port code?
        Result:
        /Vessel/Search
        {{"search": "hamburg"}}
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
        [api_path, body] = result.split("\n")
        return method, api_path, body
    
    def _clean_json_response(self, response_data: dict) -> str:
        return response_data.get("response", "")