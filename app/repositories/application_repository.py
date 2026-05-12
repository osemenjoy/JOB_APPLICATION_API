"""
Repository for job application data access.
"""

from sqlalchemy.orm import Session
from sqlalchemy import cast, String
from typing import Optional, List
from datetime import datetime

from app.models.application import Application
from app.schemas.application import ApplicationUpdate


class ApplicationRepository:
    """Repository for application data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, applicant_id: int, job_id: int, company_id: int, cover_letter: str = None, resume_url: str = None) -> Application:
        """Create a new application."""
        db_app = Application(
            applicant_id=applicant_id,
            job_id=job_id,
            company_id=company_id,
            cover_letter=cover_letter,
            resume_url=resume_url,
            status="PENDING",
        )
        self.db.add(db_app)
        self.db.commit()
        self.db.refresh(db_app)
        return db_app
    
    def get_by_id(self, app_id: int) -> Optional[Application]:
        """Get application by ID."""
        return self.db.query(Application).filter(Application.id == app_id).first()
    
    def get_user_applications(self, applicant_id: int, skip: int = 0, limit: int = 10) -> tuple[int, List[Application]]:
        """Get all applications for an applicant with pagination."""
        total = self.db.query(Application).filter(Application.applicant_id == applicant_id).count()
        apps = self.db.query(Application).filter(
            Application.applicant_id == applicant_id
        ).offset(skip).limit(limit).all()
        return total, apps
    
    def get_all(self, skip: int = 0, limit: int = 10) -> tuple[int, List[Application]]:
        """Get all applications with pagination."""
        total = self.db.query(Application).count()
        apps = self.db.query(Application).offset(skip).limit(limit).all()
        return total, apps
    
    def filter_by_job(self, job_id: int, skip: int = 0, limit: int = 10) -> tuple[int, List[Application]]:
        """Filter applications by job ID."""
        query = self.db.query(Application).filter(Application.job_id == job_id)
        total = query.count()
        apps = query.offset(skip).limit(limit).all()
        return total, apps
    
    def filter_by_status(self, status: str, applicant_id: Optional[int] = None, skip: int = 0, limit: int = 10) -> tuple[int, List[Application]]:
        """Filter applications by status."""
        query = self.db.query(Application).filter(Application.status == status)
        if applicant_id:
            query = query.filter(Application.applicant_id == applicant_id)
        total = query.count()
        apps = query.offset(skip).limit(limit).all()
        return total, apps
    
    def filter_applications_by_applicant_skill(self, applicant_id: int, skill: str, skip: int = 0, limit: int = 10) -> tuple[int, List[Application]]:
        """Filter applications by skill matching job requirements for an applicant."""
        from app.models.job import Job
        query = self.db.query(Application).join(Job).filter(
            Application.applicant_id == applicant_id,
            cast(Job.required_skills, String).ilike(f"%{skill}%")
        )
        total = query.count()
        apps = query.offset(skip).limit(limit).all()
        return total, apps
    
    def filter_applications_by_hirer_applicant_skill(self, company_id: int, skill: str, skip: int = 0, limit: int = 10) -> tuple[int, List[Application]]:
        """Filter applications for a company by applicant skill matching."""
        from app.models.user import ApplicantProfile
        query = self.db.query(Application).join(ApplicantProfile).filter(
            Application.company_id == company_id,
            cast(ApplicantProfile.skills, String).ilike(f"%{skill}%")
        )
        total = query.count()
        apps = query.offset(skip).limit(limit).all()
        return total, apps
    
    def application_exists(self, applicant_id: int, job_id: int) -> bool:
        """Check if an application already exists for the given applicant and job."""
        return self.db.query(Application).filter(
            Application.applicant_id == applicant_id,
            Application.job_id == job_id
        ).first() is not None
    
    def delete(self, app_id: int) -> bool:
        """Delete an application."""
        db_app = self.get_by_id(app_id)
        if db_app:
            self.db.delete(db_app)
            self.db.commit()
            return True
        return False
    
    def update_status(self, app_id: int, status: str) -> Optional[Application]:
        """Update application status (admin only)."""
        db_app = self.get_by_id(app_id)
        if db_app:
            db_app.status = status
            db_app.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_app)
        return db_app
    
    def filter_by_company(self, company_id: int, skip: int = 0, limit: int = 10) -> tuple[int, List[Application]]:
        """Filter applications by company ID."""
        query = self.db.query(Application).filter(Application.company_id == company_id)
        total = query.count()
        apps = query.offset(skip).limit(limit).all()
        return total, apps
