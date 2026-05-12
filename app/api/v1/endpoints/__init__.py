"""API endpoints."""

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.applications import router as applications_router
from app.api.v1.endpoints.jobs import router as jobs_router

__all__ = ["auth_router", "users_router", "applications_router", "jobs_router"]
