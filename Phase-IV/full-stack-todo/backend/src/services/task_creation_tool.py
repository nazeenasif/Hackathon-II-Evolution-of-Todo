import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from .task_service import TaskService
from ..models.task import TaskCreate
from sqlmodel import Session
from ..core.database import get_async_session
from datetime import datetime, timedelta
import re


class TaskCreationTool:
    """
    MCP tool for creating tasks via natural language input.
    """

    @staticmethod
    def get_name() -> str:
        """
        Get the name of the tool.
        """
        return "create_task"

    @staticmethod
    def get_description() -> str:
        """
        Get the description of the tool for AI agent.
        """
        return "Create a new task with title, description, priority, tags, and due date"

    @staticmethod
    def get_parameters() -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.
        """
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the task"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the task"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Priority level of the task",
                    "default": "medium"
                },
                "tags": {
                    "type": "string",
                    "description": "Comma-separated tags for the task (e.g., 'work,important')"
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                }
            },
            "required": ["title"]
        }

    @staticmethod
    def execute(user_id: int, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the task creation with the provided arguments.

        Args:
            user_id: ID of the user creating the task
            arguments: Dictionary containing task creation parameters

        Returns:
            Dictionary with result of the operation
        """
        from src.core.database import engine
        from sqlmodel import Session

        try:
            # Process due date to handle relative dates like "today", "tomorrow", "yesterday"
            due_date = arguments.get("due_date")
            if due_date and isinstance(due_date, str):
                # Handle relative dates
                due_date = parse_relative_date(due_date)

            # Create a TaskCreate object with the provided arguments
            task_create_data = TaskCreate(
                title=arguments.get("title"),
                description=arguments.get("description"),
                priority=arguments.get("priority", "medium"),
                tags=arguments.get("tags"),
                due_date=due_date,
                user_id=user_id  # This will be overridden by the service with the authenticated user_id
            )

            # Create database session using engine directly
            with Session(engine) as session:
                # Use the existing TaskService to create the task
                created_task = TaskService.create_task(session, task_create_data)

                # Return success result
                return {
                    "success": True,
                    "task_id": created_task.id,
                    "message": f"Task '{created_task.title}' created successfully",
                    "task_details": {
                        "id": created_task.id,
                        "title": created_task.title,
                        "description": created_task.description,
                        "priority": created_task.priority.value,
                        "completed": created_task.completed,
                        "due_date": created_task.due_date.isoformat() if created_task.due_date else None,
                        "tags": created_task.tags,
                        "created_at": created_task.created_at.isoformat()
                    }
                }

        except Exception as e:
            # Return error result
            return {
                "success": False,
                "message": f"Failed to create task: {str(e)}",
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
    Execute the task creation tool with JSON string arguments.

    Args:
        user_id: ID of the user executing the tool
        arguments_str: JSON string containing the arguments

    Returns:
        JSON string with the result of the operation
    """
    try:
        arguments = json.loads(arguments_str)
        result = TaskCreationTool.execute(user_id, arguments)
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