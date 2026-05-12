"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from app.models.user import User
from app.api.deps import get_user_service, get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, OTPVerify, UserMessageResponse, ResendOTPRequest
from app.schemas.token import TokenRequest, TokenResponse, TokenRefreshRequest
from app.core.security import SecurityUtility, verify_refresh_token
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **password**: Password with uppercase letter and digit (min 8 characters)
    - **full_name**: Optional full name
    """
    return user_service.register_user(user_create)

@router.post("/verify-otp", response_model=UserMessageResponse, status_code=status.HTTP_200_OK)
async def verify_otp(
    otp_verify: OTPVerify,
    user_service: UserService = Depends(get_user_service)
):
    """
    Verify user's OTP.
    
    - **otp**: 6-digit verification code
    """
    return user_service.verify_otp(otp_verify)

@router.post("/resend-otp", response_model=UserMessageResponse, status_code=status.HTTP_200_OK)
async def resend_otp(
    request: ResendOTPRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    Resend OTP to user's email.
    
    - **email**: User's email address
    """
    return user_service.resend_otp(request.email)

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: TokenRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    Login user and receive access and refresh tokens.
    
    - **email**: User's email
    - **password**: User's password
    """
    user = user_service.authenticate_user(credentials.email, credentials.password)
    return user_service.create_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: TokenRefreshRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    Generate a new access token using a refresh token.
    
    - **refresh_token**: Valid refresh token from login
    """
    return user_service.refresh_access_token(token_data.refresh_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Logout user by revoking all refresh tokens.
    Requires authentication.
    """
    user_service.logout_user(current_user)
    return {"message": "Successfully logged out"}
