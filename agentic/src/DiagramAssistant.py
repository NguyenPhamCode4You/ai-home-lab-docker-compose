from .agents.MermaidCodeWriter import MermaidCodeWriter

class DiagramAssistant():
    def __init__(self,
            llm_mermaid_code_writter: MermaidCodeWriter = None,
        ):
        self.mermaid_code_writer = llm_mermaid_code_writter or MermaidCodeWriter()

    async def stream(self, question: str = None, conversation_history: list = None):
        async for code_chunk in self.mermaid_code_writer.stream(question=question):
            yield code_chunk