import streamlit as st
import backend
import os

st.title("💬 RAG Chatbot with Document Management")

# Create a directory to store uploaded files
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# File uploader
uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Process file and store embeddings
        result = backend.process_and_store_embeddings(file_path, uploaded_file.name)
        st.success(result)

# Display uploaded files
if backend.uploaded_files:
    file_to_delete = st.selectbox("Select a file to delete", list(backend.uploaded_files.keys()))

    if st.button("Delete File"):
        result = backend.delete_file_and_embeddings(file_to_delete)
        st.success(result)

# Chatbot UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = backend.chat(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
