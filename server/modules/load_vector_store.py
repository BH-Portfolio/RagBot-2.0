import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PERSIST_DIRECTORY = "chroma_store"
UPLOAD_DIR = "uploaded_pdfs"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_vector_store(uploaded_files):
    file_paths = []

    for file in uploaded_files:
        save_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(save_path)

    docs = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=100)
    texts = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2")

    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        vector_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings
        )
        vector_store.add_documents(texts)
        vector_store.persist()
    else:
        vector_store = Chroma.from_documents(
            texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        vector_store.persist()

    return vector_store
