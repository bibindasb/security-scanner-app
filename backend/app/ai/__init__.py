# backend/app/ai/__init__.py
from .base import AIProvider
from .ollama_provider import OllamaProvider
from .manager import AIManager

__all__ = ["AIProvider", "OllamaProvider", "AIManager"]