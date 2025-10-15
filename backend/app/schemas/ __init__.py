# backend/app/schemas/__init__.py
from .scans import (
    ScanCreate,
    ScanResponse, 
    FindingResponse,
    ScanConfig,
    ScanStatus,
    SeverityLevel
)
from .ai import AIAnalysisRequest, AIAnalysisResponse

__all__ = [
    "ScanCreate",
    "ScanResponse",
    "FindingResponse", 
    "ScanConfig",
    "ScanStatus",
    "SeverityLevel",
    "AIAnalysisRequest",
    "AIAnalysisResponse"
]