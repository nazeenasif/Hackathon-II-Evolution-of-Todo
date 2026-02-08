"""
MCP tool for updating tasks.
Implements the update_task functionality as an MCP-compliant tool.
"""
from typing import Dict, Any

from ..decorators import tool_handler, require_auth
from ..utils import validate_update_task_input, format_error_response
from ..adapters.task_adapter import TaskAdapter


async def update_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the update_task tool.

    Args:
        params: Dictionary containing task update parameters

    Returns:
        Dictionary with success status and updated task ID or error
    """
    # Create adapter instance
    adapter = TaskAdapter()

    # Extract parameters
    task_id = params["task_id"]  # Required, so we can safely access it
    title = params.get("title")
    description = params.get("description")
    due_date = params.get("due_date")
    priority = params.get("priority")
    tags = params.get("tags")
    user_id = params.get("user_id", 1)  # Default user for testing

    try:
        # Update the task using the adapter
        result = adapter.update_task(
            task_id=task_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            tags=tags,
            user_id=user_id
        )

        if result is None:
            return format_error_response(
                f"Task with ID {task_id} not found or not owned by user",
                "TASK_NOT_FOUND"
            )

        # Return success response with task ID
        return {
            "success": True,
            "task_id": result["id"]
        }
    except Exception as e:
        return format_error_response(
            f"Failed to update task: {str(e)}",
            "TASK_UPDATE_ERROR"
        )


@tool_handler(validate_update_task_input)
@require_auth
async def validated_update_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validated handler for the update_task tool that includes validation.
    """
    return await update_task_handler(params)


def get_update_task_tool():
    """
    Get the update_task tool definition.

    Returns:
        A function that can be used to create the actual tool when MCP SDK is available
    """
    # Define the arguments schema for the tool
    arguments_schema = {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "minimum": 1,
                "description": "Task ID (required)"
            },
            "title": {
                "type": "string",
                "description": "New task title (optional)",
                "maxLength": 255
            },
            "description": {
                "type": "string",
                "description": "New task description (optional)",
                "maxLength": 1000
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "New due date in ISO 8601 format (optional)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "New priority level (optional)"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "maxItems": 10,
                "description": "New task tags (optional)"
            }
        },
        "required": ["task_id"],
        "additionalProperties": False
    }

    # Return the tool definition that will be used by the server
    def create_tool():
        try:
            from mcp.types import Tool
            return Tool(
                name="update_task",
                description="Update an existing task in the todo system",
                arguments_schema=arguments_schema
            )
        except ImportError:
            # Fallback for testing without MCP SDK
            return {
                "name": "update_task",
                "description": "Update an existing task in the todo system",
                "arguments_schema": arguments_schema,
                "handler": validated_update_task_handler
            }

    return create_tool


# Export the validated handler for use in tests
__all__ = ['get_update_task_tool', 'update_task_handler', 'validated_update_task_handler']