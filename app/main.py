"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core import get_settings
from app.core.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.api.v1 import router as v1_router
from app.db.session import init_db
from app.middleware.logging import logging_middleware


# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Add logging middleware
app.middleware("http")(logging_middleware)

# Include v1 API router
app.include_router(v1_router)


# ==================== Startup and Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()
    print(f"✓ {settings.api_title} v{settings.api_version} started")
    print(f"✓ Database initialized")
    print(f"✓ API Documentation: http://{settings.host}:{settings.port}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    print(f"✓ {settings.api_title} shutdown complete")


# ==================== Root Endpoint ====================

@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint with API information and available endpoints.
    """
    return {
        "message": f"Welcome to {settings.api_title}",
        "version": settings.api_version,
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "authentication": {
                "register": "POST /api/v1/auth/register",
                "login": "POST /api/v1/auth/login",
                "refresh_token": "POST /api/v1/auth/refresh",
                "logout": "POST /api/v1/auth/logout",
            },
            "users": {
                "get_profile": "GET /api/v1/users/profile",
                "update_profile": "PUT /api/v1/users/profile",
                "list_users": "GET /api/v1/users/",
                "get_user": "GET /api/v1/users/{user_id}",
                "update_user": "PUT /api/v1/users/{user_id}",
                "delete_user": "DELETE /api/v1/users/{user_id}",
            },
            "applications": {
                "submit": "POST /api/v1/applications/",
                "get_my_applications": "GET /api/v1/applications/",
                "get_application": "GET /api/v1/applications/{application_id}",
                "update_application": "PUT /api/v1/applications/{application_id}",
                "delete_application": "DELETE /api/v1/applications/{application_id}",
                "filter_by_skill": "GET /api/v1/applications/filter/skill",
                "search": "GET /api/v1/applications/filter/search",
                "admin_all": "GET /api/v1/applications/admin/all",
                "admin_get": "GET /api/v1/applications/admin/{application_id}",
                "admin_update": "PUT /api/v1/applications/admin/{application_id}",
                "admin_delete": "DELETE /api/v1/applications/admin/{application_id}",
            }
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.api_title,
        "version": settings.api_version
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
