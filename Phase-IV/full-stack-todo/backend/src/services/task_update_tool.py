import json
from typing import Dict, Any
from pydantic import BaseModel, Field
from .task_service import TaskService
from ..models.task import TaskUpdate
from sqlmodel import Session
from ..core.database import get_async_session
from datetime import datetime, timedelta
import re


class TaskUpdateTool:
    """
    MCP tool for updating tasks via natural language input.
    """

    @staticmethod
    def get_name() -> str:
        """
        Get the name of the tool.
        """
        return "update_task"

    @staticmethod
    def get_description() -> str:
        """
        Get the description of the tool for AI agent.
        """
        return "Update an existing task with new information"

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
                    "description": "ID of the task to update (optional if title is provided)"
                },
                "title": {
                    "type": "string",
                    "description": "Updated title of the task (optional if task_id is provided) or title of task to update"
                },
                "description": {
                    "type": "string",
                    "description": "Updated detailed description of the task"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Updated priority level of the task"
                },
                "tags": {
                    "type": "string",
                    "description": "Updated comma-separated tags for the task (e.g., 'work,important')"
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Updated due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                }
            },
            "required": []  # Neither field is strictly required, but one should be provided
        }

    @staticmethod
    def execute(user_id: int, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the task update with the provided arguments.

        Args:
            user_id: ID of the user updating the task
            arguments: Dictionary containing task update parameters

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
            title = arguments.get("title")  # This could be the new title or the title to find the task

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
                if not task_id and title and 'title' in arguments:
                    # In this case, title is used to identify the task to update, not to update the title
                    # We need to distinguish between "find by this title" vs "update title to this"
                    # Let's assume the AI model will send both the title to find AND new_title if updating title
                    # But for simplicity, we'll look for the exact title first
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
                    # Remove title from arguments if it was meant to identify the task, not update it
                    # We'll need to distinguish this better in practice
                    # For now, let's assume if title exists in the original request with other fields,
                    # it's meant to be updated, but if it's alone, it's for identification
                    # Actually, let's check if there are other update fields
                    update_fields = {k: v for k, v in arguments.items() if k != 'task_id'}
                    if len(update_fields) == 1:  # Only title was provided
                        # This is probably meant to identify the task, not update it
                        # So we'll remove it from update data
                        update_data = {}
                    else:
                        # There are other fields, so title might be an update field
                        # Keep all fields for update
                        update_data = {k: v for k, v in arguments.items() if k != 'task_id' and v is not None}
                else:
                    # We have task_id, so use it directly
                    update_data = {k: v for k, v in arguments.items() if k != 'task_id' and v is not None}

                # Process due date in update_data if it exists
                if 'due_date' in update_data and update_data['due_date'] and isinstance(update_data['due_date'], str):
                    update_data['due_date'] = parse_relative_date(update_data['due_date'])

                # Create a TaskUpdate object with the processed arguments
                task_update_data = TaskUpdate(**update_data)

                # Use the existing TaskService to update the task
                updated_task = TaskService.update_task(session, task_id, user_id, task_update_data)

                if updated_task:
                    # Return success result
                    return {
                        "success": True,
                        "task_id": updated_task.id,
                        "message": f"Task '{updated_task.title}' updated successfully",
                        "task_details": {
                            "id": updated_task.id,
                            "title": updated_task.title,
                            "description": updated_task.description,
                            "priority": updated_task.priority.value,
                            "completed": updated_task.completed,
                            "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                            "tags": updated_task.tags,
                            "updated_at": updated_task.updated_at.isoformat()
                        }
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
                "message": f"Failed to update task: {str(e)}",
                "error": str(e)
            }


def parse_relative_date(date_str: str) -> str:
    """
    Parse relative dates like 'today', 'tomorrow', 'yesterday' and convert them to proper ISO date format.

    Args:
        date_str: String containing the date (could be relative or absolute)

    Returns:
        Properly formatted ISO date string
    """
    if not isinstance(date_str, str):
        return date_str

    # Convert to lowercase for comparison
    lower_date = date_str.lower().strip()

    # Get current date (server's local date)
    current_date = datetime.now().date()

    # Handle relative dates
    if 'today' in lower_date or 'todays' in lower_date:
        parsed_date = current_date
    elif 'tomorrow' in lower_date:
        parsed_date = current_date + timedelta(days=1)
    elif 'yesterday' in lower_date:
        parsed_date = current_date - timedelta(days=1)
    elif 'next day' in lower_date:
        parsed_date = current_date + timedelta(days=1)
    elif 'day after' in lower_date:
        parsed_date = current_date + timedelta(days=1)
    elif 'day before' in lower_date:
        parsed_date = current_date - timedelta(days=1)
    else:
        # For absolute dates, try to parse them
        try:
            # If it contains time component (ISO format with T), return as is
            if 't' in date_str.lower():
                return date_str
            else:
                # Try to parse as date-only format (YYYY-MM-DD)
                parsed_date_obj = datetime.fromisoformat(date_str)
                # Convert date-only to datetime (at midnight) and return as ISO format
                datetime_with_time = datetime.combine(parsed_date_obj.date(), datetime.min.time())
                return datetime_with_time.isoformat()
        except ValueError:
            # If we can't parse it, return as is and let the validation handle it
            return date_str

    # Convert to datetime (midnight) and format as ISO string with timezone info
    datetime_obj = datetime.combine(parsed_date, datetime.min.time())
    # Return in ISO format that frontend can properly parse
    return datetime_obj.isoformat()


# Function that matches the expected MCP tool signature
def run(user_id: int, arguments_str: str) -> str:
    """
    Execute the task update tool with JSON string arguments.

    Args:
        user_id: ID of the user executing the tool
        arguments_str: JSON string containing the arguments

    Returns:
        JSON string with the result of the operation
    """
    try:
        arguments = json.loads(arguments_str)
        result = TaskUpdateTool.execute(user_id, arguments)
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