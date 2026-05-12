"""
Settings and configuration using Pydantic settings.
Environment variables are loaded from .env file.
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    
    # API Configuration
    api_title: str = "Job Application API"
    api_version: str = "1.0.0"
    api_description: str = "A REST API for managing job applications with authentication"
    
    # Database Configuration
    database_url: str = "sqlite:///./job_applications.db"
    
    # SQLAlchemy Configuration
    sqlalchemy_echo: bool = False
    sqlalchemy_pool_pre_ping: bool = True
    sqlalchemy_pool_size: int = 10
    sqlalchemy_max_overflow: int = 20
    
    # JWT Configuration
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Password Configuration
    password_min_length: int = 8
    password_require_uppercase: bool = True
    password_require_digits: bool = True
    password_require_special: bool = False
    
    # Logging Configuration
    log_level: str = "INFO"
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Validation
    min_experience_years: int = 0
    max_experience_years: int = 70
    min_name_length: int = 2
    max_name_length: int = 100
    min_username_length: int = 3
    max_username_length: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
