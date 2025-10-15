# backend/app/api/ai.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
        request.provider or "ollama"
    )
    
    # Save analysis
    ai_analysis = AIAnalysis(
        id=str(uuid.uuid4()),
        scan_id=request.scan_id,
        provider=request.provider or "ollama",
        model="llama2",  # This should be dynamic
        analysis=analysis_data
    )
    
    db.add(ai_analysis)
    db.commit()
    db.refresh(ai_analysis)
    
    return ai_analysis