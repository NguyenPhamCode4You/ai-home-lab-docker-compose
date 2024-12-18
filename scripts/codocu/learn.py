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

# OLLAMA_URL      = "http://10.13.13.5:11434"
# CODE_MODEL      = "qwen2.5-coder:32b"
# GENERAL_MODEL   = "gemma2:27b-instruct-q5_1"

EMBEDING_MODEL  = "nomic-embed-text:137m-v1.5-fp16"

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
    base_prompt="""
    You are an intelligent RAG AI agent for assisting users with their questions.
    Here is the user question: {question}

    Before answering, first, analyze carefully the knowledge below to base your answer on. Consider only the relevant information to the question besing asked.
    {context}

    Then, generate a WELL-STRUCTURED, BULLET-POINT, CONCISE, ACCURATE but DETAILED answer to the question!
    Important:
    - Always base your answer on the retrieved knowledge.
    - You may enhance your response with factual support when possible.
    - If the query goes beyond retrieved knowledge, just answer that you dont have information about this topics. Dont make up information.

    Here are the previous questions and answers that you can use to base your answer on:
    {histories}

    Now, answer with confidence.
    """
)
code_documentor = CodeDocumentor(
    url=OLLAMA_URL,
    model=CODE_MODEL,
    embedder=embedder,
    vector_store=vector_store,
    max_context_tokens_length=8000,
    document_extractor=RelevantDocumentExtractor(
        url=OLLAMA_URL,
        model=GENERAL_MODEL
    ),
    base_prompt="""
    You are an experienced software developer and your task is reading a code document to answer user questions.
    Here is the code document you need to read:
    {context}
    User Question: {question}
    Try your very best to assist the user with their question.
    """
    
)

code_folder_path = os.path.join(os.getcwd())
code_folder_path = "C:\\Users\\niche\\gitlab\\bbc-bvms-net-back-end-modular"
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
    await code_documentor.analyze(
        original_folder_path=code_folder_path,
        result_folder_path=code_document_folder_path,
        # allowed_file_extensions=[".py"],
        # ignored_file_pattern=['codocu_results', 'venv', '__pycache__', 'prompts', 'cpython'],
        allowed_file_extensions=[".cs"],
        ignored_file_pattern=['Test', 'test', 'bin', 'obj', 'Properties', 'packages', 'csproj', 'controller', 'program', 'startup', 'dto', 'Migrations', 'snapshot', 'mapping', 'documents', 'SednaIntegrationService', 'setup'],
        document_writter=CodeDocumentWriter(
            url=OLLAMA_URL,
            model=CODE_MODEL,
        ),
        summarizer=CodeSummarizer(
            url=OLLAMA_URL,
            model=GENERAL_MODEL
        ),
        keyword_extractor=KeywordExtractor(
            url=OLLAMA_URL,
            model=GENERAL_MODEL
        ),
    )
    # async for agent_chunk in code_documentor.stream("Read through all aspect of AssistantOrchestra carefully, then basing on this current code, suggest for codes to add a reflection layer to let the agent revise on their final answer. If the final answer is not good, it need to correct itself and answer the question again", []):
    #     if (len(agent_chunk) > 1000):
    #         continue
    #     agent_response = json.loads(agent_chunk)["response"]
    #     print(agent_response, end="", flush=True)  # Real-time console output

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
