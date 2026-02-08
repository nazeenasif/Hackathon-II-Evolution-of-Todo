"""
Task adapter to interface with existing backend services.
This adapter ensures we reuse existing business logic without duplication.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from ...models.task import Task, TaskCreate, TaskUpdate, PriorityEnum
from ...services.task_service import TaskService
from ...core.database import get_session


class TaskAdapter:
    """Adapter that connects MCP tools to existing task services."""

    def __init__(self):
        self.task_service = TaskService()

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = "medium",
        tags: Optional[List[str]] = None,
        user_id: int = 1  # Default user for testing, should come from auth
    ) -> Dict[str, Any]:
        """Create a new task using the existing task service."""
        # Convert due_date string to datetime if provided
        due_datetime = None
        if due_date:
            try:
                due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                # Handle potential format issues
                due_datetime = None

        # Create task using existing service
        task_data = {
            "title": title,
            "description": description,
            "due_date": due_datetime,
            "priority": priority,
            "tags": ",".join(tags) if tags else "",
            "user_id": user_id
        }

        with get_session() as session:
            # Create the task
            from sqlmodel import Session
            task_create_obj = TaskCreate(**{
                k: v for k, v in task_data.items()
                if v is not None
            })

            # Call the synchronous create_task method
            task = self.task_service.create_task(session, task_create_obj)

            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": "completed" if task.completed else "pending",
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                "tags": task.tags.split(",") if task.tags else [],
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "user_id": task.user_id
            }

    def get_tasks(
        self,
        user_id: int = 1,  # Default user for testing, should come from auth
        status: Optional[str] = None,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        sort_by: Optional[str] = "created_at",
        order: Optional[str] = "desc"
    ) -> Dict[str, Any]:
        """Get tasks using the existing task service."""
        with get_session() as session:
            # Convert status to completed boolean for the existing service
            completed = None
            if status == "completed":
                completed = True
            elif status == "pending":
                completed = False
            # If status is "all" or None, keep completed as None

            # Map sort_by from our format to the existing service format
            # Our service expects "due_date", "priority", "title"
            # Map "created_at" to a default like "due_date"
            mapped_sort_by = sort_by if sort_by in ["due_date", "priority", "title"] else "due_date"

            # Call existing service method - note: the existing service has a slightly different signature
            # Let me check what the actual signature is from the code we saw
            # Looking at the get_tasks method above, it takes: session, user_id, completed, priority, tag, search, sort_by, order
            # But the signature in the code is: get_tasks(self, session: Session, user_id: int, completed: Optional[bool] = None, ...)

            tasks = self.task_service.get_tasks(
                session=session,
                user_id=user_id,
                completed=completed,
                sort_by=mapped_sort_by,
                order=order
            )

            # Format the response
            tasks_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": "completed" if task.completed else "pending",
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                    "tags": task.tags.split(",") if task.tags else [],
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "user_id": task.user_id
                }
                tasks_list.append(task_dict)

            return {
                "tasks": tasks_list,
                "total_count": len(tasks_list)
            }

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        user_id: int = 1  # Default user for testing, should come from auth
    ) -> Optional[Dict[str, Any]]:
        """Update a task using the existing task service."""
        with get_session() as session:
            # Get existing task to check ownership
            existing_task = self.task_service.get_task_by_id(session, task_id, user_id)
            if not existing_task:
                return None

            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if due_date is not None:
                try:
                    update_data["due_date"] = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    return None  # Invalid date format
            if priority is not None:
                update_data["priority"] = priority
            if tags is not None:
                update_data["tags"] = ",".join(tags)

            # Create TaskUpdate object
            task_update_obj = TaskUpdate(**{k: v for k, v in update_data.items() if v is not None})

            # Update using existing service
            updated_task = self.task_service.update_task(session, task_id, user_id, task_update_obj)

            if updated_task:
                return {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": "completed" if updated_task.completed else "pending",
                    "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                    "priority": updated_task.priority.value if hasattr(updated_task.priority, 'value') else updated_task.priority,
                    "tags": updated_task.tags.split(",") if updated_task.tags else [],
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat(),
                    "user_id": updated_task.user_id
                }
            return None

    def complete_task(
        self,
        task_id: int,
        user_id: int = 1  # Default user for testing, should come from auth
    ) -> Optional[Dict[str, Any]]:
        """Complete a task using the existing task service."""
        with get_session() as session:
            # Toggle the task completion status
            updated_task = self.task_service.toggle_task_completion(session, task_id, user_id)

            if updated_task:
                return {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": "completed" if updated_task.completed else "pending",
                    "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                    "priority": updated_task.priority.value if hasattr(updated_task.priority, 'value') else updated_task.priority,
                    "tags": updated_task.tags.split(",") if updated_task.tags else [],
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat(),
                    "user_id": updated_task.user_id
                }
            return None

    def delete_task(
        self,
        task_id: int,
        user_id: int = 1  # Default user for testing, should come from auth
    ) -> bool:
        """Delete a task using the existing task service."""
        with get_session() as session:
            # Delete using existing service
            return self.task_service.delete_task(session, task_id, user_id)

    async def get_tasks(
        self,
        user_id: int = 1,  # Default user for testing, should come from auth
        status: Optional[str] = None,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        sort_by: Optional[str] = "created_at",
        order: Optional[str] = "desc"
    ) -> Dict[str, Any]:
        """Get tasks using the existing task service."""
        async with get_session() as session:
            # Prepare filter parameters
            filters = {}
            if status and status != "all":
                filters["status"] = status

            # Call existing service method
            result = await self.task_service.get_tasks(
                session=session,
                user_id=user_id,
                filters=filters,
                limit=limit,
                offset=offset,
                sort_by=sort_by,
                order=order
            )

            # Format the response
            tasks = []
            for task in result["tasks"]:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "priority": task.priority,
                    "tags": task.tags,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "user_id": task.user_id
                }
                tasks.append(task_dict)

            return {
                "tasks": tasks,
                "total_count": result["total_count"]
            }

    async def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        user_id: int = 1  # Default user for testing, should come from auth
    ) -> Optional[Dict[str, Any]]:
        """Update a task using the existing task service."""
        async with get_session() as session:
            # Get existing task to check ownership
            existing_task = await self.task_service.get_task_by_id(session, task_id, user_id)
            if not existing_task:
                return None

            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if due_date is not None:
                update_data["due_date"] = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            if priority is not None:
                update_data["priority"] = priority
            if tags is not None:
                update_data["tags"] = tags

            # Update using existing service
            updated_task = await self.task_service.update_task(session, task_id, user_id, update_data)

            if updated_task:
                return {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": updated_task.status,
                    "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                    "priority": updated_task.priority,
                    "tags": updated_task.tags,
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat(),
                    "user_id": updated_task.user_id
                }
            return None

    async def complete_task(
        self,
        task_id: int,
        user_id: int = 1  # Default user for testing, should come from auth
    ) -> Optional[Dict[str, Any]]:
        """Complete a task using the existing task service."""
        async with get_session() as session:
            # Get existing task to check ownership
            existing_task = await self.task_service.get_task_by_id(session, task_id, user_id)
            if not existing_task:
                return None

            # Update using existing service
            updated_task = await self.task_service.update_task(
                session, task_id, user_id, {"status": "completed"}
            )

            if updated_task:
                return {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": updated_task.status,
                    "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                    "priority": updated_task.priority,
                    "tags": updated_task.tags,
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat(),
                    "user_id": updated_task.user_id
                }
            return None

    async def delete_task(
        self,
        task_id: int,
        user_id: int = 1  # Default user for testing, should come from auth
    ) -> bool:
        """Delete a task using the existing task service."""
        async with get_session() as session:
            # Get existing task to check ownership
            existing_task = await self.task_service.get_task_by_id(session, task_id, user_id)
            if not existing_task:
                return False

            # Delete using existing service
            return await self.task_service.delete_task(session, task_id, user_id)