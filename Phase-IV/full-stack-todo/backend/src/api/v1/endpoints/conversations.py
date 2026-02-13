from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from src.models.conversation import Conversation, ConversationRead
from src.models.message import MessageRead
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from src.core.database import get_async_session as get_session
from src.core.security import get_current_user_id, require_same_user_id


router = APIRouter()


@router.get("/conversations", response_model=List[ConversationRead])
def get_conversations(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of conversations to return"),
    offset: int = Query(0, ge=0, description="Number of conversations to skip"),
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List conversations for the authenticated user with pagination.
    """
    conversations = ConversationService.get_conversations_by_user(session, current_user_id)
    # Apply pagination
    paginated_conversations = conversations[offset:offset+limit]
    return paginated_conversations


@router.get("/conversations/{conversation_id}", response_model=List[MessageRead])
def get_conversation_messages(
    conversation_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all messages for a specific conversation.
    """
    # First verify the user has access to this conversation
    conversation = ConversationService.get_conversation_by_id(session, conversation_id, current_user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found or doesn't belong to user")

    messages = MessageService.get_messages_by_conversation(session, conversation_id, current_user_id)
    return messages


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific conversation for the authenticated user.
    """
    success = ConversationService.delete_conversation(session, conversation_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found or doesn't belong to user")
    return {"message": "Conversation deleted successfully"}