from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME,
            version=settings.VERSION)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Quantum AI Chatbot Backend is running"}
