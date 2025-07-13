from .Task import Task
from .models.Ollama import Ollama

class CodeReviewer(Task):
    def __init__(self, **kwargs):
        kwargs["task_name"] = kwargs.get("task_name", "code-reviewer")
        kwargs["llm_model"] = kwargs.get("llm_model", Ollama())
        kwargs["max_context_tokens"] = kwargs.get("max_context_tokens", 32000)
        kwargs["instruction_template"] = kwargs.get("instruction_template", """
            ## You are an expert code reviewer that is provided with this code changes:
            {context}

            ## Your task is to review the code changes base the the following guidelines:            
            # Code Review Guidelines
            ### 1. Code & Structure Quality: [Rate 1-10]
            Rate overall code quality, readability, maintainability, error handling, and organization.

            ### 2. Performance Impact: [Yes/No]
            Identify if changes cause performance issues or critical impacts (slow queries, inefficient algorithms, bad practices).

            ### 3. Security Concerns: [List any or "None"]
            Note potential vulnerabilities, missing input validation, or insecure practices.

            ### 4. Good Points (2 compliments)
            - [Highlight what the developer did well]
            - [Another positive aspect]

            ### 5. Suggestions (2 improvements)
            - [Specific actionable improvement]
            - [Another enhancement suggestion]

            ### 6. Merge Decision
            - **APPROVED**: Ready to merge
            - **NEEDS_WORK**: Requires changes
            - **BLOCKED**: Critical issues found

            Keep feedback constructive and actionable.
            Also, please answer the addtional question from the user below.
            ## User Additional request: {question}
        """)
        super().__init__(**kwargs)