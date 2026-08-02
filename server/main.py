from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from modules.load_vector_store import load_vector_store
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from logger import logger

app = FastAPI(title="RagBot 2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def test():
    return {"message": "testing successful"}


@app.middleware("http")
async def catch_exception_middleware(request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception("Unhandled exceptions")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"Received {len(files)} files")
        load_vector_store(files)
        logger.info("Documents added to vector store")
        return {"message": "Vector store updated"}
    except Exception as e:
        logger.exception("Error during PDF upload")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/ask")
async def ask_question(question: str):
    try:
        logger.info(f"User query: {question}")

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2")
        vector_store = Chroma(persist_directory="chroma_store", embedding_function=embeddings)

        chain = get_llm_chain(vector_store)
        result = query_chain(chain, question)

        logger.info("Query successful")
        return result
    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})
    
