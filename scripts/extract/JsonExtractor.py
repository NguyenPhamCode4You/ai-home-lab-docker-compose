import json
import requests
from Helper import RecursiveSplitSentences, RemoveExcessiveSpacing

class JsonExtractor:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.prompt = None
        self.preprocessor = None
    
    def set_schema(self, schema_fields):
      schema_description = (
          "Your goal is to extract structured information from the user's input that matches the form described below. "
          "When extracting information, please make sure it matches the type information exactly. "
          "Do not add any attributes that do not appear in the schema shown below."
      )

      # Start building the schema representation
      schema_representation = "```TypeScript\n"
      schema_representation += "dataOutput: Array<{ // Details of items to be extracted.\n"

      for field in schema_fields:
          field_name = field.get("fieldName", "")
          field_type = field.get("dataType", "")
          field_description = field.get("description", "")
          field_line = f" {field_name}: {field_type} // {field_description}\n"
          schema_representation += field_line

      schema_representation += "}>\n```"

      # Add examples (if available) to the prompt
      examples = []
      for field in schema_fields:
          # Check if "examples" key exists and is a list
          field_examples = field.get("examples", [])
          if not isinstance(field_examples, list):
              continue  # Skip if "examples" is not a list

          for example in field_examples:
              # Ensure both "text" and "output" keys exist and are non-empty
              if not example.get("text") or not example.get("output"):
                  continue  # Skip incomplete examples

              # Build the object example and format it as JSON-like string
              object_example = {field["fieldName"]: example["output"]}
              object_example_json = str(object_example).replace("'", '"')  # Convert to valid JSON format

              # Append the formatted example to the examples list
              examples.append(
                  f"Input: {example['text']}\nOutput: <json>[{object_example_json}]</json>\n"
              )


      # Combine everything into the prompt
      prompt = f"{schema_description}\n\n{schema_representation}\n\n"
      prompt += (
          "Do not add any fields that are not in the schema. "
          "Do not use triple quotes or any other formatting in the output. "
          "Return only the json structure, no additional information, no triple quotes, no formatting, no explanations."
          "Wrap the json structure in <json> tags.\n\n"
      )
      prompt += "\n".join(examples)

      self.prompt = prompt
      return self

    def run(self, data: str) -> str:
        if data is None or len(data) == 0:
            return []
        
        prompt = self.prompt + f"\nNow extract from this text: {data}\nOutput: "
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": str(prompt), "stream": False}
        )
    
        if response.status_code != 200:
            print(f"Failed to extract chunk ")
            return []
        
        return self._clean_json_response(response.json())

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        print(f"Extracted JSON: {response}")
        response = response.replace("<json>", "").replace("</json>", "")
        response = response.replace("```", "").replace("json", "")
        print(f"Extracted JSON: {response}")
        try:
            return json.loads(response)
        except Exception as e:
            print(f"Failed to parse chunk {response}")
            return []