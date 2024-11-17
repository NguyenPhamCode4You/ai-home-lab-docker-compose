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

def create_entity_markdown(api_details, output_file):
    """Creates a Markdown file documenting all entities (schemas) in the Swagger file."""
    content = f"# Entities Documentation\n\n"
    content += f"Generated from `{os.path.basename(output_file)}`.\n\n"

    # Extract components/schemas
    schemas = api_details.get('components', {}).get('schemas', {})

    if not schemas:
        content += "No schemas found in the Swagger file.\n"
    else:
        for entity_name, entity_details in schemas.items():
            content += f"## {entity_name}\n\n"
            content += f"**Description:** {entity_details.get('description', 'No description provided.')}\n\n"
            content += parse_schema_object(entity_details)
            content += "\n---\n\n"

    # Write to file
    with open(output_file, 'w') as file:
        file.write(content)

def parse_schema_object(schema, indent=0):
    """Recursively parses schema objects and formats them in Markdown."""
    indent_str = ' ' * indent
    markdown = ""

    if 'type' in schema:
        markdown += f"{indent_str}- **Type:** {schema['type']}\n"
    if 'properties' in schema:
        markdown += f"{indent_str}- **Properties:**\n"
        for prop_name, prop_details in schema['properties'].items():
            markdown += f"{indent_str}  - **{prop_name}:** {prop_details.get('type', 'unknown')} "
            markdown += f"({prop_details.get('description', 'No description provided.')})\n"
            markdown += parse_schema_object(prop_details, indent + 4)
    if 'items' in schema:
        markdown += f"{indent_str}- **Items:**\n"
        markdown += parse_schema_object(schema['items'], indent + 4)
    if 'enum' in schema:
        markdown += f"{indent_str}- **Allowed Values:** {', '.join(map(str, schema['enum']))}\n"
    if '$ref' in schema:
        ref_name = schema['$ref'].split('/')[-1]
        markdown += f"{indent_str}- **Reference:** {ref_name}\n"

    return markdown

# URL of the Swagger JSON file
swagger_url = "https://bvms-master-api-test.azurewebsites.net/swagger/v1/swagger.json"  # Replace with the actual URL
local_swagger_file = "./bvms-master.json"  # Local file path for saving the Swagger file
output_file = os.path.splitext(local_swagger_file)[0] + ".md"  # Output Markdown file name

# Download Swagger JSON file
load_swagger_file_from_url(swagger_url, local_swagger_file)

# Load Swagger data
swagger_data = load_swagger_file(local_swagger_file)

# Generate Markdown file
create_entity_markdown(swagger_data, output_file)

print(f"Markdown file has been generated: '{output_file}'")

