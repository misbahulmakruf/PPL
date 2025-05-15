import streamlit as st
import requests

def call_assistant_api(prompt: str):
    try:
        res = requests.post("http://localhost:8000/assistant", json={"query": prompt})
        return res.json().get("response", "[No response]")
    except Exception as e:
        return f"Error calling assistant: {e}"

def show_ai_assistant_from_api():
    st.title("AI Book Assistant (via API)")
    st.markdown("Ask a question like: `recommend books about psychology`")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("Type your question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            response = call_assistant_api(prompt)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
