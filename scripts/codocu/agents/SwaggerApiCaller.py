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
        self.max_history_tokens_length = 6000
        self.swagger_json = None
        self.swagger_url = None
        self.api_url = None
        self.bearer_token = None
        self.allowed_api_paths = []

    def set_allowed_api_paths(self, allowed_api_paths: List[str]):
        self.allowed_api_paths = allowed_api_paths
        return self

    def set_bearer_token(self, bearer_token: str):
        self.bearer_token = bearer_token
        return self

    def set_swagger_url(self, swagger_url: str):
        response = requests.get(swagger_url)
        self.swagger_json = response.json()
        self.swagger_url = swagger_url
        self.api_url = re.sub(r"/swagger/v1/swagger.json", "", swagger_url)
        return self
    
    async def stream(self, question: str, messages: List[Message] = None):
        async with httpx.AsyncClient() as client:
            yield json.dumps({"response": f"🔎 Searching for relevant APIs ...\n\n"})
            api_path = self.get_swagger_api_to_call(question)
            yield json.dumps({"response": f"1. Creating request body for API: **{api_path}** ...\n\n"})
            request_body = self.get_request_body(question, api_path)
            yield json.dumps({"response": f"2. Request body: `{request_body}`\n\n"})
            for method, details in self.swagger_json["paths"].get(api_path).items():
                api_method = method
                print(api_method)

            print(f"{self.api_url}{api_path}")
            print(json.loads(request_body))
            print(f"Bearer {self.bearer_token}")

            response = requests.request(
                method=api_method,
                url=f"{self.api_url}{api_path}",
                headers={"Authorization": f"Bearer {self.bearer_token}"},
                json=json.loads(request_body)
            )
            print(response.json())
            yield json.dumps({"response": f"3. API Response: \n```json\n{response.json()}\n```\n\n"})

            prompt = f"""
            Given the following API response as json, describe in plain text format.
            Be concise, accurate and produce a well-structured response with bullet points.
            API Response: {response.json()}
            User Question: {question}
            Your Response:
            """

            async with client.stream("POST", self.url, json={"model": self.model, "prompt": prompt}) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    def run(self, question: str) -> str:
        response = self.get_raw_json_response(question)

        prompt = f"""
        Given the following API response as json, describe in plain text format.
        Be concise, accurate and produce a well-structured response with bullet points.
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
        for method, details in self.swagger_json["paths"].get(api_path).items():
            api_method = method

        request_body = self.get_request_body(question, api_path)
        response = requests.request(
            method=api_method,
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
    
    def get_request_body(self, question: str, api_path: str):
        # Check if the API path exists in the Swagger JSON
        if "paths" not in self.swagger_json or api_path not in self.swagger_json["paths"]:
            raise ValueError(f"API path '{api_path}' not found in the Swagger JSON.")
        
        api_params = self.swagger_json["paths"][api_path]
        
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
        AI Parameters: {json.dumps(api_params)}
        Schema Objects: {json.dumps(schema_objects)}
        Page: 1
        Limit: 5
        Question: {question}
        Return only the body as plain text, no explanation, in single line. Do not wrap in quotes or code blocks.
        The params inside the request body should contains MAXIMUM 01 most important word for each key.
        Example:
        Question: What is the detailed information about port hamburg including country, city, and port code?
        Result: {{'search': 'hamburg'}}
        Request Body: 
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
        cmd = self._clean_json_response(response.json())
        return cmd
    
    def set_max_history_tokens_length(self, max_history_tokens_length: int):
        self.max_history_tokens_length = max_history_tokens_length
        return self
    
    def _clean_json_response(self, response_data: dict) -> str:
        return response_data.get("response", "")