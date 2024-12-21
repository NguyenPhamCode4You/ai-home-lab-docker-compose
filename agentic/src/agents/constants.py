import os
from dotenv import load_dotenv
load_dotenv()

OLLAMA_CODE_MODEL = os.getenv("OLLAMA_CODE_MODEL")
OLLAMA_GENERAL_MODEL = os.getenv("OLLAMA_GENERAL_MODEL")