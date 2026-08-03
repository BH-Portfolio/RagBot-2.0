import streamlit as st

def render_history_download():
    if "messages" in st.session_state:
        chat_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in st.session_state["messages"]
        )
        st.download_button(
            "Download chat history",
            chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )
        