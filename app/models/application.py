"""
Job application model (many-to-many with extra fields).
"""

import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ApplicationStatus(str, enum.Enum):
    """Application status."""
    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"


class Application(Base):
    """Job application model connecting applicants to jobs."""
    
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    cover_letter = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.PENDING)
    applied_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    company_id = Column(Integer, ForeignKey("company_profiles.id"), nullable=False, index=True)
    
    # Relationships
    applicant = relationship("ApplicantProfile", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    company = relationship("CompanyProfile", back_populates="applications")
    
    def __repr__(self):
        return f"<Application(id={self.id}, applicant_id={self.applicant_id}, job_id={self.job_id}, status={self.status})>"

