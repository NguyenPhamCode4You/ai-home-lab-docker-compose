import json
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel
from FileHandler import FileHandler
from JsonExtractor import JsonExtractor
from PackingListParser import PackingListParser

app = FastAPI()

ollama_url = "http://10.13.13.4:11434/api/generate"
model = "qwen2.5-coder:14b-instruct-q6_K"

extractor = JsonExtractor(url=ollama_url, model=model)
packingListParser = PackingListParser(url=ollama_url, model=model)

class ExtractFromSchemaRequest(BaseModel):
    schema: list
    data: str = ""

@app.post("/extract-from-schema")
async def extract_from_schema(request_data: ExtractFromSchemaRequest):
    try:
        schema = request_data.schema
        user_input = request_data.data

        if not isinstance(schema, list):
            raise HTTPException(status_code=400, detail="Invalid input. Expected 'schema' to be a list of field objects.")

        # Dynamically create the schema
        response = extractor.set_schema(schema).run(user_input)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post('/extract-from-file')
async def extract_from_file(
    file: UploadFile = File(...),
    schema: str = Form(...)
):
    try:
        # Parse schema from the form data
        try:
            parsed_schema = json.loads(schema)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid input. 'schema' must be a valid JSON string.")

        # Validate that the parsed schema is a list
        if not isinstance(parsed_schema, list):
            raise HTTPException(status_code=400, detail="Invalid input. Expected 'schema' to be a list of field objects.")

         # Get the file stream and filename directly from the UploadFile
        file_stream = file.file
        filename = file.filename  # Use the filename from UploadFile

        # Pass the stream and filename to FileHandler
        file_handler = FileHandler(file_stream, filename)

        # Save the file temporarily and convert its content to text
        file_handler.save_temp_file()
        content = file_handler.convert_file_to_text()
        print(f"Extracted content: {content}")

        # Cleanup the temporary file
        file_handler.cleanup()

        # Process the content with the schema
        response = extractor.set_schema(parsed_schema).run(content)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=11233)
