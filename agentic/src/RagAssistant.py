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
            document_match_count: int = 200,
            max_context_tokens: int = 9000,
            context_chunk_size: int = 5600,
            max_histories_tokens: int = 50,
            allow_reflection: bool = False):
        
        self.query_function_name = query_function_name
        self.vector_store = llm_vector_store or SupabaseVectorStore(embedding=Embedding())
        self.rag_answer = llm_rag_answer or GeneralRagAnswer(
            context_chunk_size=context_chunk_size, 
            max_histories_tokens=max_histories_tokens, 
            allow_reflection=allow_reflection)
        self.document_match_count = document_match_count
        self.max_context_tokens = max_context_tokens
        self.context_chunk_size = context_chunk_size
        self.max_histories_tokens = max_histories_tokens

    async def stream(self, question: str = None, conversation_history: list = None):
        context = self.vector_store.get_documents_string(
            question=question,
            function_name=self.query_function_name,
            match_count=self.document_match_count)
        context = context[:self.max_context_tokens]
        async for response_chunk in self.rag_answer.stream(context, question, conversation_history):
            yield response_chunk