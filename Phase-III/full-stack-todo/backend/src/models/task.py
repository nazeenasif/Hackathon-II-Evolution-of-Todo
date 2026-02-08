from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import field_validator


class PriorityEnum(str, Enum):
    """
    Enum for task priority levels.
    """
    high = "high"
    medium = "medium"
    low = "low"


class TaskBase(SQLModel):
    """
    Base model for Task with common fields.
    """
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    tags: Optional[str] = Field(default=None, max_length=500)  # Comma-separated tags
    due_date: Optional[datetime] = Field(default=None)
    user_id: int = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item with various organizational features.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class TaskCreate(TaskBase):
    """
    Model for creating a new task.
    """
    # Override user_id to make it optional since it will be set from JWT token
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class TaskRead(TaskBase):
    """
    Model for reading task data.
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """
    Model for updating task fields.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None

    

class TaskToggleComplete(SQLModel):
    """
    Model for toggling task completion status.
    """
    completed: bool