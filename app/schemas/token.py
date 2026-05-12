"""
Pydantic schemas for authentication tokens.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TokenRequest(BaseModel):
    """Schema for login request."""
    email: str = Field(..., description="email address")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class TokenRefreshRequest(BaseModel):
    """Schema for token refresh request."""
    refresh_token: str = Field(..., description="Refresh token")
