from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ConversationBase(SQLModel):
    """
    Base model for Conversation with common fields.
    """
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(default="New Conversation", max_length=255)


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat conversation between user and AI agent.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    """
    Model for creating a new conversation.
    """
    user_id: int  # Required for creation


class ConversationRead(ConversationBase):
    """
    Model for reading conversation data.
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime