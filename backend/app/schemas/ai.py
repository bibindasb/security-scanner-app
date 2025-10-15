# backend/app/schemas/ai.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AIAnalysisRequest(BaseModel):
    scan_id: str
    provider: Optional[str] = None
    model: Optional[str] = None

class RemediationStep(BaseModel):
    priority: str
    action: str
    description: Optional[str] = None
    findings_affected: List[str] = []
    sample_code: Optional[Dict[str, str]] = None
    verification: Optional[str] = None

class Recommendation(BaseModel):
    category: str
    recommendation: str
    rationale: Optional[str] = None

class AIAnalysisData(BaseModel):
    summary: str
    risk_score: Optional[str] = None
    prioritized_remediation: List[RemediationStep] = []
    additional_recommendations: List[Recommendation] = []
    compliance_notes: Optional[str] = None
    error: Optional[str] = None

class AIAnalysisResponse(BaseModel):
    id: str
    scan_id: str
    provider: str
    model: str
    analysis: AIAnalysisData
    created_at: datetime

    class Config:
        from_attributes = True

class ProviderInfo(BaseModel):
    providers: List[str]
    models: Dict[str, List[str]]