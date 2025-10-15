# backend/app/schemas/scans.py
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ScanConfig(BaseModel):
    scan_type: str = "quick"
    check_headers: bool = True
    check_ssl: bool = True
    check_ports: bool = True
    check_vulnerabilities: bool = True
    depth: str = "medium"

class ScanCreate(BaseModel):
    target_url: str
    scan_config: Optional[ScanConfig] = None

class FindingBase(BaseModel):
    type: str
    severity: SeverityLevel
    title: str
    description: str
    evidence: Optional[Dict[str, Any]] = None
    owasp_category: Optional[str] = None
    cve_id: Optional[str] = None
    remediation: Optional[str] = None
    location: Optional[str] = None

class FindingResponse(FindingBase):
    id: str
    scan_id: str

    class Config:
        from_attributes = True

class ScanResponse(BaseModel):
    id: str
    target_url: str
    status: ScanStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    scan_config: Dict[str, Any]
    findings: List[FindingResponse] = []

    class Config:
        from_attributes = True