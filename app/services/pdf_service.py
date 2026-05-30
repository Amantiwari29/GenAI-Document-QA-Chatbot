import io
import PyPDF2
from typing import Tuple, List
from fastapi import UploadFile

CHUNK_SIZE = 500  # characters
CHUNK_OVERLAP = 100  # characters

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

async def process_pdf(file: UploadFile) -> Tuple[List[str], List[dict]]:
    file_bytes = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    chunks = chunk_text(text)
    metadata = [{"page": i+1} for i in range(len(chunks))]
    return chunks, metadata