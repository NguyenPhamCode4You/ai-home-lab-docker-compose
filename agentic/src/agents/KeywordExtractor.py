from .Task import Task
from .models.Ollama import Ollama

class KeywordExtractor(Task):
    def __init__(self, count: int = 10):
        super().__init__(
            task_name="keyword-extractor",
            llm_model=Ollama(),
            instruction_template=f"""
            Your task is to extract important keywords from the below context.
            {"{context}"}
            ------
            Considerations:
            1. Keywords should be the main entities that text is about, or refering to
            2. Should not have more than {count} keywords per text, ordered by importance
            3. Sometime keywords can be verbs, adjectives, or adverbs, put them at the beginning

            Example:
            How to Calculate P&L Summaries (v1.0): I. Calculation Rules & Factors: Item: Voyage Revenues, Sub-Item: Freight, Calculation Rule & Factor: Freight Rate (L) + Freight Rate (F) x Quantity.

            Output:
            Calculate, Summarize, P&L Summaries, Calculation Rules & Factors, Voyage Revenues, Freight, Calculation Rule, Factor, Freight Rate, Quantity

            3. For code, use the name of functions, classes, or variables as keywords.
            4. For documents, use the title, author, or main subject as keywords.
            5. For emails, use the subject, sender, or main topic as keywords.
            6. For URLs, use the domain, path, or main topic as keywords.
            7. For json objects, xml, or html, use the main keys, tags, or attributes as keywords.

            Important:
            - Return only the keywords, separated by commas.
            - Do not include the base prompt in the response.
            - Do not include the input text in the response.
            - Do not include any additional information.
            - No more than {count} keywords per text.

            Now, please extract the keywords from the following text: 
            """
)