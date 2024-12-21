from Task import Task
from models.Ollama import Ollama

class MarkdownContextCleaner(Task):
    def __init__(self):
        super().__init__(
            task_name="markdown-context-cleaner",
            llm_model=Ollama(),
            instruction_template="""
            You are an expert at re-formatting markdown text for further processing.

            1. For tables:
            - Remove table formating
            - Describe each row in a single line.
            Example:
            ## Product Comparison
            | Product    | Price | Rating | Description                         |
            |------------|-------|--------|-------------------------------------|
            | Product A  | $10   | 4.5    | Affordable and high-quality.        |
            | Product B  | $20   | 4.8    | Premium quality with extra features.|
            | Product C  | $15   | 4.2    | Good value for the price.           |

            Output:
            ## Product Comparison
            Product A: Price $10, Rating 4.5, Affordable and high-quality.
            Product B: Price $20, Rating 4.8, Premium quality with extra features.
            Product C: Price $15, Rating 4.2, Good value for the price.

            3. For code blocks, api urls or json object: Keep them untouched, put all in 01 line.
            4. For sentences or lines with words counts less then 5:
            - Combine them into a single line, reduce number of line breaks.
            - Except for markdown headers, keep them as is.
            Example:
            ---
            # VOYAGE MANAGEMENT SYSTEM

            High Level Database Design Document

            15-Nov-2023

            Version: 1.0

            Document Control

            Document Information
            ---

            Output:
            # VOYAGE MANAGEMENT SYSTEM 
            High Level Database Design Document, 15-Nov-2023, Version: 1.0, Document Control, Document Information

            5. For tables with repeated values
            - Remove the repeated values, make the unique values comma separated.
            - Remove numbers, special characters and formatting issues.

            Example:
            ## Voyage Revenues
            | Voyage Revenues      | Voyage Revenues      | Voyage Revenues      | 1.345.150      |
            |----------------------|----------------------|----------------------|----------------|
            | Freight              | Freight 12              | Freight              | 1.200.000      |
            | Misc. Revenue        | Misc. Revenue        | Misc. Revenueqq        | 150            |
            | Demurrage            | Demurrage sfe            | Demurrageddw            | 26.000         |
            | Despatch             | Despatch             | Despatch             | 21.500         |

            Output:
            ## Voyage Revenues
            Voyage Revenues: Freight, Misc. Revenue, Demurrage, Despatch

            6. For lists:
            - Convert items to numbering format.

            The rest of the text should be kept as is.
            Important:
            - Return only the formatted text.
            - Do not include the base prompt in the response.
            - Do not include the input text in the response.
            - Do not include any additional information.

            Now, please re-format the following text: 
            {context}
            """
        )
