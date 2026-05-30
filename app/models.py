from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    message: str

class AskRequest(BaseModel):
    question: str
    chat_history: Optional[List[str]] = None

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
