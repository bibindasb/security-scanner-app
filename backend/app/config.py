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
    OPENROUTE_API_KEY: Optional[str] = None
    OPENROUTE_MODEL: str = "meta-llama/llama-2-70b-chat"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Scanner Settings
    MAX_SCAN_DURATION: int = 300
    USER_AGENT: str = "SecurityScanner/1.0"
    
    class Config:
        env_file = ".env"

settings = Settings()