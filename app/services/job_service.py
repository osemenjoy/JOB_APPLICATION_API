"""
Service for job management.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Tuple

from app.models.job import Job
from app.models.user import User
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse


class JobService:
    """Service for job management."""
    
    def __init__(self, db: Session):
        self.db = db
        self.job_repo = JobRepository(db)
    
    def create_job(self, job_create: JobCreate, current_user: User) -> JobResponse:
        """Create a new job posting (company only)."""
        # Check if user has a company profile
        if not current_user.company_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only company users can create job postings"
            )
        
        job = self.job_repo.create(job_create, current_user.company_profile.id)
        return JobResponse.from_orm(job)
    
    def get_job(self, job_id: int) -> JobResponse:
        """Get a job by ID."""
        job = self.job_repo.get_by_id(job_id)
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        return JobResponse.from_orm(job)
    
    def list_all_jobs(self, skip: int = 0, limit: int = 10) -> JobListResponse:
        """List all active jobs with pagination."""
        total, jobs = self.job_repo.get_active(skip, limit)
        return JobListResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[JobResponse.from_orm(job) for job in jobs]
        )
    
    def list_company_jobs(self, current_user: User, skip: int = 0, limit: int = 10) -> JobListResponse:
        """List all jobs created by the current company."""
        if not current_user.company_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only company users can view their jobs"
            )
        
        total, jobs = self.job_repo.get_by_company(current_user.company_profile.id, skip, limit)
        return JobListResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[JobResponse.from_orm(job) for job in jobs]
        )
    
    def update_job(self, job_id: int, job_update: JobUpdate, current_user: User) -> JobResponse:
        """Update a job (only company owner can update)."""
        job = self.job_repo.get_by_id(job_id)
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Check if user owns this job
        if not current_user.company_profile or job.company_id != current_user.company_profile.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own job postings"
            )
        
        updated_job = self.job_repo.update(job_id, job_update)
        return JobResponse.from_orm(updated_job)
    
    def delete_job(self, job_id: int, current_user: User) -> dict:
        """Delete a job (only company owner can delete)."""
        job = self.job_repo.get_by_id(job_id)
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Check if user owns this job
        if not current_user.company_profile or job.company_id != current_user.company_profile.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own job postings"
            )
        
        self.job_repo.delete(job_id)
        return {"message": "Job deleted successfully"}
    
    def deactivate_job(self, job_id: int, current_user: User) -> JobResponse:
        """Deactivate a job (soft delete)."""
        job = self.job_repo.get_by_id(job_id)
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Check if user owns this job
        if not current_user.company_profile or job.company_id != current_user.company_profile.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only deactivate your own job postings"
            )
        
        deactivated_job = self.job_repo.deactivate(job_id)
        return JobResponse.from_orm(deactivated_job)
