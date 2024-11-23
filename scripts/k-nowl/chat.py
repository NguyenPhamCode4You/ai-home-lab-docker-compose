from CreateEmbedding import CreateEmbedding
from SupabaseVectorStore import SupabaseVectorStore
from AssistantAnswer import AssistantAnswer
from DocumentEvaluator import DocumentEvaluator

SUPABASE_URL = "http://10.13.13.4:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_bbc_bvms"
vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)

embedder = CreateEmbedding(url='http://10.13.13.4:11434/api/embed')
evaluator = DocumentEvaluator(url='http://10.13.13.4:11434/api/generate')

assistant = AssistantAnswer(url='http://10.13.13.4:11434/api/generate')
assistant.set_embedder(embedder)
assistant.set_vector_store(vector_store)
assistant.set_evaluator(evaluator)
assistant.set_match_count(32)

# Streamlit App
import streamlit as st

# Initialize chat messages storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize user input tracker
if "temp_input" not in st.session_state:
    st.session_state.temp_input = ""

def submit_message():
    """Handles the submission of a user message."""
    st.session_state.messages = []
    user_input = st.session_state.temp_input
    if user_input:
        # Append user question
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get response from the assistant (mock response for illustration)
        response = assistant.run(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Clear temporary input after processing
        st.session_state.temp_input = ""

        # Clear the previous messages

# User input form
st.text_input("Ask a question:", key="temp_input", on_change=submit_message)

# Display chat history
def render_message(role, content):
    """
    Render a message, splitting text and code sections.
    - role: "user" or "assistant"
    - content: The message content
    """
    if role == "user":
        st.markdown(f"🌞**You:** {content}")
    else:
        # Parse the message to separate code blocks (```...```) and text
        parts = content.split("```")
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Text sections
                if part.strip():
                    st.markdown(f"🤖**Assistant:** {part.strip()}")
            else:  # Code sections
                st.code(part.strip())  # Display the code section

# Display chat history
for message in st.session_state.messages:
    render_message(message["role"], message["content"])


