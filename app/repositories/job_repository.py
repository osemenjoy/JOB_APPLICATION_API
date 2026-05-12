"""
Repository for job data access.
"""

from sqlalchemy.orm import Session
from typing import Optional, List, Tuple

from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


class JobRepository:
    """Repository for job data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, job_create: JobCreate, company_id: int) -> Job:
        """Create a new job."""
        db_job = Job(
            company_id=company_id,
            title=job_create.title,
            description=job_create.description,
            required_skills=job_create.required_skills,
            location=job_create.location,
            salary_range=job_create.salary_range,
            employment_type=job_create.employment_type,
            status=job_create.status,
        )
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job
    
    def get_by_id(self, job_id: int) -> Optional[Job]:
        """Get job by ID."""
        return self.db.query(Job).filter(Job.id == job_id).first()
    
    def get_by_company(self, company_id: int, skip: int = 0, limit: int = 10) -> Tuple[int, List[Job]]:
        """Get all jobs for a company with pagination."""
        total = self.db.query(Job).filter(Job.company_id == company_id).count()
        jobs = self.db.query(Job).filter(Job.company_id == company_id).offset(skip).limit(limit).all()
        return total, jobs
    
    def get_all(self, skip: int = 0, limit: int = 10, status: Optional[bool] = True) -> Tuple[int, List[Job]]:
        """Get all jobs with pagination and optional status filter."""
        query = self.db.query(Job)
        if status is not None:
            query = query.filter(Job.status == status)
        
        total = query.count()
        jobs = query.offset(skip).limit(limit).all()
        return total, jobs
    
    def get_active(self, skip: int = 0, limit: int = 10) -> Tuple[int, List[Job]]:
        """Get all active jobs."""
        return self.get_all(skip, limit, status=True)
    
    def update(self, job_id: int, job_update: JobUpdate) -> Optional[Job]:
        """Update a job."""
        db_job = self.get_by_id(job_id)
        if db_job:
            if job_update.title is not None:
                db_job.title = job_update.title
            if job_update.description is not None:
                db_job.description = job_update.description
            if job_update.required_skills is not None:
                db_job.required_skills = job_update.required_skills
            if job_update.location is not None:
                db_job.location = job_update.location
            if job_update.salary_range is not None:
                db_job.salary_range = job_update.salary_range
            if job_update.employment_type is not None:
                db_job.employment_type = job_update.employment_type
            if job_update.status is not None:
                db_job.status = job_update.status
            
            self.db.commit()
            self.db.refresh(db_job)
        return db_job
    
    def delete(self, job_id: int) -> bool:
        """Delete a job."""
        db_job = self.get_by_id(job_id)
        if db_job:
            self.db.delete(db_job)
            self.db.commit()
            return True
        return False
    
    def deactivate(self, job_id: int) -> Optional[Job]:
        """Deactivate a job (soft delete)."""
        db_job = self.get_by_id(job_id)
        if db_job:
            db_job.status = False
            self.db.commit()
            self.db.refresh(db_job)
        return db_job
