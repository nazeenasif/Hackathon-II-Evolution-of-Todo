from fastapi import APIRouter, HTTPException, Depends, status
from datetime import timedelta
from sqlmodel import Session

from src.models.user import UserCreate, UserLogin, UserRead
from src.services.user_service import UserService
from src.core.database import get_async_session
from src.core.auth_utils import create_access_token
from src.core.config import settings

router = APIRouter()


@router.post("/auth/signup")
def signup(user_data: UserCreate, session: Session = Depends(get_async_session)):
    """
    Register a new user account and return JWT token.
    """
    # Check if user with this email already exists
    existing_user = UserService.get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Check if user with this username already exists
    existing_username = UserService.get_user_by_username(session, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists"
        )

    # Create the new user
    user = UserService.create_user(session, user_data)

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }


@router.post("/auth/signin")
def signin(user_credentials: UserLogin, session: Session = Depends(get_async_session)):
    """
    Authenticate user and return JWT token.
    """
    user = UserService.authenticate_user(
        session,
        user_credentials.email,
        user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }