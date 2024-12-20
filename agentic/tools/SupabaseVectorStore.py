import os
import requests

from dotenv import load_dotenv
load_dotenv()

class SupabaseVectorStore:
    def __init__(self, embbeder, url: str = None, token: str = None):
        self.embbeder = embbeder
        self.url = url or os.getenv("SUPABASE_URL") or None
        self.token = token or os.getenv("SUPABASE_TOKEN") or None
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "apikey": self.token
        }
    
    def query_documents(self, function_name: str, question: str, match_count: int = 200):
        rpc_endpoint = f"{self.url}/rest/v1/rpc/{function_name}"
        payload = {
            "query_embedding": self.embbeder.run(question),
            "match_count": match_count,
            "filter": {}
        }
        response = requests.post(
            rpc_endpoint,
            headers=self.headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(f"Failed to execute RPC: {response.status_code}, {response.text}")
        return response.json()

    def insert_document(self, table_name: str, content: str, metadata: dict = None, summarize: str = None):
        response = requests.post(
            f"{self.url}/rest/v1/{table_name}",
            headers=self.headers,
            json={
                "content": content,
                "metadata": metadata or {},
                "summarize": summarize or "",
                "embedding": self.embbeder.run(metadata) if metadata else [],
                "embedding2": self.embbeder.run(summarize) if summarize else []
            }
        )
        # Check if the insertion was successful
        if response.status_code != 201:
            raise Exception(f"Failed to insert document: {response.status_code}, {response.text}")
        return True