# backend/app/api/scans.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.models.database import get_db, Scan, Finding
from app.scanners.scanner_manager import ScannerManager
from app.schemas.scans import ScanCreate, ScanResponse, FindingResponse

router = APIRouter()

@router.post("/", response_model=ScanResponse)
async def create_scan(
    scan_data: ScanCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    scan = Scan(
        id=str(uuid.uuid4()),
        target_url=scan_data.target_url,
        scan_config=scan_data.scan_config.dict() if scan_data.scan_config else {}
    )
    
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    # Start scan in background
    background_tasks.add_task(run_security_scan, scan.id, scan.target_url, db)
    
    return scan

@router.get("/", response_model=List[ScanResponse])
async def list_scans(db: Session = Depends(get_db)):
    return db.query(Scan).order_by(Scan.created_at.desc()).all()

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

@router.get("/{scan_id}/findings", response_model=List[FindingResponse])
async def get_scan_findings(scan_id: str, db: Session = Depends(get_db)):
    findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()
    return findings

async def run_security_scan(scan_id: str, target_url: str, db: Session):
    try:
        # Update scan status
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        scan.status = "running"
        db.commit()
        
        # Run scanners
        scanner_manager = ScannerManager(target_url)
        findings_data = await scanner_manager.run_all_scans()
        
        # Save findings
        for finding_data in findings_data:
            # Remove id from finding_data if it exists to avoid conflicts
            finding_data_clean = {k: v for k, v in finding_data.items() if k != 'id'}
            finding = Finding(
                scan_id=scan_id,
                **finding_data_clean
            )
            db.add(finding)
        
        # Update scan status
        scan.status = "completed"
        db.commit()
        
    except Exception as e:
        scan.status = "failed"
        db.commit()
        # Log error
        print(f"Scan failed: {str(e)}")