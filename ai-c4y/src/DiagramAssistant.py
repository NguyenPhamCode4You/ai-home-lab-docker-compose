from .agents.MermaidCodeWriter import MermaidCodeWriter

class DiagramAssistant():
    def __init__(self,
            llm_mermaid_code_writter: MermaidCodeWriter = None,
        ):
        self.mermaid_code_writer = llm_mermaid_code_writter or MermaidCodeWriter()

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        async for code_chunk in self.mermaid_code_writer.stream(question=question, context=context, conversation_history=conversation_history):
            yield code_chunk