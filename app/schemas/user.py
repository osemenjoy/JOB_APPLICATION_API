"""
Pydantic schemas for user authentication and management.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Full name")
    role: Optional[str] = Field("APPLICANT", description="User role (APPLICANT or HIRER)")


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=72, description="Password (min 8, max 72 characters)")
    
    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) > 72:
            raise ValueError("Password must be 72 characters or less (bcrypt limit)")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        return v
    
class OTPVerify(BaseModel):
    """Schema for OTP verification."""
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")
    email : EmailStr = Field(..., description="User email address")


class ResendOTPRequest(BaseModel):
    """Schema for resending OTP."""
    email: EmailStr = Field(..., description="User email address")


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    verification_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response with applications count."""
    applications_count: Optional[int] = 0


class UserListResponse(BaseModel):
    """List of users with pagination."""
    total: int
    skip: int
    limit: int
    items: list[UserResponse]


class MessageResponse(BaseModel):
    """Generic response with message and data."""
    message: str = Field(..., description="Response message")
    data: Optional[dict] = Field(None, description="Response data")


class UserMessageResponse(BaseModel):
    """Response with message and user data."""
    message: str = Field(..., description="Response message")
    user: UserResponse = Field(..., description="User data")


class CompanyProfileBase(BaseModel):
    """Base company profile schema."""
    company_name: str = Field(..., min_length=2, max_length=255, description="Company name")
    company_description: Optional[str] = Field(None, description="Company description")
    website: Optional[str] = Field(None, max_length=500, description="Company website")
    industry: Optional[str] = Field(None, max_length=100, description="Industry type")


class CompanyProfileCreate(CompanyProfileBase):
    """Schema for creating company profile."""
    pass


class CompanyProfileUpdate(BaseModel):
    """Schema for updating company profile."""
    company_name: Optional[str] = Field(None, min_length=2, max_length=255)
    company_description: Optional[str] = None
    website: Optional[str] = Field(None, max_length=500)
    industry: Optional[str] = Field(None, max_length=100)


class CompanyProfileResponse(CompanyProfileBase):
    """Schema for company profile response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicantProfileBase(BaseModel):
    """Base applicant profile schema."""
    bio: Optional[str] = Field(None, description="Applicant bio/about")
    skills: Optional[list[str]] = Field(default_factory=list, description="List of skills")
    years_of_experience: Optional[int] = Field(0, ge=0, description="Years of experience")
    resume_url: Optional[str] = Field(None, max_length=500, description="Resume URL")
    github_url: Optional[str] = Field(None, max_length=500, description="GitHub profile URL")
    linkedin_url: Optional[str] = Field(None, max_length=500, description="LinkedIn profile URL")


class ApplicantProfileCreate(ApplicantProfileBase):
    """Schema for creating applicant profile."""
    pass


class ApplicantProfileUpdate(BaseModel):
    """Schema for updating applicant profile."""
    bio: Optional[str] = None
    skills: Optional[list[str]] = None
    years_of_experience: Optional[int] = Field(None, ge=0)
    resume_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    linkedin_url: Optional[str] = Field(None, max_length=500)


class ApplicantProfileResponse(ApplicantProfileBase):
    """Schema for applicant profile response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

