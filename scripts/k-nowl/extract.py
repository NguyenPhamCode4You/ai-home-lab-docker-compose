import json
from flask import Flask, request, jsonify

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
        print(response)


        # Remove <json> tags
        response = response.replace("<json>", "").replace("</json>", "")

        try:
            # Parse the JSON string into a dictionary
            response = json.loads(response)
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

        # Return the parsed response
        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
