"""Schemas module."""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserDetailResponse,
    UserListResponse,
)
from app.schemas.token import TokenRequest, TokenResponse, TokenRefreshRequest
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationDetailResponse,
    PaginatedApplicationResponse,
    ApplicationFilterParams,
    ErrorResponse,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserDetailResponse",
    "UserListResponse",
    # Token schemas
    "TokenRequest",
    "TokenResponse",
    "TokenRefreshRequest",
    # Application schemas
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "ApplicationDetailResponse",
    "PaginatedApplicationResponse",
    "ApplicationFilterParams",
    "ErrorResponse",
]
