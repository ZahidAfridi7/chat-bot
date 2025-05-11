# app/core/config.py
from pydantic_settings import BaseSettings
from datetime import timedelta

class Settings(BaseSettings):
    PROJECT_NAME: str = "Quantum AI Chatbot"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Local PostgreSQL DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "seven"
    POSTGRES_DB: str = "chat_bot"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    SECRET_KEY: str = "supersecretkey123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
        )
    @property
        
    def access_token_expiry(self):
       return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
