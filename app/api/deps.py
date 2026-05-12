"""
Dependency injection for API endpoints.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import User
from app.services.user_service import UserService
from app.services.application_service import ApplicationService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Get user service instance."""
    return UserService(db)


def get_application_service(db: Session = Depends(get_db)) -> ApplicationService:
    """Get application service instance."""
    return ApplicationService(db)


# Re-export security dependencies for convenience
__all__ = [
    "get_db",
    "get_current_user",
    "get_current_admin_user",
    "get_user_service",
    "get_application_service",
]
