from fastapi import FastAPI
from app.api import routes
from app.config import settings
import logging

app = FastAPI(title="Document QA Chatbot")

# Include API routers
app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Configure logging
logging.basicConfig(level=logging.INFO)
