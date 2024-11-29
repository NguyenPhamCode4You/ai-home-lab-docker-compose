import json
from flask import Flask, request, jsonify
from FileHandler import FileHandler

app = Flask(__name__)

from JsonExtractor import JsonExtractor
from PackingListParser import PackingListParser

ollama_url="http://localhost:11434/api/generate"
model="qwen2.5-coder:14b-instruct-q6_K"
# model="gemma2:9b-instruct-q8_0"
extractor = JsonExtractor(url=ollama_url, model=model)
packingListParser = PackingListParser(url=ollama_url, model=model)
with open('./order-schema.json', 'r', encoding='utf-8') as file:
    schema = json.load(file)
    
@app.route('/extract-orders', methods=['POST'])
def extract_orders():
    # Parse the JSON data from the request body
    try:
        request_data = request.json  # Assumes `request.json` parses the JSON directly
    except Exception as e:
        return jsonify({"error": "Invalid JSON in request body."}), 400

    # Validate that the input is a list
    if not isinstance(request_data, list):
        return jsonify({"error": "Invalid input. Expected a list of objects."}), 400

    results = []

    # Process each item in the input list
    for item in request_data:
        # Validate that item contains the expected keys
        if not all(key in item for key in ["sednaMessageId", "bodyContent"]):
            return jsonify({"error": "Invalid object structure in list. Expected keys: 'sednaMessageId', 'bodyContent'."}), 400

        # Extract user input
        user_input = item.get("bodyContent", "")

        if not isinstance(schema, list):
            return jsonify({"error": "Invalid schema. Expected 'schema' to be a list of field objects."}), 400

        # Dynamically create the schema and process user input
        try:
            orders = extractor.set_schema(schema).run(user_input)
            for order in orders:
                results.append({
                    "sednaMessageId": item.get("sednaMessageId"),
                    **order,  # Unpack the response dictionary into the result
                })
        except Exception as e:
            return jsonify({"error": f"Error processing input: {str(e)}"}), 500

    return jsonify(results), 200

@app.route('/extract-packing-items', methods=['POST'])
def extract_packing_items():
    content = request.form.get('data')
    file = request.files['file']

    if not content and not file:
        return jsonify({'error': 'Both file and input is missing'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        file_handler = FileHandler(file)
        # Save the file
        file_handler.save_temp_file()
        # Convert the file to text
        content = file_handler.convert_file_to_text()
        file_handler.cleanup()

    items = packingListParser.run(content)
    return jsonify({"response": items}), 200

if __name__ == '__main__':
    app.run(port=1598)
