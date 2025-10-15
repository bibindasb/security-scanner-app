# backend/app/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://scanner:scanner@db:5432/security_scanner"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    # AI Settings
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OPENAI_API_KEY: Optional[str] = None
    OPENROUTE_API_KEY: Optional[str] = None
    
    # Scanner Settings
    MAX_SCAN_DURATION: int = 300
    USER_AGENT: str = "SecurityScanner/1.0"
    
    class Config:
        env_file = ".env"

settings = Settings()