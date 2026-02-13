"""
MCP tool for adding tasks.
Implements the add_task functionality as an MCP-compliant tool.
"""
from typing import Dict, Any

from ..decorators import tool_handler, require_auth
from ..utils import validate_add_task_input
from ..adapters.task_adapter import TaskAdapter


async def add_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the add_task tool.

    Args:
        params: Dictionary containing task creation parameters

    Returns:
        Dictionary with success status and task ID or error
    """
    # Create adapter instance
    adapter = TaskAdapter()

    # Extract parameters with defaults
    title = params.get("title")
    description = params.get("description")
    due_date = params.get("due_date")
    priority = params.get("priority", "medium")  # Default to medium priority
    tags = params.get("tags")
    user_id = params.get("user_id", 1)  # Default user for testing

    try:
        # Create the task using the adapter
        result = adapter.create_task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            tags=tags,
            user_id=user_id
        )

        # Return success response with task ID
        return {
            "success": True,
            "task_id": result["id"]
        }
    except Exception as e:
        from ..utils import format_error_response
        return format_error_response(
            f"Failed to create task: {str(e)}",
            "TASK_CREATION_ERROR"
        )


@tool_handler(validate_add_task_input)
@require_auth
async def validated_add_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validated handler for the add_task tool that includes validation.
    """
    return await add_task_handler(params)


def get_add_task_tool():
    """
    Get the add_task tool definition.

    Returns:
        A function that can be used to create the actual tool when MCP SDK is available
    """
    # Define the arguments schema for the tool
    arguments_schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Task title (required)",
                "minLength": 1,
                "maxLength": 255
            },
            "description": {
                "type": "string",
                "description": "Task description (optional)",
                "maxLength": 1000
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "Due date in ISO 8601 format (optional)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "default": "medium",
                "description": "Priority level (optional, defaults to 'medium')"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "maxItems": 10,
                "description": "Task tags (optional)"
            }
        },
        "required": ["title"],
        "additionalProperties": False
    }

    # Return the tool definition that will be used by the server
    def create_tool():
        try:
            from mcp.types import Tool
            return Tool(
                name="add_task",
                description="Create a new task in the todo system",
                arguments_schema=arguments_schema
            )
        except ImportError:
            # Fallback for testing without MCP SDK
            return {
                "name": "add_task",
                "description": "Create a new task in the todo system",
                "arguments_schema": arguments_schema,
                "handler": validated_add_task_handler
            }

    return create_tool


# Export the validated handler for use in tests
__all__ = ['get_add_task_tool', 'add_task_handler', 'validated_add_task_handler']