"""
Pydantic schemas for job postings.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class JobBase(BaseModel):
    """Base job schema."""
    title: str = Field(..., min_length=3, max_length=255, description="Job title")
    description: str = Field(..., min_length=10, description="Job description")
    required_skills: List[str] = Field(default=[], description="List of required skills")
    location: str = Field(..., min_length=2, max_length=255, description="Job location")
    salary_range: Optional[str] = Field(None, max_length=100, description="Salary range (e.g., $50k-$80k)")
    employment_type: str = Field(..., description="Employment type: FULL_TIME, PART_TIME, CONTRACT, FREELANCE")
    status: bool = Field(default=True, description="Job status (True=active, False=inactive)")


class JobCreate(JobBase):
    """Schema for creating a new job."""
    pass


class JobUpdate(BaseModel):
    """Schema for updating a job."""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    required_skills: Optional[List[str]] = None
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    salary_range: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = None
    status: Optional[bool] = None


class JobResponse(JobBase):
    """Schema for job response."""
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """List of jobs with pagination."""
    total: int
    skip: int
    limit: int
    items: List[JobResponse]
