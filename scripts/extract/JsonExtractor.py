import json
import requests
from Helper import RecursiveSplitSentences

class JsonExtractor:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.prompt = None

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
          field_line = f" {field['fieldName']}: {field['dataType']} // {field['description']}\n"
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
          "Please output the extracted information in JSON format. "
          "Do not output anything except for the extracted information. "
          "Do not add any clarifying information. "
          "Do not add any fields that are not in the schema. "
          "If the text contains attributes that do not appear in the schema, please ignore them. "
          "All output must be in JSON format and follow the schema specified above. Wrap the JSON in <json> tags.\n\n"
      )
      prompt += "\n".join(examples)

      self.prompt = prompt
      return self

    def run(self, data: str) -> str:
        chunks = RecursiveSplitSentences(data, limit=4000, overlap=0)
        chunks = [chunk for chunk in chunks if len(chunk) > 0]
        current = 1
        total = len(chunks)
        extracted_items = []

        for chunk in chunks:
            print(f"Extracting chunk: {current}/{total}")
            prompt = self.prompt + f"\nNow extract from this text: {chunk}\nOutput: "
            response = requests.post(
                url=self.url,
                json={"model": self.model, "prompt": str(prompt), "stream": False}
            )
        
            # Check if the response is successful
            if response.status_code != 200:
                print(f"Failed to extract chunk {current}/{total}.")
            else:
                try:
                    items = self._clean_json_response(response.json())
                    extracted_items.extend(items)
                    print(f"Successfully - found {len(items)} items in chunk {current}/{total}.")

                except Exception as e:
                    print(f"Failed to parse chunk {current}/{total}. Error: {e}")
            
            current += 1

        print(f"Extraction complete. Total items extracted: {len(extracted_items)}")
        return extracted_items

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        response = response.replace("<json>", "").replace("</json>", "")
        return json.loads(response)