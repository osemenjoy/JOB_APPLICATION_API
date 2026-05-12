"""
Database session management and initialization.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.settings import get_settings
from app.db.base import Base

settings = get_settings()

# Database engine configuration
engine_kwargs = {
    "echo": settings.sqlalchemy_echo,
    "pool_pre_ping": settings.sqlalchemy_pool_pre_ping,
}

# Use SQLite-specific settings if using SQLite
if "sqlite" in settings.database_url:
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    })
else:
    # Use standard pool for other databases (PostgreSQL, MySQL, etc.)
    engine_kwargs.update({
        "pool_size": settings.sqlalchemy_pool_size,
        "max_overflow": settings.sqlalchemy_max_overflow,
    })

# Create database engine
engine = create_engine(settings.database_url, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependency to get database session.
    
    Usage:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all tables. Use with caution!"""
    Base.metadata.drop_all(bind=engine)
