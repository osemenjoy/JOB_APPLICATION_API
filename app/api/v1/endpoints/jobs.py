"""
Job management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_current_admin_user, get_current_user
from app.db.session import get_db
from app.services.job_service import JobService
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_job_service(db: Session = Depends(get_db)) -> JobService:
    """Dependency to get job service."""
    return JobService(db)


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_create: JobCreate,
    current_user: User = Depends(get_current_admin_user),
    job_service: JobService = Depends(get_job_service)
):
    """
    Create a new job posting.
    
    Only company users can create jobs.
    - **title**: Job title (min 3 characters)
    - **description**: Job description (min 10 characters)
    - **required_skills**: List of required skills
    - **location**: Job location
    - **salary_range**: Salary range (optional)
    - **employment_type**: FULL_TIME, PART_TIME, CONTRACT, or FREELANCE
    """
    return job_service.create_job(job_create, current_user)


@router.get("/my-jobs", response_model=JobListResponse)
async def list_my_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_admin_user),
    job_service: JobService = Depends(get_job_service)
):
    """
    List all jobs created by the current company.
    
    Requires authentication. Only for company users.
    - **skip**: Number of jobs to skip (pagination)
    - **limit**: Number of jobs to return (max 100)
    """
    return job_service.list_company_jobs(current_user, skip, limit)


@router.get("", response_model=JobListResponse)
async def list_all_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    job_service: JobService = Depends(get_job_service)
):
    """
    List all active job postings.
    
    - **skip**: Number of jobs to skip (pagination)
    - **limit**: Number of jobs to return (max 100)
    """
    return job_service.list_all_jobs(skip, limit)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    job_service: JobService = Depends(get_job_service)
):
    """
    Get a job by ID.
    
    - **job_id**: Job ID
    """
    return job_service.get_job(job_id)


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    current_user: User = Depends(get_current_admin_user),
    job_service: JobService = Depends(get_job_service)
):
    """
    Update a job posting.
    
    Only the company owner can update their job postings.
    - **job_id**: Job ID to update
    - **job_update**: Fields to update (all optional)
    """
    return job_service.update_job(job_id, job_update, current_user)


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
async def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_admin_user),
    job_service: JobService = Depends(get_job_service)
):
    """
    Delete a job posting.
    
    Only the company owner can delete their job postings.
    - **job_id**: Job ID to delete
    """
    return job_service.delete_job(job_id, current_user)


@router.patch("/{job_id}/deactivate", response_model=JobResponse)
async def deactivate_job(
    job_id: int,
    current_user: User = Depends(get_current_admin_user),
    job_service: JobService = Depends(get_job_service)
):
    """
    Deactivate a job posting (soft delete).
    
    Only the company owner can deactivate their job postings.
    - **job_id**: Job ID to deactivate
    """
    return job_service.deactivate_job(job_id, current_user)
