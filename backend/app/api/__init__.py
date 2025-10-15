# backend/app/api/__init__.py
from .scans import router as scans_router
from .ai import router as ai_router
from .auth import router as auth_router

__all__ = ["scans_router", "ai_router", "auth_router"]