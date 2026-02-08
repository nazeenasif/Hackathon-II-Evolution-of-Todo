from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator
import re


class UserBase(SQLModel):
    """
    Base model for User with common fields.
    """
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=50)

    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Email cannot be empty')
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        if len(v) > 255:
            raise ValueError('Email must be 255 characters or less')
        return v.lower().strip()

    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Username cannot be empty')
        if len(v) > 50:
            raise ValueError('Username must be 50 characters or less')
        # Username should contain only alphanumeric characters and underscores/hyphens
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.strip()


class User(UserBase, table=True):
    """
    User model representing a user account that owns tasks.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)  # Store hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship back-references would go here if needed
    # tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    password: str  # Plain text password for creation


class UserRead(UserBase):
    """
    Model for reading user data without sensitive information.
    """
    id: int
    created_at: datetime
    updated_at: datetime


class UserLogin(SQLModel):
    """
    Model for user login credentials.
    """
    email: str
    password: str