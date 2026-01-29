from typing import List, Optional
from sqlmodel import Session, select, and_, func
from sqlalchemy import or_
from datetime import datetime
from src.models.task import Task, TaskCreate, TaskUpdate, PriorityEnum
from src.models.user import User


class TaskService:
    """
    Service class to handle business logic for tasks.
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate) -> Task:
        """
        Create a new task for a user.
        """
        task = Task.from_orm(task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Get a specific task by ID for a specific user.
        """
        statement = select(Task).where(
            and_(Task.id == task_id, Task.user_id == user_id)
        )
        return session.exec(statement).first()

    @staticmethod
    def get_tasks(
        session: Session,
        user_id: int,
        completed: Optional[bool] = None,
        priority: Optional[PriorityEnum] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "due_date",
        order: Optional[str] = "asc"
    ) -> List[Task]:
        """
        Get all tasks for a user with optional filtering and sorting.
        """
        statement = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        if priority is not None:
            statement = statement.where(Task.priority == priority)

        if tag is not None:
            # Tag filtering for comma-separated tags - match the tag exactly within the comma-separated list
            statement = statement.where(
                or_(
                    Task.tags.like(f'{tag},%'),    # Tag at the beginning
                    Task.tags.like(f'%{tag},%'),   # Tag in the middle or at the end
                    Task.tags.like(f'%{tag}'),     # Tag at the end (without trailing comma)
                    Task.tags == tag               # Exact match (tag is the only one)
                )
            )

        if search is not None:
            statement = statement.where(
                Task.title.contains(search) | Task.description.contains(search)
            )

        # Apply sorting
        if sort_by == "due_date":
            if order == "desc":
                statement = statement.order_by(Task.due_date.desc())
            else:
                statement = statement.order_by(Task.due_date)
        elif sort_by == "priority":
            if order == "desc":
                statement = statement.order_by(Task.priority.desc())
            else:
                statement = statement.order_by(Task.priority)
        elif sort_by == "title":
            if order == "desc":
                statement = statement.order_by(Task.title.desc())
            else:
                statement = statement.order_by(Task.title)
        else:  # Default to due_date
            if order == "desc":
                statement = statement.order_by(Task.due_date.desc())
            else:
                statement = statement.order_by(Task.due_date)

        return session.exec(statement).all()

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a specific task for a user.
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if task:
            # Update only provided fields, excluding unset values
            update_data = task_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                if value is not None:  # Only update if the value is not None
                    setattr(task, field, value)

            # Update the updated_at timestamp
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a specific task for a user.
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if task:
            session.delete(task)
            session.commit()
            return True
        return False

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if task:
            task.completed = not task.completed
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
        return task