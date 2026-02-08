"""
Utilities for MCP tools including validation, error handling, and response formatting.
Provides consistent behavior across all tools.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import re


def validate_add_task_input(params: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate input for add_task tool.

    Returns dict with errors if validation fails, empty dict if valid.
    """
    errors = []

    # Title is required
    if "title" not in params or not params["title"]:
        errors.append("title is required and cannot be empty")
    elif not isinstance(params["title"], str):
        errors.append("title must be a string")
    elif len(params["title"]) > 255:
        errors.append("title must be 255 characters or less")

    # Description validation
    if "description" in params and params["description"] is not None:
        if not isinstance(params["description"], str):
            errors.append("description must be a string")
        elif len(params["description"]) > 1000:
            errors.append("description must be 1000 characters or less")

    # Due date validation
    if "due_date" in params and params["due_date"] is not None:
        if not isinstance(params["due_date"], str):
            errors.append("due_date must be a string in ISO 8601 format")
        else:
            try:
                # Try to parse the date to validate format
                datetime.fromisoformat(params["due_date"].replace('Z', '+00:00'))
            except ValueError:
                errors.append("due_date must be in ISO 8601 format")

    # Priority validation
    if "priority" in params and params["priority"] is not None:
        if params["priority"] not in ["low", "medium", "high"]:
            errors.append("priority must be one of: low, medium, high")

    # Tags validation
    if "tags" in params and params["tags"] is not None:
        if not isinstance(params["tags"], list):
            errors.append("tags must be a list of strings")
        else:
            for i, tag in enumerate(params["tags"]):
                if not isinstance(tag, str):
                    errors.append(f"tag at index {i} must be a string")
            if len(params["tags"]) > 10:
                errors.append("cannot have more than 10 tags")

    return {"errors": errors}


def validate_list_tasks_input(params: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate input for list_tasks tool.

    Returns dict with errors if validation fails, empty dict if valid.
    """
    errors = []

    # Status validation
    if "status" in params and params["status"] is not None:
        if params["status"] not in ["all", "pending", "completed"]:
            errors.append("status must be one of: all, pending, completed")

    # Limit validation
    if "limit" in params and params["limit"] is not None:
        if not isinstance(params["limit"], int) or params["limit"] < 1 or params["limit"] > 100:
            errors.append("limit must be an integer between 1 and 100")

    # Offset validation
    if "offset" in params and params["offset"] is not None:
        if not isinstance(params["offset"], int) or params["offset"] < 0:
            errors.append("offset must be a non-negative integer")

    # Sort by validation
    if "sort_by" in params and params["sort_by"] is not None:
        if params["sort_by"] not in ["created_at", "due_date", "priority", "title"]:
            errors.append("sort_by must be one of: created_at, due_date, priority, title")

    # Order validation
    if "order" in params and params["order"] is not None:
        if params["order"] not in ["asc", "desc"]:
            errors.append("order must be one of: asc, desc")

    return {"errors": errors}


def validate_update_task_input(params: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate input for update_task tool.

    Returns dict with errors if validation fails, empty dict if valid.
    """
    errors = []

    # Task ID is required
    if "task_id" not in params:
        errors.append("task_id is required")
    elif not isinstance(params["task_id"], int) or params["task_id"] < 1:
        errors.append("task_id must be a positive integer")

    # Title validation (if provided)
    if "title" in params and params["title"] is not None:
        if not isinstance(params["title"], str):
            errors.append("title must be a string")
        elif len(params["title"]) > 255:
            errors.append("title must be 255 characters or less")

    # Description validation
    if "description" in params and params["description"] is not None:
        if not isinstance(params["description"], str):
            errors.append("description must be a string")
        elif len(params["description"]) > 1000:
            errors.append("description must be 1000 characters or less")

    # Due date validation
    if "due_date" in params and params["due_date"] is not None:
        if not isinstance(params["due_date"], str):
            errors.append("due_date must be a string in ISO 8601 format")
        else:
            try:
                datetime.fromisoformat(params["due_date"].replace('Z', '+00:00'))
            except ValueError:
                errors.append("due_date must be in ISO 8601 format")

    # Priority validation
    if "priority" in params and params["priority"] is not None:
        if params["priority"] not in ["low", "medium", "high"]:
            errors.append("priority must be one of: low, medium, high")

    # Tags validation
    if "tags" in params and params["tags"] is not None:
        if not isinstance(params["tags"], list):
            errors.append("tags must be a list of strings")
        else:
            for i, tag in enumerate(params["tags"]):
                if not isinstance(tag, str):
                    errors.append(f"tag at index {i} must be a string")
            if len(params["tags"]) > 10:
                errors.append("cannot have more than 10 tags")

    return {"errors": errors}


def validate_task_id_input(params: Dict[str, Any], param_name: str = "task_id") -> Dict[str, List[str]]:
    """
    Validate input for tools that require a task_id.

    Returns dict with errors if validation fails, empty dict if valid.
    """
    errors = []

    # Task ID is required
    if param_name not in params:
        errors.append(f"{param_name} is required")
    elif not isinstance(params[param_name], int) or params[param_name] < 1:
        errors.append(f"{param_name} must be a positive integer")

    return {"errors": errors}


def validate_required_fields(params: Dict[str, Any], required_fields: List[str]) -> Dict[str, List[str]]:
    """
    Validate that required fields are present in params.

    Returns dict with errors if validation fails, empty dict if valid.
    """
    errors = []

    for field in required_fields:
        if field not in params:
            errors.append(f"{field} is required")

    return {"errors": errors}


def format_success_response(data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Format a successful response for MCP tools.
    """
    response = {"success": True}
    if data:
        response.update(data)
    return response


def format_error_response(error_msg: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Format an error response for MCP tools.
    """
    response = {
        "success": False,
        "error": error_msg
    }
    if error_code:
        response["error_code"] = error_code
    if details:
        response["details"] = details
    return response


def handle_validation_errors(validation_result: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
    """
    Handle validation errors and return formatted error response if validation failed.
    Returns None if validation passed.
    """
    if validation_result and "errors" in validation_result and validation_result["errors"]:
        error_msg = "; ".join(validation_result["errors"])
        return format_error_response(error_msg, "VALIDATION_ERROR")
    return None