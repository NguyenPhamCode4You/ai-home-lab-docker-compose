import json
import os
from agents.RagKnowledgeBase import RagKnowledgeBase
from agents.CodeDocumentor import CodeDocumentor

from tools.CreateEmbedding import CreateEmbedding
from tools.SupabaseVectorStore import SupabaseVectorStore
from jobs.RelevantDocumentExtractor import RelevantDocumentExtractor

SUPABASE_URL    = "http://10.13.13.4:8000"
SUPABASE_TOKEN  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_ebook"
FUNCTION   = "match_n8n_documents_ebook_neo"

OLLAMA_URL      = "http://10.13.13.4:11434"
CODE_MODEL      = "qwen2.5-coder:14b-instruct-q6_K"
GENERAL_MODEL   = "gemma2:9b-instruct-q8_0"
EMBEDING_MODEL  = "nomic-embed-text:137m-v1.5-fp16"

with open(os.path.join(os.path.dirname(__file__), "prompts/BVMS-Prompt.txt"), "r", encoding="utf-8") as file:
    bvms_prompt = file.read()

with open(os.path.join(os.path.dirname(__file__), "prompts/Document-Prompt.txt"), "r", encoding="utf-8") as file:
    documentor_prompt = file.read()

embedder = CreateEmbedding(
    url=OLLAMA_URL,
    model=EMBEDING_MODEL
)
vector_store = SupabaseVectorStore(
    url=SUPABASE_URL,
    token=SUPABASE_TOKEN,
    table_name=TABLE_NAME,
    function_name=FUNCTION
)
knowledge_base = RagKnowledgeBase(
    url=OLLAMA_URL,
    model=GENERAL_MODEL,
    embedder=embedder,
    vector_store=vector_store,
    base_prompt=bvms_prompt
)
code_documentor = CodeDocumentor(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    embedder=embedder,
    vector_store=vector_store,
    base_prompt=documentor_prompt,
    document_extractor=RelevantDocumentExtractor(
        url=OLLAMA_URL,
        model=GENERAL_MODEL
    )
)

code_folder_path = os.path.join(os.getcwd())
code_document_folder_path = os.path.join(os.getcwd(), "codocu_results", "code-documentation")

original_folder_path = os.path.join(os.getcwd(), "bvms-knowledge-base")
formatted_folder_path = os.path.join(os.getcwd(), "codocu_results", "bvms-knowledge-base")

from jobs.DocumentLinesExtractor import DocumentLinesExtractor
from jobs.KeywordExtractor import KeywordExtractor
from jobs.SentenceSummarizer import SentenceSummarizer
from jobs.MarkdownProcessor import MarkdownProcessor
from jobs.CodeDocumentWriter import CodeDocumentWriter
from jobs.CodeSummarizer import CodeSummarizer

async def example1():
    # await code_documentor.analyze(
    #     original_folder_path=code_folder_path,
    #     result_folder_path=code_document_folder_path,
    #     allowed_file_extensions=[".py"],
    #     ignored_file_pattern=['codocu_results', 'venv', '__pycache__', 'prompts', 'cpython'],
    #     document_writter=CodeDocumentWriter(
    #         url=OLLAMA_URL,
    #         model=CODE_MODEL,
    #     ),
    #     summarizer=CodeSummarizer(
    #         url=OLLAMA_URL,
    #         model=GENERAL_MODEL
    #     ),
    #     keyword_extractor=KeywordExtractor(
    #         url=OLLAMA_URL,
    #         model=GENERAL_MODEL
    #     ),
    # )
    async for agent_chunk in code_documentor.stream("Can you explain how the agent named AssistantOrchestra works? Can you also provide code snippets of this agent?", []):
        if (len(agent_chunk) > 1000):
            continue
        agent_response = json.loads(agent_chunk)["response"]
        print(agent_response, end="", flush=True)  # Real-time console output

async def example2():
    await knowledge_base.formatting(
        original_folder_path=original_folder_path,
        formatted_folder_path=formatted_folder_path,
        markdown_processor=MarkdownProcessor(
            url=OLLAMA_URL,
            model=GENERAL_MODEL
        ),
        chunk_size=600
    )
    await knowledge_base.learn(
        folder_path=formatted_folder_path,
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
    )
    async for agent_chunk in knowledge_base.stream("Can you tell me how BVMS calculate EU ETS?", []):
        if (len(agent_chunk) > 1000):
            continue
        agent_response = json.loads(agent_chunk)["response"]
        print(agent_response, end="", flush=True)  # Real-time console output


import asyncio
asyncio.run(example1())
