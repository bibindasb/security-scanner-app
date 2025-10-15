# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from app.api import scans, ai, auth
from app.config import settings
from app.models.database import create_db_and_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    logger.info("Application started successfully")
    yield
    # Shutdown
    logger.info("Application shutting down")

app = FastAPI(
    title="Security Scanner API",
    description="Automated website security scanning with AI remediation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["scans"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])

@app.get("/")
async def root():
    return {"message": "Security Scanner API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api")
async def api_info():
    return {
        "name": "Security Scanner API",
        "version": "1.0.0",
        "endpoints": {
            "scans": "/api/v1/scans",
            "ai": "/api/v1/ai",
            "auth": "/api/v1/auth"
        }
    }