# backend/app/models/database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    target_url = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    scan_config = Column(JSON, default={})
    
    # Relationships
    findings = relationship("Finding", back_populates="scan", cascade="all, delete-orphan")
    ai_analysis = relationship("AIAnalysis", back_populates="scan", uselist=False)

class Finding(Base):
    __tablename__ = "findings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, ForeignKey("scans.id"))
    type = Column(String, nullable=False)  # vulnerability, misconfiguration, info
    severity = Column(String, nullable=False)  # critical, high, medium, low, info
    title = Column(String, nullable=False)
    description = Column(Text)
    evidence = Column(JSON)
    owasp_category = Column(String)
    cve_id = Column(String)
    remediation = Column(Text)
    location = Column(String)
    
    # Relationships
    scan = relationship("Scan", back_populates="findings")

class AIAnalysis(Base):
    __tablename__ = "ai_analysis"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, ForeignKey("scans.id"))
    provider = Column(String, nullable=False)  # ollama, openai, openroute
    model = Column(String, nullable=False)
    analysis = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scan = relationship("Scan", back_populates="ai_analysis")