from typing import Any, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    """
    Standardized API response format.
    """
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None


def create_success_response(data: Any = None, message: str = "Request successful") -> APIResponse:
    """
    Create a standardized success response.
    """
    return APIResponse(success=True, data=data, message=message)


def create_error_response(error: str, message: str = "Request failed") -> APIResponse:
    """
    Create a standardized error response.
    """
    return APIResponse(success=False, error=error, message=message)