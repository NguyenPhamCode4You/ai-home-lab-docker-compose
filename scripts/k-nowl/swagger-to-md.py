import json
import os

def load_swagger_file(file_path):
    """Loads the Swagger JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def create_markdown(api_details, output_dir):
    """Creates Markdown files for each API endpoint and data structure."""
    os.makedirs(output_dir, exist_ok=True)

    # Write each API endpoint documentation
    for path, methods in api_details['paths'].items():
        for method, details in methods.items():
            # Construct file name and path
            file_name = f"{method.upper()}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}.md"
            file_path = os.path.join(output_dir, file_name)

            # Construct Markdown content
            content = f"# {method.upper()} {path}\n\n"
            content += f"**Summary:** {details.get('summary', 'No summary provided.')}\n\n"
            content += f"**Description:** {details.get('description', 'No description provided.')}\n\n"

            # Parameters
            if 'parameters' in details:
                content += "## Parameters\n\n"
                for param in details['parameters']:
                    content += f"- **{param['name']}** ({param['in']}): {param.get('description', 'No description.')}\n"

            # Request body
            if 'requestBody' in details:
                content += "\n## Request Body\n\n"
                content += parse_schema(details['requestBody'].get('content', {}))

            # Responses
            content += "\n## Responses\n\n"
            for status_code, response in details.get('responses', {}).items():
                content += f"### {status_code}\n\n"
                content += f"**Description:** {response.get('description', 'No description provided.')}\n\n"
                if 'content' in response:
                    content += parse_schema(response['content'])

            # Write to file
            with open(file_path, 'w') as file:
                file.write(content)

def parse_schema(content):
    """Parses and formats a schema from the OpenAPI content field."""
    markdown = ""
    for media_type, details in content.items():
        markdown += f"- **Media Type:** {media_type}\n\n"
        schema = details.get('schema', {})
        if schema:
            markdown += parse_schema_object(schema)
    return markdown

def parse_schema_object(schema, indent=0):
    """Recursively parses schema objects and formats them in Markdown."""
    indent_str = ' ' * indent
    markdown = ""
    if 'type' in schema:
        markdown += f"{indent_str}- **Type:** {schema['type']}\n"
    if 'properties' in schema:
        markdown += f"{indent_str}- **Properties:**\n"
        for prop_name, prop_details in schema['properties'].items():
            markdown += f"{indent_str}  - **{prop_name}:** {prop_details.get('type', 'unknown')}\n"
            markdown += parse_schema_object(prop_details, indent + 4)
    if 'items' in schema:
        markdown += f"{indent_str}- **Items:**\n"
        markdown += parse_schema_object(schema['items'], indent + 4)
    return markdown

def main():
    # File paths
    swagger_file_path = "./bvms-master.json"  # Update with your Swagger JSON file path
    output_dir = "./"  # Output directory for Markdown files

    # Load Swagger file
    swagger_data = load_swagger_file(swagger_file_path)

    # Generate Markdown files
    create_markdown(swagger_data, output_dir)

    print(f"Markdown files have been generated in '{output_dir}'.")