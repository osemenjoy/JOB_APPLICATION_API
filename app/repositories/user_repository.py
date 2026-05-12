"""
Repository for user data access.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
import random

from app.models.user import User, RefreshToken
from app.schemas.user import UserCreate, UserUpdate



class UserRepository:
    """Repository for user data access operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def verification_code_generator(self) -> str:
        """Generate a random 6-digit verification code."""
        return f"{random.randint(100000, 999999)}"

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
        """Create a new user."""
        db_user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            verification_code=self.verification_code_generator(),
            verification_code_expires_at=datetime.utcnow() + timedelta(minutes=10),
            is_active=False,
            role=user_create.role if hasattr(user_create, "role") else "APPLICANT"
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 10) -> tuple[int, List[User]]:
        """Get all users with pagination."""
        total = self.db.query(User).count()
        users = self.db.query(User).offset(skip).limit(limit).all()
        return total, users
    
    def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        db_user = self.get_by_id(user_id)
        if db_user:
            if user_update.full_name is not None:
                db_user.full_name = user_update.full_name
            if user_update.email is not None:
                db_user.email = user_update.email
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        """Delete a user."""
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
    
    def deactivate(self, user_id: int) -> Optional[User]:
        """Deactivate a user account."""
        db_user = self.get_by_id(user_id)
        if db_user:
            db_user.is_active = False
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def get_by_verification_code(self, code: str) -> Optional[User]:
        """Get user by verification code."""
        return self.db.query(User).filter(User.verification_code == code).first()

class RefreshTokenRepository:
    """Repository for refresh token data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, token: str, expires_at) -> RefreshToken:
        """Create a new refresh token."""
        db_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        return db_token
    
    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get refresh token by token string."""
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
    
    def get_user_tokens(self, user_id: int) -> List[RefreshToken]:
        """Get all refresh tokens for a user."""
        return self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).all()
    
    def revoke(self, token_id: int) -> Optional[RefreshToken]:
        """Revoke a refresh token."""
        db_token = self.db.query(RefreshToken).filter(RefreshToken.id == token_id).first()
        if db_token:
            db_token.is_revoked = True
            self.db.commit()
            self.db.refresh(db_token)
        return db_token
    
    def revoke_all_user_tokens(self, user_id: int) -> int:
        """Revoke all tokens for a user."""
        count = self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).update({RefreshToken.is_revoked: True})
        self.db.commit()
        return count
    
    def delete(self, token_id: int) -> bool:
        """Delete a refresh token."""
        db_token = self.db.query(RefreshToken).filter(RefreshToken.id == token_id).first()
        if db_token:
            self.db.delete(db_token)
            self.db.commit()
            return True
        return False
