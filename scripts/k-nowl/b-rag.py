from CreateEmbedding import CreateEmbedding
from SupabaseVectorStore import SupabaseVectorStore
from AssistantAnswer import AssistantAnswer
from DocumentEvaluator import DocumentEvaluator

SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_bbc_bvms"
vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)
embedder = CreateEmbedding()
evaluator = DocumentEvaluator()

assistant = AssistantAnswer()
assistant.set_embedder(embedder).set_vector_store(vector_store).set_evaluator(evaluator)

# print(assistant.run("What is this knowledge base about?"))

print(assistant.run("""If I have a cargo freight of 250,000 USD, I need to hire BBC amber to deliver the cargo. The voyage is 10 days, the bunker cost for each ton is 720. Is this voyage a loss or a profit? Given the hire rate of BBC Amber is 16,000 USD per day, and BBC Amber is traveling at 17 knots. 
Calculate the total bunker cost by the consumption rate per day x days. Other expenses are set = 0
If It is a loss, how much? Then if I want to have 50,000 as profit, how much freight I need to charge the customer for the cargo?"""))
