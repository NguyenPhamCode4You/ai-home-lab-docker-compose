import os
from agents.RagKnowledgeBase import RagKnowledgeBase

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL    = "http://10.13.13.4:8000"
SUPABASE_TOKEN  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"

DOCU_TABLE_NAME = "n8n_documents_ebook"
DOCU_FUNCTION   = "match_n8n_documents_ebook_neo"

OLLAMA_URL      = "http://10.13.13.4:11434"
CODE_MODEL      = "qwen2.5-coder:14b-instruct-q6_K"
GENERAL_MODEL   = "gemma2:9b-instruct-q8_0"
EMBEDING_MODEL  = "nomic-embed-text:137m-v1.5-fp16"

knowledge_base = RagKnowledgeBase(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    embedder=CreateEmbedding(
        url=OLLAMA_URL,
        model=EMBEDING_MODEL
    ),
    vector_store=SupabaseVectorStore(
        url=SUPABASE_URL,
        token=SUPABASE_TOKEN,
        table_name=DOCU_TABLE_NAME,
        function_name=DOCU_FUNCTION
    )
)

folder_path = os.path.join(os.getcwd(), "codocu_results", "knowledge-base")
from jobs.DocumentLinesExtractor import DocumentLinesExtractor
from jobs.KeywordExtractor import KeywordExtractor
from jobs.SentenceSummarizer import SentenceSummarizer

import asyncio
asyncio.run(knowledge_base.learn(
    folder_path=folder_path,
    line_extractor=DocumentLinesExtractor(
        url=OLLAMA_URL,
        model=GENERAL_MODEL
    ),
    keyword_extractor=KeywordExtractor(
        url=OLLAMA_URL,
        model=GENERAL_MODEL
    ),
    sentence_summarizer=SentenceSummarizer(
        url=OLLAMA_URL,
        model=GENERAL_MODEL
    )
))


# knowledge_base.stream("What is the purpose of this knowledge base?")
