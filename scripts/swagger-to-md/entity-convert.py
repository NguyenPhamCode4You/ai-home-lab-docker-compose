import json
import os
import requests

def load_swagger_file_from_url(url, local_file_path):
    """Downloads the Swagger JSON file from a URL and saves it locally."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP issues
    with open(local_file_path, 'w') as file:
        file.write(response.text)

def load_swagger_file(file_path):
    """Loads the Swagger JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def create_simple_markdown(api_details, output_file):
    """Generates a simplified Markdown file for API endpoints."""
    content = f"# API Documentation\n\n"

    for path, methods in api_details['paths'].items():
        for method, details in methods.items():
            content += f"## {path}\n"
            content += f"- **Method:** {method.upper()}\n"

            # Request body
            request_body = details.get('requestBody', {}).get('content', {})
            content += "- **Request:** "
            if request_body:
                content += parse_data_structure(request_body, api_details)
            else:
                content += "No request body.\n"

            # Response data
            responses = details.get('responses', {})
            content += "- **Response:** "
            if responses:
                content += parse_response_structure(responses, api_details)
            else:
                content += "No responses provided.\n"

            content += "\n---\n\n"

    # Write to file
    with open(output_file, 'w') as file:
        file.write(content)

def parse_data_structure(content, api_details):
    """Parses and formats the data structure from request or response content."""
    for media_type, details in content.items():
        schema = details.get('schema', {})
        return resolve_and_parse_schema(schema, api_details)
    return "No schema provided.\n"

def parse_response_structure(responses, api_details):
    """Parses and formats the response structure."""
    for status_code, response in responses.items():
        description = response.get('description', 'No description provided.')
        content = response.get('content', {})
        for media_type, details in content.items():
            schema = details.get('schema', {})
            return resolve_and_parse_schema(schema, api_details)
    return "No schema provided.\n"

def resolve_and_parse_schema(schema, api_details):
    """Resolves schema references and parses the schema object."""
    components = api_details.get('components', {}).get('schemas', {})
    entity_name = schema.get('$ref', '').split('/')[-1] if '$ref' in schema else "AnonymousEntity"
    fields = []

    # If $ref is found, resolve the reference
    if '$ref' in schema and entity_name in components:
        resolved_schema = components[entity_name]
        fields = parse_schema_properties(resolved_schema)
    elif 'properties' in schema:
        # Direct properties without $ref
        fields = parse_schema_properties(schema)

    fields_str = "|".join(fields)
    return f"Entity=[{entity_name}]|Fields=[{fields_str}]\n"

def parse_schema_properties(schema):
    """Parses schema properties into fields."""
    fields = []
    for field_name, field_details in schema.get('properties', {}).items():
        field_type = field_details.get('type', 'unknown')
        fields.append(f"{field_name}:{field_type}")
    return fields

# URL of the Swagger JSON file
swagger_url = "https://bvms-master-api-test.azurewebsites.net/swagger/v1/swagger.json"  # Replace with the actual URL
local_swagger_file = "./swagger.json"  # Local file path for saving the Swagger file
output_file = os.path.splitext(local_swagger_file)[0] + "_simple.md"  # Output Markdown file name

# Download Swagger JSON file
load_swagger_file_from_url(swagger_url, local_swagger_file)

# Load Swagger data
swagger_data = load_swagger_file(local_swagger_file)

# Generate Markdown file
create_simple_markdown(swagger_data, output_file)

print(f"Markdown file has been generated: '{output_file}'")

