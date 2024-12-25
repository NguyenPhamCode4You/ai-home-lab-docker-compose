from src.ApiCallerAssistant import ApiCallerAssistant
from src.ChatBackend import create_chat_backend

from dotenv import load_dotenv
import os
load_dotenv()

assistant = ApiCallerAssistant(
    base_url="https://bvms-master-api-test.azurewebsites.net",
    bearer_token=os.getenv("BVMS_API_TOKEN"),
    api_instructions=[
        "/Vessels/Search - Method: POST - Description: Search for vessels using keywords, but cannot search for GUID, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL.",
        "/Ports/Search - Method: POST - Description: Search for ports using keywords, Body = {keySearch, pageSize} with pageSize default = 3, max = 5. No query in the URL.",
    ]
)

app = create_chat_backend(assistant)    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)