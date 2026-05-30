import httpx
from typing import List, Dict, Tuple
from app.config import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_answer(
    question: str,
    relevant_chunks: List[Dict]
) -> Tuple[str, List[Dict]]:

    # Extract top chunks safely
    context = "\n".join([
        chunk.get("chunk", "")
        for chunk in relevant_chunks[:3]
    ])

    # Prevent token overflow
    context = context[:6000]

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful document question answering assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:

            response = await client.post(
                GROQ_API_URL,
                headers=headers,
                json=payload
            )

            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)

            response.raise_for_status()

            data = response.json()

            answer = (
                data["choices"][0]["message"]["content"]
                .strip()
            )

    except httpx.HTTPStatusError as e:
        print("HTTP ERROR:", e.response.text)
        return "Error generating answer from Groq API.", []

    except Exception as e:
        print("UNEXPECTED ERROR:", str(e))
        return "Unexpected server error occurred.", []

    # Extract metadata sources
    sources = [
    f"Page {chunk.get('metadata', {}).get('page', 'Unknown')}"
    for chunk in relevant_chunks[:3]
    ]

    return answer, sources