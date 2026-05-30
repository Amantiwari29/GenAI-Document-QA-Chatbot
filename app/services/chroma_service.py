import chromadb
from app.config import settings
from typing import List, Dict

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="docs", metadata={"persist_directory": settings.CHROMA_DB_PATH})

async def store_chunks(embeddings: List[List[float]], chunks: List[str], metadata: List[dict]):
    for i, (embedding, chunk, meta) in enumerate(zip(embeddings, chunks, metadata)):
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[meta],
            ids=[f"chunk_{i}"]
        )

async def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[Dict]:
    results = collection.query(query_texts=[query], n_results=top_k)
    return [
        {"chunk": doc, "metadata": meta}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]
