"""
Decorators for consistent MCP tool implementation.
Provides common patterns for validation, error handling, and response formatting.
"""
from functools import wraps
from typing import Callable, Any, Dict, Awaitable

from .utils import handle_validation_errors, format_error_response


def tool_handler(validate_func: Callable[[Dict[str, Any]], Dict[str, Any]]):
    """
    Decorator for MCP tool handlers that provides:
    - Input validation using the specified validation function
    - Error handling
    - Consistent response formatting
    """
    def decorator(func: Callable[..., Awaitable[Dict[str, Any]]]):
        @wraps(func)
        async def wrapper(params: Dict[str, Any]) -> Dict[str, Any]:
            # First, validate the input
            validation_result = validate_func(params)
            validation_error = handle_validation_errors(validation_result)

            if validation_error:
                return validation_error

            try:
                # Call the actual handler function
                result = await func(params)

                # If result is already formatted (contains 'success' key), return as-is
                if isinstance(result, dict) and 'success' in result:
                    return result

                # Otherwise, wrap the result in a success response
                return {
                    "success": True,
                    **result
                }

            except Exception as e:
                # Handle unexpected errors
                return format_error_response(
                    f"An unexpected error occurred: {str(e)}",
                    "INTERNAL_ERROR",
                    {"exception_type": type(e).__name__}
                )

        return wrapper
    return decorator


def require_auth(func: Callable[..., Awaitable[Dict[str, Any]]]):
    """
    Decorator to require authentication for MCP tools.
    Currently a placeholder - would extract user identity from context in real implementation.
    """
    @wraps(func)
    async def wrapper(params: Dict[str, Any]) -> Dict[str, Any]:
        # In a real implementation, this would extract user identity from context
        # For now, we'll use a default user_id for testing purposes
        if "user_id" not in params:
            params = params.copy()  # Don't modify original
            params["user_id"] = 1  # Default user for testing

        return await func(params)

    return wrapper