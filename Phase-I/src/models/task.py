"""
Task data model for the In-Memory Python Console Todo Application.

This module defines the Task entity with id, title, description, and status fields.
It includes validation rules as specified in the data model.
"""
from typing import Optional


class Task:
    """
    Represents a single todo item with ID, title, description, and status.

    Fields:
    - id (int): Unique identifier for the task, auto-incremented from 1
    - title (str): Required title of the task, minimum 1 character
    - description (str): Optional description of the task, can be empty string
    - status (str): Task completion status, either "Incomplete" or "Complete"
    """

    def __init__(self, task_id: int, title: str, description: str = "", status: str = "Incomplete"):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Required title of the task (minimum 1 character)
            description (str): Optional description of the task
            status (str): Task completion status, either "Complete" or "Incomplete"

        Raises:
            ValueError: If validation rules are not met
        """
        self.id = self._validate_id(task_id)
        self.title = self._validate_title(title)
        self.description = description
        self.status = self._validate_status(status)

    def _validate_id(self, task_id: int) -> int:
        """Validate that the task ID is a positive integer."""
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {task_id}")
        return task_id

    def _validate_title(self, title: str) -> str:
        """Validate that the title is a non-empty string."""
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise ValueError("Task title must be a non-empty string")
        return title.strip()

    def _validate_status(self, status: str) -> str:
        """Validate that the status is either 'Complete' or 'Incomplete'."""
        valid_statuses = ["Complete", "Incomplete"]
        if status not in valid_statuses:
            raise ValueError(f"Task status must be one of {valid_statuses}, got '{status}'")
        return status

    def to_dict(self) -> dict:
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

    def __repr__(self) -> str:
        """String representation of the Task."""
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status='{self.status}')"

    def __eq__(self, other) -> bool:
        """Check equality between two Task instances."""
        if not isinstance(other, Task):
            return False
        return (self.id == other.id and
                self.title == other.title and
                self.description == other.description and
                self.status == other.status)