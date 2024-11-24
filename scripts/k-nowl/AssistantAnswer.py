import requests

with open("./prompts/BVMS-Rag-Prompt.txt", "r", encoding="utf-8") as file:
    base_prompt_default = file.read()

class AssistantAnswer:
    def __init__(self: str, url: str = 'http://localhost:11434/api/generate', model: str = 'gemma2:9b-instruct-q8_0'):
        self.url = url
        self.model = model
        self.embedder = None
        self.vector_store = None
        self.execution_strategy = None
        self.question_rewrite = None
        self.base_prompt = base_prompt_default
        self.match_count = 100
        self.max_promp_tokens = 6000

    def set_question_rewrite(self, question_rewrite):
        self.question_rewrite = question_rewrite
        return self

    def set_execution_strategy(self, execution_strategy):
        self.execution_strategy = execution_strategy
        return self
    
    def set_match_count(self, match_count: int):
        self.match_count = match_count
        return self

    def set_embedder(self, embedder):
        self.embedder = embedder
        return self

    def set_base_prompt(self, base_prompt: str):
        self.base_prompt = base_prompt
        return self
    
    def set_vector_store(self, vector_store):
        self.vector_store = vector_store
        return self
    
    def set_evaluator(self, evaluator):
        self.evaluator = evaluator
        return self
    
    def organize_documents(self, documents):
        # Extract titles from the document contents
        titles = [document["content"].split(":")[0] for document in documents]
        unique_titles = list(dict.fromkeys(titles))

        # Create sections for each unique title
        sections = []
        for title in unique_titles:
            counts = len([doc for doc in documents if doc["content"].split(":")[0] == title])
            
            # Collect document contents for the current title
            docs = [
                document["content"].replace(title, "", 1).replace(":", "", 1).strip()
                for document in documents
                if document["content"].split(":")[0] == title
            ]
            context = "\n".join(docs)

            # Add section with title, counts, and context
            sections.append({"title": title, "counts": counts, "context": context})

        # Order the sections by counts (descending order)
        # sections = sorted(sections, key=lambda x: x["counts"], reverse=True)
        return sections
    
    def reasoning(self, question: str) -> str:
        if self.question_rewrite is None:
            return self.run(question)
        
        questions = self.question_rewrite.run(question)
        if not questions:
            return self.run(question)
        
        questions = [question for question in questions.split("VNLPAGL\n") if len(question) > 0]
        context = ""
        for question in questions:
            print(f"Question: {question}")
            response = self.run(question)
            section = f"\n# Question: {question}\nResponse: {response}"
            context += section
            print(f"section: {section}")

        context = context[:self.max_promp_tokens]
        
        prompt = self.base_prompt.replace("{context}", context).replace("{question}", question)
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        
        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        
        # Clean and format the JSON response
        return self._clean_json_response(response.json())

    def run(self, question: str) -> str:
        question_embedding = self.embedder.run(question)
        documents = self.vector_store.query_documents(query_embedding=question_embedding, match_count=self.match_count)
        context = ""

        sections = self.organize_documents(documents)
        for section in sections:
            print(f"Title: {section["title"]}, Counts: {section["counts"]}")
            context += f"""\n# {section["title"]}:\n{section['context']}"""

        # context = "\n".join([document["content"] for document in documents if len(document["content"]) > 6])

        context = context[:self.max_promp_tokens]
        # print(f"Context: \nooooooooooooooooooooooooo\n{context}\nnooooooooooooooooooooooooo")

        prompt = self.base_prompt.replace("{context}", context).replace("{question}", question)
        # Send the request to the Ollama API
        response = requests.post(
            url=self.url,
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        
        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code}")
        
        # Clean and format the JSON response
        return self._clean_json_response(response.json())

    def _clean_json_response(self, response_data):
        # Assuming the API response has a 'response' field with the raw JSON text
        response = response_data.get("response", "")
        return response