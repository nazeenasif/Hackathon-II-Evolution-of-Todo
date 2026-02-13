import json
from typing import Dict, Any
from pydantic import BaseModel, Field
from .task_service import TaskService
from sqlmodel import Session
from ..core.database import get_async_session


class TaskDeletionTool:
    """
    MCP tool for deleting tasks via natural language input.
    """

    @staticmethod
    def get_name() -> str:
        """
        Get the name of the tool.
        """
        return "delete_task"

    @staticmethod
    def get_description() -> str:
        """
        Get the description of the tool for AI agent.
        """
        return "Delete an existing task"

    @staticmethod
    def get_parameters() -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.
        """
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID of the task to delete (optional if title is provided)"
                },
                "title": {
                    "type": "string",
                    "description": "Title of the task to delete (optional if task_id is provided)"
                }
            },
            "required": []  # Neither field is strictly required, but one should be provided
        }

    @staticmethod
    def execute(user_id: int, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the task deletion with the provided arguments.

        Args:
            user_id: ID of the user deleting the task
            arguments: Dictionary containing task deletion parameters

        Returns:
            Dictionary with result of the operation
        """
        from src.core.database import engine
        from sqlmodel import Session, select
        from ..models.task import Task
        from sqlalchemy import and_

        try:
            # Extract task_id and title
            task_id = arguments.get("task_id")
            title = arguments.get("title")

            # Validate that at least one parameter is provided
            if not task_id and not title:
                return {
                    "success": False,
                    "message": "Either task_id or title must be provided",
                    "error": "Missing required parameter"
                }

            # Create database session using engine directly
            with Session(engine) as session:
                # If title is provided but no task_id, find the task by title
                if not task_id and title:
                    # Find the task by title for the user
                    statement = select(Task).where(
                        and_(Task.title == title, Task.user_id == user_id)
                    )
                    task = session.exec(statement).first()

                    if not task:
                        return {
                            "success": False,
                            "message": f"No task found with title '{title}'",
                            "error": "Task not found"
                        }

                    task_id = task.id

                # Use the existing TaskService to delete the task
                success = TaskService.delete_task(session, task_id, user_id)

                if success:
                    # Return success result
                    return {
                        "success": True,
                        "task_id": task_id,
                        "message": f"Task '{title or f'ID {task_id}'}' deleted successfully"
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Task with ID {task_id} not found or doesn't belong to user",
                        "error": "Task not found"
                    }

        except Exception as e:
            # Return error result
            return {
                "success": False,
                "message": f"Failed to delete task: {str(e)}",
                "error": str(e)
            }


# Function that matches the expected MCP tool signature
def run(user_id: int, arguments_str: str) -> str:
    """
    Execute the task deletion tool with JSON string arguments.

    Args:
        user_id: ID of the user executing the tool
        arguments_str: JSON string containing the arguments

    Returns:
        JSON string with the result of the operation
    """
    try:
        arguments = json.loads(arguments_str)
        result = TaskDeletionTool.execute(user_id, arguments)
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