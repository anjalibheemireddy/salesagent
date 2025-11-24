import streamlit as st
import requests

st.set_page_config(page_title="🛒 Sales Agent Chatbot", layout="wide")
st.title("🛒 Sales Agent Chatbot")

API_URL = "http://127.0.0.1:8000"  # FastAPI backend

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Type your message here..."):
    res = requests.post(f"{API_URL}/chat", json={"message": prompt}).json()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": res["assistant_response"]})

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])



# Checkout button
if st.sidebar.button("Checkout"):
    res = requests.post(f"{API_URL}/checkout").json()
    st.session_state.messages.append({"role": "assistant", "content": res["checkout_message"]})
