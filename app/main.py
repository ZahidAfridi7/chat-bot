from fastapi import FastAPI,Depends
from app.api.api import api_router
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

app = FastAPI(title=settings.PROJECT_NAME,
            version=settings.VERSION)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Quantum AI Chatbot Backend is running"}
