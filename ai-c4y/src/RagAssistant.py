from .agents.tools import SupabaseVectorStore
from .agents.tools.SupabaseVectorStore import SupabaseVectorStore
from .agents.tools.Embedding import Embedding
from .agents.Task import Task
from .agents.GeneralRagAnswer import GeneralRagAnswer
from .agents.DocumentRanking import DocumentRanking
from .FileHanlder import split_markdown_header_and_content

class RagAssistant():
    def __init__(self, 
            query_function_name: str, 
            llm_vector_store: SupabaseVectorStore = None, 
            llm_rag_answer: Task = None,
            llm_document_ranking: Task = None,
            llm_context_enricher: Task = None,
            llm_final_summarizer: Task = None,
            document_match_count: int = 200,
        ):
        
        self.query_function_name = query_function_name
        self.vector_store = llm_vector_store or SupabaseVectorStore(embedding=Embedding())
        self.rag_answer = llm_rag_answer or GeneralRagAnswer()
        self.document_ranking = llm_document_ranking or None
        self.context_enricher = llm_context_enricher or None
        self.final_summarizer = llm_final_summarizer or None
        self.document_match_count = document_match_count

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        knowledge_context = self.vector_store.get_documents_string(
            question=question,
            function_name=self.query_function_name,
            match_count=self.document_match_count)
        print(f"Knowledge context: {knowledge_context}")
        if self.document_ranking is not None:
            max_ranking_context_tokens = self.rag_answer.max_context_tokens * 2.5
            yield f"📌 Re-ranking documents: "
            documents = []
            documents_context_length = 0
            for header, content in split_markdown_header_and_content(knowledge_context):
                document = f"# {header}\n\n{content}"
                score = await self.document_ranking.run(context=document, question=question, conversation_history=conversation_history)
                score = float(score)
                documents.append((document, score))
                documents_context_length += len(document)
                percentage = int(documents_context_length / max_ranking_context_tokens * 100)
                if percentage > 100:
                    percentage = 100
                yield f" ➜ {str(percentage)}%"
                if documents_context_length > max_ranking_context_tokens:
                    break
            documents.sort(key=lambda x: x[1], reverse=True)
            knowledge_context = "\n\n".join([doc[0] for doc in documents])
        iterations_response = ""
        yield "\n\n"
        async for response_chunk in self.rag_answer.stream(context=knowledge_context, question=question, conversation_history=conversation_history):
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
        