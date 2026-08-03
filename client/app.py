import streamlit as st

st.set_page_config(page_title="Ragbot 2.0", layout="wide")
st.title("RAG PDF Chatbot")

from components.upload import render_uploader
from components.chat_ui import render_chat
from components.history_download import render_history_download

render_uploader
render_chat
render_history_download

