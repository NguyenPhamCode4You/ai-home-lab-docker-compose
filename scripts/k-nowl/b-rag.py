from CreateEmbedding import CreateEmbedding
from SupabaseVectorStore import SupabaseVectorStore
from AssistantAnswer import AssistantAnswer

SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_bbc_bvms"
vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)
embedder = CreateEmbedding()

assistant = AssistantAnswer()
assistant.set_embedder(embedder).set_vector_store(vector_store)

assistant.run("What is this knowledge base about?")
