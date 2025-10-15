# backend/app/schemas/ai.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AIAnalysisRequest(BaseModel):
    scan_id: str
    provider: Optional[str] = "ollama"

class AIAnalysisResponse(BaseModel):
    id: str
    scan_id: str
    provider: str
    model: str
    analysis: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True