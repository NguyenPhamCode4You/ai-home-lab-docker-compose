import streamlit as st
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

# Streamlit App
st.title("Streamlit Chat with LLM")

# Chat messages storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
with st.form("chat_form"):
    user_input = st.text_input("Ask a question:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append user question
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from the assistant
    response = assistant.run(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Assistant:** {message['content']}")
