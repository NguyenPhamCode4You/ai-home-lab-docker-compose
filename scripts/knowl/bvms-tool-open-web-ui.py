import requests


class Tools:
    def __init__(self):
        pass

    async def get_bvms_documents(self, question: str, __event_emitter__=None) -> str:
        """
        Get documents for answering questions about BVMS.
        """
        base_prompt = """
        You are an intelligent RAG AI agent for the BVMS (BBC Voyage Management System). For every questions, do the following steps:

        Step 1. Question Understanding: When a question is asked, first understand the query fully, breaking it down if necessary. Anaylize the main topics, entities and purpose of the question.
        Step 2. Then, Analyze carefully the below knowledge below, that you should base your answer on. Remeber, information is vast, so you need to account only for the sentences that satisfies the topics, entities and objectives of the questions above.

        -------
        Knowledge:
        {context}
        -------

        Step 3. Use the retrieved information above to generate a WELL-STRUCTURED, BULLET-POINT, CONCISE, ACCURATE response. Enhance your response with factual support when possible.
        Step 4. If the query goes beyond retrieved knowledge, just answer that you dont have information about this topics. Dont make up answers.
        Here is the question, Remember HUMAN ask questions always according the the knowledge base above.

        -------
        Here are the previous questions and answers:
        {histories}
        -------

        Now, answer with confidence.
        Question: {question}
        """

        base_url = "http://10.13.13.2:8000/api/retrieve"
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
            documents = data["documents"]

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
                    "data": { "content": f"Found {len(documents)} documents related to the question." },
                }
            )

            return base_prompt.format(
                context=documents,
                histories="",
                question=question,
            )

        except requests.RequestException as e:
            return f"Error fetching BVMS answer: {str(e)}"
