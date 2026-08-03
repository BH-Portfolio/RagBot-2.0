import streamlit as st
from utils.api import ask_question_api

def render_chat():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask something about your PDFs...")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        response = ask_question_api(user_input)

        if response.status_code == 200:
            answer = response.json().get("response", "")
        else:
            answer = f"Error: {response.text}"


        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
        