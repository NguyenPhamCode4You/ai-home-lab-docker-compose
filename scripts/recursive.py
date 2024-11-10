from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.prompts import PromptTemplate
import pandas as pd

# Load your large document
document_path = './[BBC_Chartering] Infrastructure Design Document_V1.0 (1).docx.txt'
loader = TextLoader(document_path)
documents = loader.load()

# remove empty strings
documents = [doc for doc in documents if doc.page_content]

# remove empty lines
documents = [doc for doc in documents if doc.page_content.strip()]

# Use RecursiveCharacterTextSplitter for agentic chunking
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunked_texts = text_splitter.split_documents(documents)

# Convert chunked_texts to a DataFrame
chunk_data = [{"chunk_index": i, "chunk_text": chunk.page_content} for i, chunk in enumerate(chunked_texts)]
df_chunks = pd.DataFrame(chunk_data)

csv_path = './chunked/[BBC_Chartering] Infrastructure Design Document_V1.0 (1).docx.csv'
df_chunks.to_csv(csv_path, index=False)

json_path = './chunked/[BBC_Chartering] Infrastructure Design Document_V1.0 (1).docx.json'
df_chunks.to_json(json_path, orient="records", lines=True)

# Initialize Ollama embeddings
embedding_model = OllamaEmbeddings(model="llama3.2:latest")
faiss_index = FAISS.from_documents(chunked_texts, embedding_model)

# Set up retrieval with FAISS
retriever = faiss_index.as_retriever()

# Initialize Ollama as LLM for answering questions
llm = Ollama(model="llama3.2:latest")
qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, chain_type="stuff")

# Define a prompt template for custom responses
prompt_template = PromptTemplate(input_variables=["question"], template="Answer the following question: {question}")

# Set up tools for the agent
tools = [
    Tool(
        name="Answer Questions",
        func=qa_chain.run,
        description="Answers questions based on the provided text chunks."
    )
]

# Initialize agent with tools and Ollama LLM
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    prompt_template=prompt_template
)

# Example query with the expected key 'input' instead of 'question'
question = "What is the main topic of the document?"
response = agent({"input": question})  # Changed 'question' to 'input'
print(response['output'])

# Notify the user of the saved Excel file path
print(f"The chunked texts have been saved to {excel_path}")
