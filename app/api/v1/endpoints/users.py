"""
User management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from app.models.user import User
from app.api.deps import get_user_service, get_current_user, get_current_admin_user
from app.services.user_service import UserService
from app.schemas.user import (
    UserResponse, UserUpdate, CompanyProfileCreate, CompanyProfileUpdate, CompanyProfileResponse,
    ApplicantProfileCreate, ApplicantProfileUpdate, ApplicantProfileResponse
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get current user's profile.
    Requires authentication.
    """
    return user_service.get_user_profile(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update current user's profile information.
    Requires authentication.
    
    - **full_name**: Optional, new full name
    - **email**: Optional, new email address (must be unique)
    """
    return user_service.update_user_profile(current_user, user_update)


# Company Profile Endpoints
@router.post("/profile/company", response_model=CompanyProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_company_profile(
    profile: CompanyProfileCreate,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Create company profile for HIRER users.
    
    Only users with HIRER role can create company profiles.
    - **company_name**: Company name (required)
    - **company_description**: Company description (optional)
    - **website**: Company website URL (optional)
    - **industry**: Industry type (optional)
    """
    return user_service.create_company_profile(current_user, profile)


@router.get("/profile/company", response_model=CompanyProfileResponse)
async def get_company_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get current user's company profile.
    Requires HIRER user with existing company profile.
    """
    return user_service.get_company_profile(current_user)


@router.put("/profile/company", response_model=CompanyProfileResponse)
async def update_company_profile(
    profile: CompanyProfileUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update current user's company profile.
    
    All fields are optional.
    """
    return user_service.update_company_profile(current_user, profile)


@router.delete("/profile/company", status_code=status.HTTP_200_OK)
async def delete_company_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Delete current user's company profile.
    """
    user_service.delete_company_profile(current_user)
    return {"message": "Company profile deleted successfully"}


# Applicant Profile Endpoints
@router.post("/profile/applicant", response_model=ApplicantProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_applicant_profile(
    profile: ApplicantProfileCreate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Create applicant profile for APPLICANT users.
    
    Only users with APPLICANT role can create applicant profiles.
    - **bio**: Applicant bio/about (optional)
    - **skills**: List of skills (optional)
    - **years_of_experience**: Years of experience (optional)
    - **resume_url**: Resume URL (optional)
    - **github_url**: GitHub profile URL (optional)
    - **linkedin_url**: LinkedIn profile URL (optional)
    """
    return user_service.create_applicant_profile(current_user, profile)


@router.get("/profile/applicant", response_model=ApplicantProfileResponse)
async def get_applicant_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get current user's applicant profile.
    Requires APPLICANT user with existing applicant profile.
    """
    return user_service.get_applicant_profile(current_user)


@router.put("/profile/applicant", response_model=ApplicantProfileResponse)
async def update_applicant_profile(
    profile: ApplicantProfileUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update current user's applicant profile.
    
    All fields are optional.
    """
    return user_service.update_applicant_profile(current_user, profile)


@router.delete("/profile/applicant", status_code=status.HTTP_200_OK)
async def delete_applicant_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Delete current user's applicant profile.
    """
    user_service.delete_applicant_profile(current_user)
    return {"message": "Applicant profile deleted successfully"}
