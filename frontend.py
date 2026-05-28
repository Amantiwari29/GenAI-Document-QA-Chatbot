import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Document QA Chatbot")

# PDF Upload
st.header("Upload PDF Document")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    with st.spinner("Uploading and processing..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{API_URL}/upload-doc", files=files)
        if response.status_code == 200:
            st.success("Document uploaded and processed!")
        else:
            st.error(f"Upload failed: {response.text}")

# Chatbot Interface
st.header("Ask a Question")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_question = st.text_input("Your question:")
if st.button("Ask") and user_question:
    payload = {"question": user_question, "chat_history": st.session_state['chat_history']}
    with st.spinner("Getting answer..."):
        response = requests.post(f"{API_URL}/ask", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state['chat_history'].append(user_question)
            st.markdown(f"**Answer:** {data['answer']}")
            st.markdown("**Sources:**")
            for src in data['sources']:
                st.json(src)
        else:
            st.error(f"Error: {response.text}")
