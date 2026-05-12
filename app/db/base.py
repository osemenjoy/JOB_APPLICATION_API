"""
Database base class for all models.
"""

from sqlalchemy.orm import declarative_base

# Create the declarative base for all models
Base = declarative_base()
