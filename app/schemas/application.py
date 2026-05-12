"""
Pydantic schemas for job applications.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    """Schema for creating an application."""
    job_id: int = Field(..., description="Job ID to apply for")
    cover_letter: Optional[str] = Field(None, max_length=5000, description="Cover letter")
    resume_url: Optional[str] = Field(None, max_length=500, description="Resume URL")


class ApplicationUpdate(BaseModel):
    """Schema for updating an application."""
    status: Optional[str] = Field(None, description="Application status (admin only)")


class ApplicationResponse(BaseModel):
    """Schema for application response."""
    id: int
    applicant_id: int
    job_id: int
    company_id: int
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: str
    applied_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationDetailResponse(ApplicationResponse):
    """Detailed application response with applicant info."""
    pass


class PaginatedApplicationResponse(BaseModel):
    """Paginated application response."""
    total: int = Field(..., description="Total number of records")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Records per page")
    items: list[ApplicationResponse] = Field(..., description="List of applications")


class ApplicationFilterParams(BaseModel):
    """Schema for filtering applications."""
    job_id: Optional[int] = Field(None, description="Filter by job ID")
    status: Optional[str] = Field(None, description="Filter by status")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
