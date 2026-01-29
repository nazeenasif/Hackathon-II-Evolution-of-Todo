from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from src.core.auth import get_user_from_token
from src.models.user import UserRead


# HTTP Bearer token scheme for authentication
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Dependency to get the current authenticated user from the JWT token.
    """
    token = credentials.credentials

    try:
        user_info = get_user_from_token(token)
        return user_info
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Dependency to get the current authenticated user's ID from the JWT token.
    """
    token = credentials.credentials

    try:
        user_info = get_user_from_token(token)
        return user_info["user_id"]
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_user_owns_resource(user_id: int, requested_user_id: int) -> bool:
    """
    Verify that the authenticated user owns the requested resource.
    Returns True if user_id matches requested_user_id, False otherwise.
    """
    return user_id == requested_user_id


def require_same_user_id(user_id: int, requested_user_id: int):
    """
    Dependency to ensure the authenticated user can only access their own resources.
    Raises HTTPException if the user_id doesn't match the requested_user_id.
    """
    if not verify_user_owns_resource(user_id, requested_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )