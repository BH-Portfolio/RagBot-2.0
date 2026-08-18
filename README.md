# RagBot 2.0 — RAG PDF Chatbot

A modular Retrieval-Augmented Generation (RAG) chatbot that lets you upload PDFs and ask questions about them. Built with a decoupled frontend/backend microservice architecture.

**Stack:** FastAPI · Streamlit · ChromaDB · LangChain · LLaMA (via Groq) · HuggingFace Embeddings

## Architecture

```
User → Streamlit (frontend) → FastAPI (backend) → ChromaDB (vector store) → Groq LLM → Response
```

- **`client/`** — Streamlit UI: upload PDFs, chat interface, download chat history
- **`server/`** — FastAPI backend: PDF processing, chunking, embeddings, vector storage, LLM querying

## Features

- Upload multiple PDFs and store them as embedded vector chunks
- Ask natural-language questions and get context-aware answers with source attribution
- Persistent vector store (ChromaDB) across sessions
- Download chat history as a `.txt` file
- CORS-restricted API — configured to accept requests only from the deployed frontend domain (edit `allow_origins` in `main.py` for other setups)

## Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/keys)
- Docker (optional, for containerized run)

## Project Structure

```
ragbot-2.0/
├── server/
│   ├── modules/
│   │   ├── llm.py
│   │   ├── load_vector_store.py
│   │   ├── pdf_handlers.py
│   │   └── query_handlers.py
│   ├── main.py
│   ├── logger.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── client/
│   ├── components/
│   │   ├── upload.py
│   │   ├── chat_ui.py
│   │   └── history_download.py
│   ├── utils/
│   │   └── api.py
│   ├── config.py
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── docker-compose.yml
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/ragbot-2.0.git
cd ragbot-2.0
```

### 2. Backend

```bash
cd server
python -m venv myenv
source myenv/bin/activate   # myenv\Scripts\activate on Windows
pip install -r requirements.txt
```

> Requires `langchain-classic`, `langchain-text-splitters`, and `langchain-chroma` in addition to core `langchain` — see `server/requirements.txt` for the full pinned list.

Create a `.env` file in `server/`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Run the backend:

```bash
uvicorn main:app --reload
```

API available at `http://127.0.0.1:8000`. Test it at `/test`.

### 3. Frontend

In a new terminal:

```bash
cd client
pip install -r requirements.txt
streamlit run app.py
```

App available at `http://localhost:8501`.

## Running with Docker

From the project root:

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8501`

Vector store and uploaded PDFs persist via named Docker volumes (`chroma_data`, `uploads_data`).

> Note: the `Dockerfile` `CMD`s bind to `$PORT` (falling back to 8000/8501 if unset) for compatibility with hosts like Railway that assign ports dynamically.

## API Endpoints

| Method | Endpoint         | Description                          |
|--------|------------------|---------------------------------------|
| GET    | `/test`          | Health check                          |
| POST   | `/upload_pdfs/`  | Upload one or more PDFs (form-data)   |
| POST   | `/ask`           | Ask a question (`?question=...`)      |

## Deployment

This app runs as two long-lived Docker services with a persistent vector store, so it's best suited to a Docker-friendly host such as **Railway**:

1. Push this repo to GitHub.
2. Create two services (one per `Dockerfile`: `server/` and `client/`).
3. Set `GROQ_API_KEY` on the backend service.
4. Set `API_URL` on the frontend service to the backend's public URL.
5. Attach persistent volumes to the backend at `/app/chroma_store` and `/app/uploaded_pdfs`.
6. Ensure `API_URL` includes the `https://` scheme (a bare domain will fail with `requests.exceptions.MissingSchema`).

## Tech Notes

- Embeddings: `all-MiniLM-L12-v2` (HuggingFace `sentence-transformers`)
- LLM: `openai/gpt-oss-120b` via Groq (Groq deprecates models frequently — check [console.groq.com/docs/models](https://console.groq.com/docs/models) if this stops working)
- Chunking: `RecursiveCharacterTextSplitter`, chunk size 1000, overlap 100
- Retrieval: top-3 relevant chunks per query
- Chain construction: `create_retrieval_chain` + `create_stuff_documents_chain` (`langchain-classic` ≥1.0) — not the deprecated `RetrievalQA` API

## Known Limitations / Lessons Learned

- **LangChain's API surface moves fast.** Core modules like text splitters and legacy chains (`RetrievalQA`) have been split out into separate packages (`langchain-text-splitters`, `langchain-classic`) across recent major versions — pin dependency versions if you need long-term stability.
- **Groq's hosted model lineup changes without much notice.** Models used in tutorials or examples can be decommissioned within months; always check the current model list before assuming a model name works.
- **Container platforms often assign ports dynamically.** Hardcoding a port in a Dockerfile `CMD` (rather than reading `$PORT`) can silently break deployments on platforms like Railway even when the container itself is running fine.
