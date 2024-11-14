import requests

ollama_instruct_url = "http://localhost:11434/api/generate"
ollama_embeding_url = "http://localhost:11434/api/embed"
ollama_instruct_model = "codegemma:7b-instruct-v1.1-q8_0"
ollama_embeding_model = "nomic-embed-text:137m-v1.5-fp16"

class QuestionAsker:
    def __init__(self, message: str):
        self.message = str(message)
        self.base_prompt = """
        You are an expert anylyzing markdown documents and ask at least 03 questions about the content. Follow the guidelines below:
        
        1. Provide questions that lead to the main idea or purpose of the paragraph or sentences.
        2. Use \n to separate between questions.
        4. Always try to put keywords of the content in the question.

        Here is an example:
        Example -----------------------------------------------------
        # Introduction
        Markdown is a lightweight markup language with plain-text formatting syntax. Markdown supports headers, lists, emphasis, links, images, and more. Syntax is designed for readability.
        End of example.----------------------------------------------

        Output:
        \n What is Markdown?
        \n What does Markdown support?
        \n Are lists, emphasis, links, and images supported by Markdown?

        5. For table, try to put lots of contents/keywords in each questions. Generate questions based on the content/items of the table.
        6. If questions length become > 500 characters, use "VNLPAGL" to separate between questions.
        Example -----------------------------------------------------
        ## Product Comparison
        | Product    | Price | Rating | Description                         |
        |------------|-------|--------|-------------------------------------|
        | Product A  | $10   | 4.5    | Affordable and high-quality.        |
        | Product B  | $20   | 4.8    | Premium quality with extra features.|
        | Product C  | $15   | 4.2    | Good value for the price.           |
        End of example.----------------------------------------------

        Output:
        \n What are the products compared based on?; What are the prices, ratings, and descriptions of the products?
        \n What is the description of Product A?; What is the price of Product B? What is the rating of Product C?
        \n What is the best value product?; What is the most expensive product?
        VNLPAGL\n What product has the highest rating? What product has the lowest price?
        \n What are the features of Product B?; What are the features of Product C?

        6. For Code block, try to put the function name or API Url in the question.
        7. Try to infer the main idea or purpose of the code block and generate questions based on that.
        8. Generate at least 05 questions for each code block.

        Example -----------------------------------------------------
        api_url = "https://api.example.com/data"
        def process_data(data):
            # This function processes data by cleaning and transforming it
            cleaned_data = [item.strip().lower() for item in data if isinstance(item, str)]
            transformed_data = [int(item) for item in cleaned_data if item.isdigit()]
            return transformed_data
        ```
        End of example.----------------------------------------------
        
        Output:
        \n What does the process_data function do?; 
        \n How does the process_data function clean and transform data?
        \n What is the API URL of process_data?; 
        \n What API need to be called to process data?
        \n What is the purpose of the process_data function?;

        9. If the text is just a useless text, return only one VNLPAGL.
        Example -----------------------------------------------------
        <!-- image -->## Integration Support
        | jr-f7 | attribute s|
        End of example.----------------------------------------------

        Output:
        VNLPAGL

        Again, Important Notes:
        - Always use "\n" to separate questions, use "VNLPAGL" to separate if questions length become > 500 characters.
        - For table, try to put lots of contents/keywords in the questions. Ask questions based on the content/items of the table.
        - For Code block, try to put the function name or API Url in the question. Generate at least 05 questions for each code block.
        
        Now, please extract the questions from the following text:  
        """

    def run(self):
        # Send the request to the Ollama API
        response = requests.post(
            ollama_instruct_url,
            json={"model": ollama_instruct_model, "prompt": self.base_prompt + self.message, "stream": False}
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