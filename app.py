import os
import streamlit as st
from sentence_transformers import SentenceTransformer
from faiss import IndexFlatL2
import numpy as np
from pdfminer.high_level import extract_text
from docx import Document
import ollama  # For interacting with Ollama's DeepSeek LLM

# Disable problematic components
os.environ["STREAMLIT_WATCHDOG"] = "false"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Custom styling
st.markdown("""
<style>
    .main {background-color: #1a1a1a; color: #ffffff;}
    .sidebar .sidebar-content {background-color: #2d2d2d;}
    .stTextInput textarea {color: #ffffff !important;}
</style>
""", unsafe_allow_html=True)

st.title("📄 Document Chatbot with RAG")
st.caption("🤖 Upload documents and chat with them!")

# Initialize components
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
index = None
documents = []

# Initialize session state for chat history and document processing
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = {}

# File processing functions
def process_pdf(file_bytes):
    with open("temp.pdf", "wb") as f:
        f.write(file_bytes)
    text = extract_text("temp.pdf")
    os.remove("temp.pdf")
    return text

def process_docx(file_bytes):
    with open("temp.docx", "wb") as f:
        f.write(file_bytes)
    doc = Document("temp.docx")
    text = "\n".join([p.text for p in doc.paragraphs])
    os.remove("temp.docx")
    return text

def process_txt(file_bytes):
    encodings = ["utf-8", "ISO-8859-1", "windows-1252"]
    for encoding in encodings:
        try:
            return file_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None

# Document processing
uploaded_files = st.file_uploader("Upload documents", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    all_embeddings = []
    documents = []
    
    for file in uploaded_files:
        if file.name in st.session_state.processed_files:
            st.success(f"Using cached data for {file.name}")
            text = st.session_state.processed_files[file.name]
        else:
            content = file.read()
            try:
                if file.name.endswith(".pdf"):
                    text = process_pdf(content)
                elif file.name.endswith(".docx"):
                    text = process_docx(content)
                elif file.name.endswith(".txt"):
                    text = process_txt(content)
                
                if text:
                    # Cache the processed text
                    st.session_state.processed_files[file.name] = text
                    st.success(f"Processed {file.name}")
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                continue
        
        if text:
            # Split and store documents
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            embeddings = model.encode(chunks)
            all_embeddings.extend(embeddings)
            documents.extend(chunks)
    
    if len(all_embeddings) > 0:
        # Create FAISS index (only once)
        if "faiss_index" not in st.session_state:
            dimension = all_embeddings[0].shape[0]
            index = IndexFlatL2(dimension)
            index.add(np.array(all_embeddings))
            st.session_state.faiss_index = index
            st.write("**FAISS index created successfully.**")
        else:
            index = st.session_state.faiss_index

# Chat interface
st.subheader("Chat with the Document Bot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Ask a question about the documents...")
if user_input and "faiss_index" in st.session_state:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Retrieve relevant chunks
    query_embedding = model.encode([user_input])
    D, I = st.session_state.faiss_index.search(query_embedding, 3)
    
    # Combine retrieved chunks into context
    context = "\n\n".join([documents[i] for i in I[0]])
    
    # Generate a prompt for the LLM
    prompt = f"""
    You are an AI assistant that answers questions based on the provided context.
    Your task is to generate a clear and concise answer using ONLY the information from the context.
    If the context does not contain enough information, say "I don't know."

    Context:
    {context}

    Question:
    {user_input}

    Answer:
    """

    # Use Ollama's DeepSeek LLM to generate an answer
    with st.spinner("Thinking..."):
        try:
            response = ollama.generate(
                model="deepseek-r1:1.5b",  # Use the DeepSeek model
                prompt=prompt
            )
            answer = response['response']
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
            answer = "Failed to generate an answer."

    # Add bot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    
    # Display the bot's response
    with st.chat_message("assistant"):
        st.write(answer)
    
    # Display the relevant context (optional)
    with st.expander("See relevant context"):
        st.write(context)