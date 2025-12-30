"""
Input validation utilities for the In-Memory Python Console Todo Application.

This module provides functions to validate user inputs according to the
requirements specified in the feature specification.
"""
from typing import Union


def validate_task_title(title: str) -> bool:
    """
    Validate that the task title is a non-empty string.

    Args:
        title (str): The title to validate

    Returns:
        bool: True if the title is valid, False otherwise
    """
    if not isinstance(title, str):
        return False
    return len(title.strip()) > 0


def validate_task_description(description: str) -> bool:
    """
    Validate that the task description is a string (can be empty).

    Args:
        description (str): The description to validate

    Returns:
        bool: True if the description is valid, False otherwise
    """
    return isinstance(description, str)


def validate_task_id(task_id: Union[str, int]) -> bool:
    """
    Validate that the task ID is a positive integer.

    Args:
        task_id (Union[str, int]): The task ID to validate

    Returns:
        bool: True if the task ID is valid, False otherwise
    """
    try:
        if isinstance(task_id, str):
            task_id = int(task_id)
        return isinstance(task_id, int) and task_id > 0
    except ValueError:
        return False


def validate_task_status(status: str) -> bool:
    """
    Validate that the task status is either "Complete" or "Incomplete".

    Args:
        status (str): The status to validate

    Returns:
        bool: True if the status is valid, False otherwise
    """
    return status in ["Complete", "Incomplete"]


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input by stripping leading/trailing whitespace.

    Args:
        user_input (str): The input to sanitize

    Returns:
        str: The sanitized input
    """
    if not isinstance(user_input, str):
        return ""
    return user_input.strip()
from typing import Union


def validate_task_title(title: str) -> bool:
    """
    Validate that the task title is a non-empty string.

    Args:
        title (str): The title to validate

    Returns:
        bool: True if the title is valid, False otherwise
    """
    if not isinstance(title, str):
        return False
    return len(title.strip()) > 0


def validate_task_description(description: str) -> bool:
    """
    Validate that the task description is a string (can be empty).

    Args:
        description (str): The description to validate

    Returns:
        bool: True if the description is valid, False otherwise
    """
    return isinstance(description, str)


def validate_task_id(task_id: Union[str, int]) -> bool:
    """
    Validate that the task ID is a positive integer.

    Args:
        task_id (Union[str, int]): The task ID to validate

    Returns:
        bool: True if the task ID is valid, False otherwise
    """
    try:
        if isinstance(task_id, str):
            task_id = int(task_id)
        return isinstance(task_id, int) and task_id > 0
    except ValueError:
        return False


def validate_task_status(status: str) -> bool:
    """
    Validate that the task status is either "Complete" or "Incomplete".

    Args:
        status (str): The status to validate

    Returns:
        bool: True if the status is valid, False otherwise
    """
    return status in ["Complete", "Incomplete"]


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input by stripping leading/trailing whitespace.

    Args:
        user_input (str): The input to sanitize

    Returns:
        str: The sanitized input
    """
    if not isinstance(user_input, str):
        return ""
    return user_input.strip()