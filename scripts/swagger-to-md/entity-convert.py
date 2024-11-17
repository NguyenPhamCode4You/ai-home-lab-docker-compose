import json
import os

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

    # File paths
swagger_file_path = "./bvms-master.json"  # Update with your Swagger JSON file path
output_file = os.path.splitext(swagger_file_path)[0] + ".md"  # Use the same name with .md extension

# Load Swagger file
swagger_data = load_swagger_file(swagger_file_path)

# Generate Markdown file
create_entity_markdown(swagger_data, output_file)

print(f"Markdown file has been generated: '{output_file}'")