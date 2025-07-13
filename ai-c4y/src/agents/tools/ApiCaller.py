import httpx

class ApiCaller:
    def __init__(self, base_url: str, bearer_token: str):
        self.base_url = base_url
        self.bearer_token = bearer_token

    async def run(self, api_path: str, method: str = 'get', body_object = {}):
        headers= {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
        api_url = f'{self.base_url}{api_path}'
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            try:
                response = await client.request(
                    method=method,
                    url=api_url,
                    headers=headers,
                    json=body_object
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f'ApiClaller Error: {e}')
                return None