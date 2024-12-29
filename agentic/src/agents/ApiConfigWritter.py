from .Task import Task
from .models.Ollama import Ollama

from .constants import OLLAMA_CODE_MODEL

class ApiConfigWritter(Task):
    def __init__(self):
        super().__init__(
            task_name="api-config-writer",
            llm_model=Ollama(
                model=OLLAMA_CODE_MODEL
            ),
            instruction_template="""
                Given the following API endpoints:
                -------------------
                {context}
                -------------------

                User is asking for the following information:
                -------------------
                {question}
                -------------------

                Return the correct method (1st), api path (2nd) and request body (3rd), separated by new line to make the API call.
                Method, api path and request body (as json object) should be returned as plain text. Do not wrap in quotes or code blocks.

                Important Notes:
                1. For search related APIs, the keyword to search should be less than 3 words.
                - if the search keyword is "port hamburg", use "hamburg" only
                - if the search keyword is "vessel BBC Hamburg", use "BBC Hamburg" only
                
                2. For GET API with GUIDs or IDs, exact GUIDs or IDs from the conversation and make the correct API path from it.

                3. If request body is not mentioned, always return an empty object.
                4. Always use double quotes for keys and values.

                Example Question: What is the detailed information about port hamburg including country, city, and port code?
                Then the Result should be:
                get
                /vessels
                {{"search": "hamburg"}}
            """
        )