"""
Service for user authentication and management.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional, Tuple

from app.core.security import SecurityUtility
from app.core.settings import get_settings
from app.models.user import User, RefreshToken, CompanyProfile, ApplicantProfile
from app.repositories.user_repository import UserRepository, RefreshTokenRepository
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserDetailResponse, OTPVerify, UserMessageResponse,
    CompanyProfileCreate, CompanyProfileUpdate, CompanyProfileResponse,
    ApplicantProfileCreate, ApplicantProfileUpdate, ApplicantProfileResponse
)
from app.schemas.token import TokenResponse


class UserService:
    """Service for user authentication and management."""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = RefreshTokenRepository(db)
    
    def register_user(self, user_create: UserCreate) -> UserResponse:
        """Register a new user."""
        
        if self.user_repo.get_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = SecurityUtility.hash_password(user_create.password)
        user = self.user_repo.create(user_create, hashed_password)
        
        return UserResponse.from_orm(user)
    
    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user by email and password."""
        user = self.user_repo.get_by_email(email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not SecurityUtility.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is not active. Please verify your email first."
            )
        
        return user
    
    def create_tokens(self, user: User) -> TokenResponse:
        """Create access and refresh tokens for a user."""
        settings = get_settings()
        
        # Create tokens - convert user.id to string for JWT sub claim
        access_token = SecurityUtility.create_access_token(data={"sub": str(user.id)})
        refresh_token = SecurityUtility.create_refresh_token(data={"sub": str(user.id)})
        
        # Store refresh token in database
        expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        self.token_repo.create(user.id, refresh_token, expires_at)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
    
    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Generate a new access token and refresh token using an old refresh token."""
        settings = get_settings()
        
        # Verify refresh token
        payload = SecurityUtility.verify_token(refresh_token)
        user_id = payload.get("sub")  # This is a string
        token_type = payload.get("type")
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Check if token is in database and not revoked
        db_token = self.token_repo.get_by_token(refresh_token)
        if not db_token or db_token.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is revoked"
            )
        
        # Check if expired
        if db_token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )
        
        # Revoke old refresh token
        self.token_repo.revoke(db_token.id)
        
        # Create new tokens
        access_token = SecurityUtility.create_access_token(data={"sub": user_id})
        new_refresh_token = SecurityUtility.create_refresh_token(data={"sub": user_id})
        
        # Store new refresh token in database
        new_expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        self.token_repo.create(int(user_id), new_refresh_token, new_expires_at)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
    
    def verify_otp(self, otp_verify: OTPVerify) -> UserMessageResponse:
        """Verify user's OTP."""
        user = self.user_repo.get_by_email(otp_verify.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        
        if otp_verify.otp != user.verification_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code"
            )
        
        if not user.verification_code_expires_at or user.verification_code_expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired"
            )
        
        # Activate user and clear verification code
        user.is_active = True
        user.verification_code = None
        user.verification_code_expires_at = None
        self.db.commit()
        self.db.refresh(user)
        
        return UserMessageResponse(
            message="OTP verified successfully",
            user=UserResponse.from_orm(user)
        )
    
    def resend_otp(self, email: str) -> UserMessageResponse:
        """Resend OTP to user's email."""
        user = self.user_repo.get_by_email(email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        
        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already active"
            )
        
        # Generate new OTP and update user
        user.verification_code = self.user_repo.verification_code_generator()
        user.verification_code_expires_at = datetime.utcnow() + timedelta(minutes=10)
        self.db.commit()
        self.db.refresh(user)
        return UserMessageResponse(
            message="OTP resent successfully",
            user=UserResponse.from_orm(user)
        )
    
    def logout_user(self, user: User) -> bool:
        """Logout user by revoking all refresh tokens."""
        revoked_count = self.token_repo.revoke_all_user_tokens(user.id)
        return revoked_count > 0
    
    def get_user_profile(self, user: User) -> UserResponse:
        """Get user profile information."""
        return UserResponse.from_orm(user)
    
    def update_user_profile(self, user: User, user_update: UserUpdate) -> UserResponse:
        """Update user profile information."""
        # Check if new email already exists
        if user_update.email and user_update.email != user.email:
            if self.user_repo.get_by_email(user_update.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
        
        updated_user = self.user_repo.update(user.id, user_update)
        return UserResponse.from_orm(updated_user)
    
    def get_user_detail(self, user_id: int) -> UserDetailResponse:
        """Get user details with application count."""
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        apps_count = len(user.applications)
        response = UserDetailResponse.from_orm(user)
        response.applications_count = apps_count
        
        return response
    
    # Company Profile Management
    def create_company_profile(self, current_user: User, profile_create: CompanyProfileCreate) -> CompanyProfileResponse:
        """Create company profile for hirer user."""
        if current_user.role.value != "HIRER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only users with HIRER role can create company profile"
            )
        
        if current_user.company_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a company profile"
            )
        
        company_profile = CompanyProfile(
            user_id=current_user.id,
            company_name=profile_create.company_name,
            company_description=profile_create.company_description,
            website=profile_create.website,
            industry=profile_create.industry
        )
        self.db.add(company_profile)
        self.db.commit()
        self.db.refresh(company_profile)
        
        return CompanyProfileResponse.from_orm(company_profile)
    
    def get_company_profile(self, current_user: User) -> CompanyProfileResponse:
        """Get current user's company profile."""
        if not current_user.company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )
        
        return CompanyProfileResponse.from_orm(current_user.company_profile)
    
    def update_company_profile(self, current_user: User, profile_update: CompanyProfileUpdate) -> CompanyProfileResponse:
        """Update current user's company profile."""
        if not current_user.company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )
        
        company_profile = current_user.company_profile
        
        if profile_update.company_name:
            company_profile.company_name = profile_update.company_name
        if profile_update.company_description is not None:
            company_profile.company_description = profile_update.company_description
        if profile_update.website is not None:
            company_profile.website = profile_update.website
        if profile_update.industry is not None:
            company_profile.industry = profile_update.industry
        
        self.db.commit()
        self.db.refresh(company_profile)
        
        return CompanyProfileResponse.from_orm(company_profile)
    
    def delete_company_profile(self, current_user: User) -> bool:
        """Delete current user's company profile."""
        if not current_user.company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )
        
        self.db.delete(current_user.company_profile)
        self.db.commit()
        return True
    
    # Applicant Profile Management
    def create_applicant_profile(self, current_user: User, profile_create: ApplicantProfileCreate) -> ApplicantProfileResponse:
        """Create applicant profile for regular user."""
        if current_user.role.value != "APPLICANT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only users with APPLICANT role can create applicant profile"
            )
        
        if current_user.applicant_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has an applicant profile"
            )
        
        applicant_profile = ApplicantProfile(
            user_id=current_user.id,
            bio=profile_create.bio,
            skills=profile_create.skills or [],
            years_of_experience=profile_create.years_of_experience or 0,
            resume_url=profile_create.resume_url,
            github_url=profile_create.github_url,
            linkedin_url=profile_create.linkedin_url
        )
        self.db.add(applicant_profile)
        self.db.commit()
        self.db.refresh(applicant_profile)
        
        return ApplicantProfileResponse.from_orm(applicant_profile)
    
    def get_applicant_profile(self, current_user: User) -> ApplicantProfileResponse:
        """Get current user's applicant profile."""
        if not current_user.applicant_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Applicant profile not found"
            )
        
        return ApplicantProfileResponse.from_orm(current_user.applicant_profile)
    
    def update_applicant_profile(self, current_user: User, profile_update: ApplicantProfileUpdate) -> ApplicantProfileResponse:
        """Update current user's applicant profile."""
        if not current_user.applicant_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Applicant profile not found"
            )
        
        applicant_profile = current_user.applicant_profile
        
        if profile_update.bio is not None:
            applicant_profile.bio = profile_update.bio
        if profile_update.skills is not None:
            applicant_profile.skills = profile_update.skills
        if profile_update.years_of_experience is not None:
            applicant_profile.years_of_experience = profile_update.years_of_experience
        if profile_update.resume_url is not None:
            applicant_profile.resume_url = profile_update.resume_url
        if profile_update.github_url is not None:
            applicant_profile.github_url = profile_update.github_url
        if profile_update.linkedin_url is not None:
            applicant_profile.linkedin_url = profile_update.linkedin_url
        
        self.db.commit()
        self.db.refresh(applicant_profile)
        
        return ApplicantProfileResponse.from_orm(applicant_profile)
    
    def delete_applicant_profile(self, current_user: User) -> bool:
        """Delete current user's applicant profile."""
        if not current_user.applicant_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Applicant profile not found"
            )
        
        self.db.delete(current_user.applicant_profile)
        self.db.commit()
        return True
