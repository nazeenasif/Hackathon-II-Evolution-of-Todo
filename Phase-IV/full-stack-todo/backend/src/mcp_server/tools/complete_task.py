"""
MCP tool for completing tasks.
Implements the complete_task functionality as an MCP-compliant tool.
"""
from typing import Dict, Any

from ..decorators import tool_handler, require_auth
from ..utils import validate_task_id_input, format_error_response
from ..adapters.task_adapter import TaskAdapter


async def complete_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the complete_task tool.

    Args:
        params: Dictionary containing task completion parameters

    Returns:
        Dictionary with success status and completed task ID or error
    """
    # Create adapter instance
    adapter = TaskAdapter()

    # Extract parameters
    task_id = params["task_id"]  # Required, so we can safely access it
    user_id = params.get("user_id", 1)  # Default user for testing

    try:
        # Complete the task using the adapter
        result = adapter.complete_task(
            task_id=task_id,
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
            f"Failed to complete task: {str(e)}",
            "TASK_COMPLETION_ERROR"
        )


@tool_handler(lambda params: validate_task_id_input(params))
@require_auth
async def validated_complete_task_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validated handler for the complete_task tool that includes validation.
    """
    return await complete_task_handler(params)


def get_complete_task_tool():
    """
    Get the complete_task tool definition.

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
                "description": "Task ID to complete (required)"
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
                name="complete_task",
                description="Mark a task as completed in the todo system",
                arguments_schema=arguments_schema
            )
        except ImportError:
            # Fallback for testing without MCP SDK
            return {
                "name": "complete_task",
                "description": "Mark a task as completed in the todo system",
                "arguments_schema": arguments_schema,
                "handler": validated_complete_task_handler
            }

    return create_tool


# Export the validated handler for use in tests
__all__ = ['get_complete_task_tool', 'complete_task_handler', 'validated_complete_task_handler']