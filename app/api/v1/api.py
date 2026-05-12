"""
API v1 router - combines all v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth_router, users_router, applications_router, jobs_router

router = APIRouter(prefix="/api/v1")

# Include all endpoint routers
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(applications_router)
router.include_router(jobs_router)

__all__ = ["router"]
