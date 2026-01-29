from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from src.core.config import settings
from src.models.user import UserRead


def verify_token(token: str) -> dict:
    """
    Verify a JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_from_token(token: str) -> dict:
    """
    Extract user information from a JWT token.
    """
    payload = verify_token(token)

    # Extract user information from the token
    user_id: int = payload.get("sub")
    email: str = payload.get("email")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user_id": user_id, "email": email}


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired.
    """
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        exp_timestamp = payload.get("exp")

        if exp_timestamp is None:
            return True

        return datetime.fromtimestamp(exp_timestamp) < datetime.utcnow()
    except JWTError:
        return True