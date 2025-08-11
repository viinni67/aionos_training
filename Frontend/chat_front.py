import streamlit as st
import requests

# Backend API URL (FastAPI must be running)
API_URL = "http://127.0.0.1:8000/search"

st.set_page_config(page_title="Chatbot", layout="centered")

# 🎨 Custom CSS for bluish theme
st.markdown("""
    <style>
    body {
        background-color: #e8f0fe; /* Light blue background */
        color: #003366; /* Dark blue text */
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stChatMessage.user {
        background-color: #cce5ff; /* Light blue bubble */
        color: #003366;
    }
    .stChatMessage.assistant {
        background-color: #b3d9ff; /* Slightly darker blue */
        color: #00264d;
    }
    </style>
""", unsafe_allow_html=True)

st.title(" Indigo source training Rag_based ")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show existing messages
for message in st.session_state.messages:
    bubble_class = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(message["role"]):
        st.markdown(f"<div class='stChatMessage {bubble_class}'>{message['content']}</div>", unsafe_allow_html=True)

# User input
if prompt := st.chat_input("Ask a question..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='stChatMessage user'>{prompt}</div>", unsafe_allow_html=True)

    # Send to FastAPI backend
    try:
        response = requests.post("http://127.0.0.1:8000/search/", json={"query": prompt})
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer") or data.get("context", "No answer found.")

            # Save bot message
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(f"<div class='stChatMessage assistant'>{answer}</div>", unsafe_allow_html=True)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
