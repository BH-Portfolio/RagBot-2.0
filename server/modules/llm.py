import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about the user's uploaded "
    "documents. Use the retrieved context below to answer the question. "
    "If you don't know the answer from the context, say you don't know.\n\n"
    "Context:\n{context}"
)

def get_llm_chain(vector_store):
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-120b"
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    return retrieval_chain
