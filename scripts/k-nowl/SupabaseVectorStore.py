import requests

class SupabaseVectorStore:
    def __init__(self, url: str, token: str, table_name: str):
        self.url = url
        self.token = token
        self.table_name = table_name
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "apikey": self.token
        }
    
    def query_documents(self, query_embedding: list[float], match_count: int = 20, filter: dict = {}, function: str = "match_n8n_documents_bbc_bvms"):
        """
        Calls the function via Supabase RPC.

        :param query_embedding: A list of floats (size 768) representing the query embedding.
        :param match_count: Number of results to return.
        :param filter: A JSON object for metadata filtering.
        :return: A list of matching records.
        """
        rpc_endpoint = f"{self.url}/rest/v1/rpc/{function}"

        payload = {
            "query_embedding": query_embedding,
            "match_count": match_count,
            "filter": filter
        }

        response = requests.post(
            rpc_endpoint,
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Failed to execute RPC: {response.status_code}, {response.text}")

        return response.json()

    def insert_embedding(self, text: str, embedding: list[float], metadata: str = "", embedding2: list[float] = []):
        """
        Inserts an embedding into the Supabase Postgres database.
        
        :param text: The original text for which the embedding was created.
        :param embedding: A list of floats representing the embedding vector.
        :return: The response from the Supabase API call.
        """
        data = {
            "content": text,
            "metadata": { "extracted": metadata },
            "embedding": embedding,
            "embedding2": embedding2
        }
        
        response = requests.post(
            f"{self.url}/rest/v1/{self.table_name}",
            headers=self.headers,
            json=data
        )

        # Check if the insertion was successful
        if response.status_code != 201:
            raise Exception(f"Failed to insert embedding: {response.status_code}, {response.text}")
        
        return True