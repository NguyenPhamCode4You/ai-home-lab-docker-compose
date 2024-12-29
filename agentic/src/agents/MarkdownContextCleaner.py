from .Task import Task
from .models.Ollama import Ollama

class MarkdownContextCleaner(Task):
    def __init__(self):
        super().__init__(
            task_name="markdown-context-cleaner",
            llm_model=Ollama(),
            instruction_template="""
            You are an expert at re-formatting markdown content for further LLM processing.

            1. For tables:
            - Remove all table formatting
            - Describe each row in a single line, with column names and values separated by a colon.
            
            Table Example:
            ## Product Comparison
            | Product    | Price | Rating | Description                         |
            |------------|-------|--------|-------------------------------------|
            | Product A  | $10   | 4.5    | Affordable and high-quality.        |
            | Product B  | $20   | 4.8    | Premium quality with extra features.|
            | Product C  | $15   | 4.2    | Good value for the price.           |

            Output:
            ## Product Comparison
            Product: Product A: Price $10, Rating 4.5, Description: Affordable and high-quality.
            Product: Product B: Price $20, Rating 4.8, Description: Premium quality with extra features.
            Product: Product C: Price $15, Rating 4.2, Description: Good value for the price.

            2. For code blocks, api urls or json object: Keep them untouched, put all in 01 line.
            3. For sentences or lines with words counts less then 5: Combine them into a single line, reduce number of line breaks.
            Example:
            ---
            High Level Database Design Document
            15-Nov-2023
            Version: 1.0
            Document Control
            Document Information
            ---
            Output:
            High Level Database Design Document, 15-Nov-2023, Version: 1.0, Document Control, Document Information

            4. For repeated values: Keep only one instance of the value.
            5. For lists: Convert items to numbering format.

            Important:
            1. DO NOT include noise or irrelevant information, for example: ads, comments, page navigation, hyperlink, citations, references.
            2. Just return the written content, no extra explanation needed.
            3. Keep the markdown header as is, only re-format the content.

            Now, please re-format the following text: 
            {context}
            """
        )
