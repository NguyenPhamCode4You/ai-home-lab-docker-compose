import os
from typing import List
import requests

from dotenv import load_dotenv
load_dotenv()

class SupabaseVectorStore:
    def __init__(self, embedding, url: str = None, token: str = None):
        self.embedding = embedding
        self.url = url or os.getenv("SUPABASE_URL") or None
        self.token = token or os.getenv("SUPABASE_TOKEN") or None
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "apikey": self.token
        }

    def get_documents_string(self, function_name: str, question: str, match_count: int = 200):
        documents = self.query(function_name, question, match_count)
        sections = self.organize_documents(documents)
        context_result = ""
        for section in sections:
            title = section["title"]
            if "#" not in title:
                title = f"# {title}"
            context = section["context"]
            context_result += f"{title}\n\n{context}\n\n"
        return context_result
    
    def query(self, function_name: str, question: str, match_count: int = 200):
        rpc_endpoint = f"{self.url}/rest/v1/rpc/{function_name}"
        payload = {
            "query_embedding": self.embedding.run(question),
            "match_count": match_count,
            "filter": {}
        }
        # print the payload as json text
        print(f"Payload: {payload}")
        response = requests.post(
            rpc_endpoint,
            headers=self.headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(f"Failed to execute RPC: {response.status_code}, {response.text}")
        return response.json()

    def insert(self, table_name: str, content: str, metadata: dict = None, summarize: str = None):
        response = requests.post(
            f"{self.url}/rest/v1/{table_name}",
            headers=self.headers,
            json={
                "content": content,
                "metadata": metadata or {},
                "summarize": summarize or "",
                "embedding": self.embedding.run(metadata) if metadata else [],
                "embedding2": self.embedding.run(summarize) if summarize else []
            }
        )
        # Check if the insertion was successful
        if response.status_code != 201:
            raise Exception(f"Failed to insert document: {response.status_code}, {response.text}")
        return True
    
    def organize_documents(self, documents: List[dict]) -> List[dict]:
        titles = [document["content"].split(":")[0] for document in documents]
        unique_titles = list(dict.fromkeys(titles))
        sections = []
        for title in unique_titles:
            counts = len([doc for doc in documents if doc["content"].split(":")[0] == title])
            docs = [
                document["content"].replace(title, "", 1).replace(":", "", 1).strip()
                for document in documents
                if document["content"].split(":")[0] == title
            ]
            context = "\n".join(docs)
            sections.append({"title": title, "counts": counts, "context": context})
        return sections