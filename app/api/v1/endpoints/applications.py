"""
Job application endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.models.user import User
from app.api.deps import get_application_service, get_current_user, get_current_admin_user
from app.services.application_service import ApplicationService
from app.schemas.application import (
    ApplicationCreate, ApplicationDetailResponse, ApplicationUpdate,
    PaginatedApplicationResponse, ApplicationFilterParams
)

router = APIRouter(prefix="/applications", tags=["Applications"])


# User endpoints

@router.post("/", response_model=ApplicationDetailResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """
    Submit a new job application.
    Requires authentication.
    """
    return app_service.submit_application(current_user, application_data)


@router.get("/", response_model=PaginatedApplicationResponse)
async def get_my_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """
    Get all applications for the current user.
    Requires authentication.
    """
    return app_service.get_user_applications(current_user, skip, limit)


@router.get("/filter/skill", response_model=PaginatedApplicationResponse)
async def filter_by_skill(
    skill: str = Query(..., description="Skill to filter by"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """
    Filter applications by skill (case-insensitive).
    Regular users see only their own applications.
    HIRERS can see their companies applications.
    """
    return app_service.filter_by_skill(current_user, skill, skip, limit)


@router.get("/{application_id}", response_model=ApplicationDetailResponse)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """
    Get a specific application.
    Users can only access their own applications unless they are admins.
    """
    return app_service.get_application(current_user, application_id)


@router.put("/{application_id}", response_model=ApplicationDetailResponse)
async def update_application_status(
    application_id: int,
    application_update: ApplicationUpdate,
    current_user: User = Depends(get_current_admin_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """
    Update an application.
    Users can only update their own applications unless they are admins.
    Admins can modify status, rating, and notes.
    """
    return app_service.update_application(current_user, application_id, application_update)


@router.get("/company/{company_id}", response_model=PaginatedApplicationResponse)
async def retrieve_companies_applications(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_admin_user),
    app_service: ApplicationService = Depends(get_application_service)
):
    """
    Retrieve all applications for a specific company.
    Only a company can see all the applications to their job.
    """
    return app_service.get_company_applications(company_id, skip, limit)