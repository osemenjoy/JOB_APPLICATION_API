"""
Service for job application management.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List, Tuple

from app.models.user import User
from app.models.application import Application
from app.models.job import Job
from app.repositories.application_repository import ApplicationRepository
from app.schemas.application import (
    ApplicationCreate, ApplicationUpdate, ApplicationResponse,
    ApplicationDetailResponse, ApplicationFilterParams, PaginatedApplicationResponse
)


class ApplicationService:
    """Service for job application management."""
    
    def __init__(self, db: Session):
        self.db = db
        self.app_repo = ApplicationRepository(db)
    
    def submit_application(self, user: User, app_create: ApplicationCreate) -> ApplicationDetailResponse:
        """Submit a new job application."""
        # Ensure only APPLICANT users can apply for jobs
        if user.role.value != "APPLICANT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only applicants can submit job applications. Hirers cannot apply for jobs."
            )
        
        # Ensure user has an applicant profile
        if not user.applicant_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please complete your applicant profile before applying for jobs"
            )
        
        # Check if user has already applied to this job
        if self.app_repo.application_exists(user.applicant_profile.id, app_create.job_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied for this job"
            )
        
        # Get the job to retrieve company_id
        job = self.db.query(Job).filter(Job.id == app_create.job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Create application with applicant_id, job_id, and company_id
        application = self.app_repo.create(
            applicant_id=user.applicant_profile.id,
            job_id=app_create.job_id,
            company_id=job.company_id,
            cover_letter=app_create.cover_letter,
            resume_url=app_create.resume_url
        )
        return ApplicationDetailResponse.from_orm(application)
    
    def get_user_applications(
        self,
        user: User,
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedApplicationResponse:
        """Get all applications for the current user."""
        if not user.applicant_profile:
            return PaginatedApplicationResponse(
                total=0,
                skip=skip,
                limit=limit,
                items=[]
            )
        
        total, applications = self.app_repo.get_user_applications(user.applicant_profile.id, skip, limit)
        
        return PaginatedApplicationResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[ApplicationResponse.from_orm(app) for app in applications]
        )
    
    def get_application(self, user: User, app_id: int) -> ApplicationDetailResponse:
        """Get a specific application."""
        application = self.app_repo.get_by_id(app_id)
        
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        
        # Check authorization
        if application.user_id != user.id and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this application"
            )
        
        return ApplicationDetailResponse.from_orm(application)
    
    def update_application(
        self,
        user: User,
        app_id: int,
        app_update: ApplicationUpdate
    ) -> ApplicationDetailResponse:
        """Update an application."""
        application = self.app_repo.get_by_id(app_id)
        
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        
        # Check authorization
        if not user.role == "HIRER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this application"
            )
        
        # Users can't modify status/rating/notes unless admin
        updated_app = self.app_repo.update_status(app_id, app_update.status)
        return ApplicationDetailResponse.from_orm(updated_app)
    
    def delete_application(self, user: User, app_id: int) -> bool:
        """Delete an application."""
        application = self.app_repo.get_by_id(app_id)
        
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        
        # Check authorization
        if application.user_id != user.id and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this application"
            )
        
        return self.app_repo.delete(app_id)
    
    def filter_by_skill(
        self,
        user: User,
        skill: str,
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedApplicationResponse:
        """Filter applications by skill."""
        # Regular users see only their own applications
        user_id = user.id
        total, applications = self.app_repo.filter_by_skill(skill, user_id, skip, limit)
        
        return PaginatedApplicationResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[ApplicationResponse.from_orm(app) for app in applications]
        )

    def get_company_applications(self, company_id: int, skip: int = 0, limit: int = 10) -> PaginatedApplicationResponse:
        """Get all applications for a specific company."""
        total, applications = self.app_repo.filter_by_company(company_id, skip, limit)
        
        return PaginatedApplicationResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[ApplicationResponse.from_orm(app) for app in applications]
        )
  