import json
from flask import Flask, request, jsonify
from FileHandler import FileHandler

app = Flask(__name__)

from JsonExtractor import JsonExtractor
ollama_url="http://10.13.13.4:11434/api/generate"

@app.route('/extract-from-schema', methods=['POST'])
def extract_from_schema():
    try:
        request_data = request.json
        schema = request_data.get("schema")
        user_input = request_data.get("data", "")

        if not isinstance(schema, list):
            return jsonify({"error": "Invalid input. Expected 'schema' to be a list of field objects."}), 400

        # Dynamically create the schema
        extractor = JsonExtractor(url=ollama_url)
        response = extractor.set_schema(schema).run(user_input)
        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/extract-from-file', methods=['POST'])
def extract_from_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Extract additional JSON data from the request
    schema = request.form.get('schema')
    if not schema:
        return jsonify({'error': 'Schema is missing'}), 400

    try:
        # Attempt to parse schema as JSON
        schema = json.loads(schema)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid input. 'schema' must be a valid JSON string."}), 400

    # Validate that the parsed schema is a list
    if not isinstance(schema, list):
        return jsonify({"error": "Invalid input. Expected 'schema' to be a list of field objects."}), 400


    file_handler = FileHandler(file)
    try:
        # Save the file
        file_handler.save_temp_file()

        # Convert the file to text
        content = file_handler.convert_file_to_text()
        print(content)

        # Cleanup the temporary file
        file_handler.cleanup()

        # Dynamically create the schema
        extractor = JsonExtractor(url=ollama_url)
        response = extractor.set_schema(schema).run(content)
        return jsonify({"response": response}), 200
    
    except Exception as e:
        file_handler.cleanup()
        return f"Failed to process file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
