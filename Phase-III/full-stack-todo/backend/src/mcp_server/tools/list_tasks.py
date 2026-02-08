"""
MCP tool for listing tasks.
Implements the list_tasks functionality as an MCP-compliant tool.
"""
from typing import Dict, Any

from ..decorators import tool_handler, require_auth
from ..utils import validate_list_tasks_input, format_error_response
from ..adapters.task_adapter import TaskAdapter


async def list_tasks_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the list_tasks tool.

    Args:
        params: Dictionary containing task listing parameters

    Returns:
        Dictionary with success status and list of tasks or error
    """
    # Create adapter instance
    adapter = TaskAdapter()

    # Extract parameters with defaults
    status = params.get("status")
    limit = params.get("limit", 20)  # Default limit
    offset = params.get("offset", 0)  # Default offset
    sort_by = params.get("sort_by", "created_at")  # Default sort field
    order = params.get("order", "desc")  # Default sort order
    user_id = params.get("user_id", 1)  # Default user for testing

    try:
        # Get tasks using the adapter
        result = adapter.get_tasks(
            user_id=user_id,
            status=status,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order
        )

        # Return success response with tasks
        return {
            "success": True,
            "tasks": result["tasks"],
            "total_count": result["total_count"]
        }
    except Exception as e:
        return format_error_response(
            f"Failed to list tasks: {str(e)}",
            "TASK_LISTING_ERROR"
        )


@tool_handler(validate_list_tasks_input)
@require_auth
async def validated_list_tasks_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validated handler for the list_tasks tool that includes validation.
    """
    return await list_tasks_handler(params)


def get_list_tasks_tool():
    """
    Get the list_tasks tool definition.

    Returns:
        A function that can be used to create the actual tool when MCP SDK is available
    """
    # Define the arguments schema for the tool
    arguments_schema = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["all", "pending", "completed"],
                "default": "all",
                "description": "Filter by task status (optional, defaults to 'all')"
            },
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "default": 20,
                "description": "Maximum number of tasks to return (optional, defaults to 20)"
            },
            "offset": {
                "type": "integer",
                "minimum": 0,
                "default": 0,
                "description": "Offset for pagination (optional, defaults to 0)"
            },
            "sort_by": {
                "type": "string",
                "enum": ["created_at", "due_date", "priority", "title"],
                "default": "created_at",
                "description": "Field to sort by (optional, defaults to 'created_at')"
            },
            "order": {
                "type": "string",
                "enum": ["asc", "desc"],
                "default": "desc",
                "description": "Sort order (optional, defaults to 'desc')"
            }
        },
        "additionalProperties": False
    }

    # Return the tool definition that will be used by the server
    def create_tool():
        try:
            from mcp.types import Tool
            return Tool(
                name="list_tasks",
                description="List tasks in the todo system with optional filters",
                arguments_schema=arguments_schema
            )
        except ImportError:
            # Fallback for testing without MCP SDK
            return {
                "name": "list_tasks",
                "description": "List tasks in the todo system with optional filters",
                "arguments_schema": arguments_schema,
                "handler": validated_list_tasks_handler
            }

    return create_tool


# Export the validated handler for use in tests
__all__ = ['get_list_tasks_tool', 'list_tasks_handler', 'validated_list_tasks_handler']