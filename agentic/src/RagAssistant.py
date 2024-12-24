from .agents.tools import SupabaseVectorStore
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding
from .agents.Task import Task
from .agents.GeneralRagAnswer import GeneralRagAnswer

class RagAssistant():
    def __init__(self, 
            query_function_name: str, 
            llm_vector_store: SupabaseVectorStore = None, 
            llm_rag_answer: Task = None,
            llm_context_enricher: Task = None,
            llm_final_summarizer: Task = None,
            document_match_count: int = 200,
            max_context_tokens: int = 6000):
        
        self.query_function_name = query_function_name
        self.vector_store = llm_vector_store or SupabaseVectorStore(embedding=Embedding())
        self.rag_answer = llm_rag_answer or GeneralRagAnswer()
        self.context_enricher = llm_context_enricher or None
        self.final_summarizer = llm_final_summarizer or None
        self.document_match_count = document_match_count
        self.max_context_tokens = max_context_tokens

    async def stream(self, question: str = None, conversation_history: list = None):
        context = self.vector_store.get_documents_string(
            question=question,
            function_name=self.query_function_name,
            match_count=self.document_match_count)
        context = context[:self.max_context_tokens]
        iterations_response = ""
        async for response_chunk in self.rag_answer.stream(context, question, conversation_history):
            yield response_chunk
            iterations_response += response_chunk
        if self.context_enricher:
            enrichment_header = f"\n\n### 🌟 Let's enrich the context with more information...\n\n"
            yield enrichment_header
            iterations_response += enrichment_header
            async for enricher_chunk in self.context_enricher.stream(question=question):
                yield enricher_chunk
                iterations_response += enricher_chunk
        if self.final_summarizer:
            summarizer_header = f"\n\n### 🎯 Lets have one final revise on the question ...\n\n"
            yield summarizer_header
            iterations_response += summarizer_header
            async for summarizer_chunk in self.final_summarizer.stream(context=iterations_response, question=question):
                yield summarizer_chunk
        