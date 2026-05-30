from sentence_transformers import SentenceTransformer
from app.config import settings
from typing import List

model = SentenceTransformer(settings.EMBEDDING_MODEL)

async def embed_chunks(chunks: List[str]) -> List[List[float]]:
    embeddings = model.encode(
        chunks,
        show_progress_bar=False
    )
    return embeddings.tolist()