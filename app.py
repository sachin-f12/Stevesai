import streamlit as st
from backend import chat


# Streamlit UI
st.title("💬 Custom Chatbot")

#uploading a file 
uploaded_files = st.file_uploader(
    "Upload files ", accept_multiple_files=True
)
   
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chat(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})