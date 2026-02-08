from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    """
    Enum for message roles in conversation.
    """
    user = "user"
    assistant = "assistant"
    system = "system"
    tool = "tool"


class MessageBase(SQLModel):
    """
    Base model for Message with common fields.
    """
    conversation_id: int = Field(foreign_key="conversation.id")
    role: RoleEnum
    content: str = Field(max_length=10000)  # Allow longer messages for AI responses
    tool_calls: Optional[str] = Field(default=None, max_length=5000)  # Store as JSON string
    tool_call_results: Optional[str] = Field(default=None, max_length=5000)  # Store as JSON string


class Message(MessageBase, table=True):
    """
    Message model representing individual messages in a conversation.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    """
    Model for creating a new message.
    """
    conversation_id: int
    role: RoleEnum
    content: str


class MessageRead(MessageBase):
    """
    Model for reading message data.
    """
    id: int
    conversation_id: int
    created_at: datetime