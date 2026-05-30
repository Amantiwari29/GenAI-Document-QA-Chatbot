from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import process_pdf
from app.services.embedding_service import embed_chunks
from app.services.chroma_service import store_chunks, retrieve_relevant_chunks
from app.services.chat_service import generate_answer
from app.models import AskRequest, AskResponse, UploadResponse
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload-doc", response_model=UploadResponse)
async def upload_doc(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    chunks, metadata = await process_pdf(file)
    embeddings = await embed_chunks(chunks)
    await store_chunks(embeddings, chunks, metadata)
    return UploadResponse(message="Document uploaded and processed successfully.")

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    relevant_chunks = await retrieve_relevant_chunks(request.question, top_k=5)
    answer, sources = await generate_answer(request.question, relevant_chunks)
    return AskResponse(answer=answer, sources=sources)
