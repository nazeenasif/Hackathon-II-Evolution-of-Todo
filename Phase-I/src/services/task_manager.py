"""
TaskManager service for the In-Memory Python Console Todo Application.

This module implements the core business logic for task operations,
including in-memory storage management as specified in the data model.
"""
from typing import Dict, List, Optional
from src.models.task import Task


class TaskManager:
    """
    Manages tasks in memory with operations for creating, retrieving, updating, and deleting tasks.
    """

    def __init__(self):
        """
        Initialize the TaskManager with empty storage and next ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def _get_next_id(self) -> int:
        """
        Get the next available task ID and increment the counter.

        Returns:
            int: The next available task ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the given title and optional description.

        Args:
            title (str): Required title of the task
            description (str): Optional description of the task

        Returns:
            Task: The created Task instance with a unique ID and default status of "Incomplete"
        """
        task_id = self._get_next_id()
        task = Task(task_id=task_id, title=title, description=description, status="Incomplete")
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks currently stored in memory.

        Returns:
            List[Task]: A list of all Task instances
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description while preserving its status.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            Task: The updated Task instance if found, None otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        # Update fields if provided
        if title is not None:
            task.title = task._validate_title(title)
        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if it didn't exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_status(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task between "Complete" and "Incomplete".

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            Task: The updated Task instance if found, None otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        # Toggle status
        task.status = "Complete" if task.status == "Incomplete" else "Incomplete"
        return task

    def get_next_id(self) -> int:
        """
        Get the next ID that will be assigned (without incrementing).
        This is primarily for testing purposes.

        Returns:
            int: The next ID that will be assigned
        """
        return self._next_id