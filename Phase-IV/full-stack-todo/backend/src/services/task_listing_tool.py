import json
from typing import Dict, Any, List
from .task_service import TaskService
from ..models.task import PriorityEnum
from sqlmodel import Session
from ..core.database import get_async_session


class TaskListingTool:
    """
    MCP tool for listing tasks based on various criteria.
    """

    @staticmethod
    def get_name() -> str:
        """
        Get the name of the tool.
        """
        return "list_tasks"

    @staticmethod
    def get_description() -> str:
        """
        Get the description of the tool for AI agent.
        """
        return "List tasks with optional filtering by completion status, priority, tags, or search terms"

    @staticmethod
    def get_parameters() -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.
        """
        return {
            "type": "object",
            "properties": {
                "completed": {
                    "type": "boolean",
                    "description": "Filter by completion status (true for completed, false for pending)"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Filter by priority level"
                },
                "tag": {
                    "type": "string",
                    "description": "Filter by specific tag"
                },
                "search": {
                    "type": "string",
                    "description": "Search term for title or description"
                },
                "sort_by": {
                    "type": "string",
                    "enum": ["due_date", "priority", "title"],
                    "description": "Field to sort by",
                    "default": "due_date"
                },
                "order": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Sort order",
                    "default": "asc"
                }
            },
            "description": "Parameters for filtering and sorting the task list"
        }

    @staticmethod
    def execute(user_id: int, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the task listing with the provided arguments.

        Args:
            user_id: ID of the user listing the tasks
            arguments: Dictionary containing listing parameters

        Returns:
            Dictionary with result of the operation
        """
        from src.core.database import engine
        from sqlmodel import Session
        from ..models.task import PriorityEnum

        try:
            # Extract parameters from arguments
            completed = arguments.get("completed")
            priority = arguments.get("priority")
            tag = arguments.get("tag")
            search = arguments.get("search")
            sort_by = arguments.get("sort_by", "due_date")
            order = arguments.get("order", "asc")

            # Create database session using engine directly
            with Session(engine) as session:
                # Use the existing TaskService to get tasks
                tasks = TaskService.get_tasks(
                    session=session,
                    user_id=user_id,
                    completed=completed,
                    priority=PriorityEnum(priority) if priority else None,
                    tag=tag,
                    search=search,
                    sort_by=sort_by,
                    order=order
                )

                # Convert tasks to a simplified representation
                task_list = []
                for task in tasks:
                    task_dict = {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "priority": task.priority.value,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "tags": task.tags,
                        "created_at": task.created_at.isoformat()
                    }
                    task_list.append(task_dict)

                # Return success result
                return {
                    "success": True,
                    "count": len(task_list),
                    "tasks": task_list,
                    "message": f"Found {len(task_list)} tasks matching criteria"
                }

        except Exception as e:
            # Return error result
            return {
                "success": False,
                "message": f"Failed to list tasks: {str(e)}",
                "error": str(e)
            }


# Function that matches the expected MCP tool signature
def run(user_id: int, arguments_str: str) -> str:
    """
    Execute the task listing tool with JSON string arguments.

    Args:
        user_id: ID of the user executing the tool
        arguments_str: JSON string containing the arguments

    Returns:
        JSON string with the result of the operation
    """
    try:
        arguments = json.loads(arguments_str)
        result = TaskListingTool.execute(user_id, arguments)
        return json.dumps(result)
    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "message": f"Invalid JSON arguments: {str(e)}",
            "error": str(e)
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "error": str(e)
        })