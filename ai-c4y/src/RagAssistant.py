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
            document_ranking_patch_percent: float = 5.0
        ):
        
        self.query_function_name = query_function_name
        self.vector_store = llm_vector_store or SupabaseVectorStore(embedding=Embedding())
        self.rag_answer = llm_rag_answer or GeneralRagAnswer()
        self.document_ranking = llm_document_ranking or None
        self.context_enricher = llm_context_enricher or None
        self.final_summarizer = llm_final_summarizer or None
        self.document_match_count = document_match_count
        self.document_ranking_patch_percent = document_ranking_patch_percent

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        knowledge_context = self.vector_store.get_documents_string(
            question=question,
            function_name=self.query_function_name,
            match_count=self.document_match_count)
        print(f"Knowledge context: {knowledge_context}")
        if self.document_ranking is not None:
            max_ranking_context_tokens = self.rag_answer.max_context_tokens * 2.5
            yield "<think>📌 Retrieving documents: "

            # Collect documents up to the token limit first
            docs_to_rank = []
            documents_context_length = 0
            for header, content in split_markdown_header_and_content(knowledge_context):
                document = f"# {header}\n\n{content}"
                docs_to_rank.append(document)
                documents_context_length += len(document)
                if documents_context_length > max_ranking_context_tokens:
                    break

            # Rank documents in parallel batches of 10% at a time
            async def rank_doc(idx, doc):
                raw = await self.document_ranking.run(context=doc, question=question, conversation_history=conversation_history)
                try:
                    import re as _re
                    match = _re.search(r'\d+(\.\d+)?', str(raw))
                    score = float(match.group()) if match else 0.0
                except Exception:
                    score = 0.0
                return idx, score

            total = len(docs_to_rank)
            batch_size = max(1, int(total * self.document_ranking_patch_percent / 100))
            scores = [0.0] * total
            completed = 0

            for batch_start in range(0, total, batch_size):
                batch = [(i, docs_to_rank[i]) for i in range(batch_start, min(batch_start + batch_size, total))]
                batch_results = await asyncio.gather(*[rank_doc(i, doc) for i, doc in batch])
                for idx, score in batch_results:
                    scores[idx] = score
                completed += len(batch)
                percentage = int(completed / total * 100)
                yield f" ➜ {percentage}%"

            documents = list(zip(docs_to_rank, scores))
            documents.sort(key=lambda x: x[1], reverse=True)

            # Keep only top documents that fit within the answer LLM's context limit
            top_docs = []
            top_docs_length = 0
            for doc, _ in documents:
                if top_docs_length + len(doc) > self.rag_answer.max_context_tokens:
                    break
                top_docs.append(doc)
                top_docs_length += len(doc)

            knowledge_context = "\n\n".join(top_docs)
            yield f"\n✅ Using top {len(top_docs)}/{total} documents ({top_docs_length} chars)\n</think>\n\n"

        # ---- Single-shot answer ----
        iterations_response = ""
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