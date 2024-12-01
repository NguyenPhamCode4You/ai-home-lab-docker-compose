import requests


class Tools:
    def __init__(self):
        pass

    async def get_bvms_documents(self, question: str, __event_emitter__=None) -> str:
        """
        Get documents and answer a question from the BVMS
        """

        base_url = "http://localhost:8000/api/answer"
        body = {"messages": [{"role": "user", "content": question}]}

        try:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching BVMS documents...",
                        "done": False,
                    },
                }
            )

            # Send the request to fetch the documents
            response = requests.post(base_url, json=body)
            response.raise_for_status()  # Ensure the request was successful

            # Parse the response
            data = response.json()
            answer = data["answer"]

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Success fetching BVMS documents!",
                        "done": True,
                    },
                }
            )

            await __event_emitter__(
                {
                    "type": "message",
                    "data": {
                        "content": "Answer: " + answer,
                    },
                }
            )

            return "Do nothing!"

        except requests.RequestException as e:
            return f"Error fetching BVMS answer: {str(e)}"
