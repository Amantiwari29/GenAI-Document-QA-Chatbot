# Document QA Chatbot

## Features
- Upload PDF documents
- Extract and chunk text
- Generate embeddings (HuggingFace)
- Store in ChromaDB
- Ask questions, get contextual answers (RAG)
- FastAPI backend, Streamlit frontend

## Setup

1. Clone repo and install dependencies:
   ```zsh
   pip install -r requirements.txt
   ```
2. Set your `.env` variables (see `.env` example).
3. Run the API server:
   ```zsh
   uvicorn app.main:app --reload
   ```
4. (Optional) Build and run with Docker:
   ```zsh
   docker build -t doc-qa-bot .
   docker run -p 8000:8000 --env-file .env doc-qa-bot
   ```

## API Endpoints
- `POST /upload-doc` — Upload PDF
- `POST /ask` — Ask a question
- `GET /health` — Health check

## Frontend
- Streamlit app (coming soon)

## Notes
- ChromaDB persists locally
- Supports multi-PDF, chat history, and source chunk retrieval
# GenAI-Document-QA-Chatbot
