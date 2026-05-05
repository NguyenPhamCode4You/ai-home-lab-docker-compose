import asyncio
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
            yield f"📌 Retrieving documents: "

            # Collect documents up to the token limit first
            docs_to_rank = []
            documents_context_length = 0
            for header, content in split_markdown_header_and_content(knowledge_context):
                document = f"# {header}\n\n{content}"
                docs_to_rank.append(document)
                documents_context_length += len(document)
                if documents_context_length > max_ranking_context_tokens:
                    break

            # Rank all documents in parallel
            async def rank_doc(idx, doc):
                raw = await self.document_ranking.run(context=doc, question=question, conversation_history=conversation_history)
                try:
                    import re as _re
                    match = _re.search(r'\d+(\.\d+)?', str(raw))
                    score = float(match.group()) if match else 0.0
                except Exception:
                    score = 0.0
                return idx, score

            tasks = [rank_doc(i, doc) for i, doc in enumerate(docs_to_rank)]
            scores = [0.0] * len(docs_to_rank)
            completed = 0
            last_emitted = -1
            for coro in asyncio.as_completed(tasks):
                idx, score = await coro
                scores[idx] = score
                completed += 1
                percentage = int(completed / len(docs_to_rank) * 100)
                milestone = (percentage // 10) * 10
                if milestone > last_emitted:
                    yield f" ➜ {str(milestone)}%"
                    last_emitted = milestone

            documents = list(zip(docs_to_rank, scores))
            documents.sort(key=lambda x: x[1], reverse=True)
            knowledge_context = "\n\n".join([doc[0] for doc in documents])

        # ---- Single-shot answer ----
        iterations_response = ""
        yield "\n\n"
        async for response_chunk in self.rag_answer.stream(
            context=knowledge_context,
            question=question,
            conversation_history=conversation_history,
        ):
            yield response_chunk
            iterations_response += response_chunk

        # ---- Optional enricher ----
        if self.context_enricher:
            enrichment_header = f"\n\n### 🌟 Let's enrich the context with more information...\n\n"
            yield enrichment_header
            iterations_response += enrichment_header
            async for enricher_chunk in self.context_enricher.stream(question=question):
                yield enricher_chunk
                iterations_response += enricher_chunk

        # ---- Optional final summarizer ----
        if self.final_summarizer:
            summarizer_header = f"\n\n### 🎯 Lets have one final revise on the question ...\n\n"
            yield summarizer_header
            iterations_response += summarizer_header
            async for summarizer_chunk in self.final_summarizer.stream(context=iterations_response, question=question):
                yield summarizer_chunk