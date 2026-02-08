import json
from typing import Dict, Any
from pydantic import BaseModel, Field
from .task_service import TaskService
from sqlmodel import Session
from ..core.database import get_async_session


class TaskCompletionTool:
    """
    MCP tool for toggling task completion status via natural language input.
    """

    @staticmethod
    def get_name() -> str:
        """
        Get the name of the tool.
        """
        return "toggle_task_completion"

    @staticmethod
    def get_description() -> str:
        """
        Get the description of the tool for AI agent.
        """
        return "Toggle the completion status of a task (mark as complete/incomplete)"

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
                    "description": "ID of the task to toggle completion status (optional if title is provided)"
                },
                "title": {
                    "type": "string",
                    "description": "Title of the task to toggle completion status (optional if task_id is provided)"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Whether the task should be marked as completed (true) or not (false)"
                }
            },
            "required": []
        }

    @staticmethod
    def execute(user_id: int, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the task completion toggle with the provided arguments.

        Args:
            user_id: ID of the user toggling the task completion
            arguments: Dictionary containing task completion parameters

        Returns:
            Dictionary with result of the operation
        """
        from src.core.database import engine
        from sqlmodel import Session, select
        from ..models.task import Task, TaskUpdate
        from sqlalchemy import and_

        try:
            # Extract task_id and title
            task_id = arguments.get("task_id")
            title = arguments.get("title")
            completed = arguments.get("completed")

            # Validate that at least one identifier is provided
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

                if completed is not None:
                    # If completed is specified, update to that value
                    task_update = TaskUpdate(completed=completed)
                    updated_task = TaskService.update_task(session, task_id, user_id, task_update)

                    if updated_task:
                        return {
                            "success": True,
                            "task_id": updated_task.id,
                            "message": f"Task '{updated_task.title}' marked as {'completed' if updated_task.completed else 'not completed'}",
                            "task_details": {
                                "id": updated_task.id,
                                "title": updated_task.title,
                                "completed": updated_task.completed,
                                "updated_at": updated_task.updated_at.isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "message": f"Task with ID {task_id} not found or doesn't belong to user",
                            "error": "Task not found"
                        }
                else:
                    # If completed is not specified, toggle the current status
                    current_task = TaskService.get_task_by_id(session, task_id, user_id)
                    if current_task:
                        # Use the existing toggle_task_completion method
                        updated_task = TaskService.toggle_task_completion(session, task_id, user_id)

                        if updated_task:
                            return {
                                "success": True,
                                "task_id": updated_task.id,
                                "message": f"Task '{updated_task.title}' marked as {'completed' if updated_task.completed else 'not completed'}",
                                "task_details": {
                                    "id": updated_task.id,
                                    "title": updated_task.title,
                                    "completed": updated_task.completed,
                                    "updated_at": updated_task.updated_at.isoformat()
                                }
                            }
                        else:
                            return {
                                "success": False,
                                "message": f"Failed to toggle completion status for task {task_id}",
                                "error": "Toggle failed"
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
                "message": f"Failed to toggle task completion: {str(e)}",
                "error": str(e)
            }


# Function that matches the expected MCP tool signature
def run(user_id: int, arguments_str: str) -> str:
    """
    Execute the task completion tool with JSON string arguments.

    Args:
        user_id: ID of the user executing the tool
        arguments_str: JSON string containing the arguments

    Returns:
        JSON string with the result of the operation
    """
    try:
        arguments = json.loads(arguments_str)
        result = TaskCompletionTool.execute(user_id, arguments)
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