# backend/app/api/ai.py
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db, Scan, AIAnalysis
from app.ai.manager import AIManager
from app.schemas.ai import AIAnalysisRequest, AIAnalysisResponse

router = APIRouter()
ai_manager = AIManager()

@router.post("/analyze", response_model=AIAnalysisResponse)
async def analyze_scan_findings(
    request: AIAnalysisRequest,
    db: Session = Depends(get_db)
):
    # Get scan and findings
    scan = db.query(Scan).filter(Scan.id == request.scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    findings = [{
        'id': finding.id,
        'type': finding.type,
        'severity': finding.severity,
        'title': finding.title,
        'description': finding.description,
        'remediation': finding.remediation
    } for finding in scan.findings]
    
    # Get AI analysis
    analysis_data = await ai_manager.analyze_scan(
        findings, 
        request.provider
    )
    
    # Save analysis
    ai_analysis = AIAnalysis(
        id=str(uuid.uuid4()),
        scan_id=request.scan_id,
        provider=request.provider or "openrouter",
        model=request.model or "meta-llama/llama-2-70b-chat",
        analysis=analysis_data
    )
    
    db.add(ai_analysis)
    db.commit()
    db.refresh(ai_analysis)
    
    return ai_analysis

@router.get("/providers")
async def get_available_providers():
    """Get list of available AI providers"""
    return {
        "providers": ai_manager.get_available_providers(),
        "models": {
            provider: ai_manager.get_provider_models(provider) 
            for provider in ai_manager.get_available_providers()
        }
    }

@router.get("/analysis/{scan_id}")
async def get_analysis(scan_id: str, db: Session = Depends(get_db)):
    """Get existing AI analysis for a scan"""
    analysis = db.query(AIAnalysis).filter(AIAnalysis.scan_id == scan_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis