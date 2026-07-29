import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_lim_chain(vector_store):
    pass
