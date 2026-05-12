"""API module."""

from app.api.v1 import router as v1_router
from app.api import deps

__all__ = ["v1_router", "deps"]
