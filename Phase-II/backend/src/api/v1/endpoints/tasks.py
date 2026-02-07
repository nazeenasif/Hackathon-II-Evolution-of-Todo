from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime

from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskToggleComplete, PriorityEnum
from src.models.user import User
from src.services.task_service import TaskService
from src.core.database import get_async_session as get_session
from src.core.security import get_current_user_id, require_same_user_id


router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[PriorityEnum] = Query(None, description="Filter by priority level"),
    tag: Optional[str] = Query(None, description="Filter by tag/category"),
    search: Optional[str] = Query(None, description="Search term for title or description"),
    sort_by: Optional[str] = Query("due_date", description="Field to sort by", regex="^(due_date|priority|title)$"),
    order: Optional[str] = Query("asc", description="Sort order", regex="^(asc|desc)$"),
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List tasks for the authenticated user with optional filtering and sorting.
    """
    tasks = TaskService.get_tasks(
        session=session,
        user_id=current_user_id,
        completed=completed,
        priority=priority,
        tag=tag,
        search=search,
        sort_by=sort_by,
        order=order
    )
    return tasks


@router.post("/tasks", response_model=TaskRead)
def create_task(
    task_data: TaskCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Set the user_id from the authenticated user
    task_data.user_id = current_user_id
    task = TaskService.create_task(session, task_data)
    return task


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get a specific task for the authenticated user.
    """
    task = TaskService.get_task_by_id(session, task_id, current_user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or doesn't belong to user")
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    task = TaskService.update_task(session, task_id, current_user_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or doesn't belong to user")
    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Delete a specific task for the authenticated user.
    """
    success = TaskService.delete_task(session, task_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found or doesn't belong to user")
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Toggle the completion status of a task for the authenticated user.
    """
    task = TaskService.toggle_task_completion(session, task_id, current_user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or doesn't belong to user")
    return task