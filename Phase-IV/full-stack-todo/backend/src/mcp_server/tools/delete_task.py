"""
MCP tool for deleting tasks.
Implements the delete_task functionality as an MCP-compliant tool.
"""
from typing import Dict, Any

from ..decorators import tool_handler, require_auth
from ..utils import validate_task_id_input, format_error_response
from ..adapters.task_adapter import TaskAdapter


async def delete_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the delete_task tool.

    Args:
        params: Dictionary containing task deletion parameters

    Returns:
        Dictionary with success status and task ID or error
    """
    # Create adapter instance
    adapter = TaskAdapter()

    # Extract parameters
    task_id = params["task_id"]  # Required, so we can safely access it
    user_id = params.get("user_id", 1)  # Default user for testing

    try:
        # Delete the task using the adapter
        success = adapter.delete_task(
            task_id=task_id,
            user_id=user_id
        )

        if not success:
            return format_error_response(
                f"Task with ID {task_id} not found or not owned by user",
                "TASK_NOT_FOUND"
            )

        # Return success response
        return {
            "success": True,
            "task_id": task_id
        }
    except Exception as e:
        return format_error_response(
            f"Failed to delete task: {str(e)}",
            "TASK_DELETION_ERROR"
        )


@tool_handler(lambda params: validate_task_id_input(params))
@require_auth
async def validated_delete_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validated handler for the delete_task tool that includes validation.
    """
    return await delete_task_handler(params)


def get_delete_task_tool():
    """
    Get the delete_task tool definition.

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
                "description": "Task ID to delete (required)"
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
                name="delete_task",
                description="Delete a task from the todo system",
                arguments_schema=arguments_schema
            )
        except ImportError:
            # Fallback for testing without MCP SDK
            return {
                "name": "delete_task",
                "description": "Delete a task from the todo system",
                "arguments_schema": arguments_schema,
                "handler": validated_delete_task_handler
            }

    return create_tool


# Export the validated handler for use in tests
__all__ = ['get_delete_task_tool', 'delete_task_handler', 'validated_delete_task_handler']