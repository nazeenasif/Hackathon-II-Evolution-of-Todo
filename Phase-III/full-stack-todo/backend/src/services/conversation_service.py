from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.conversation import Conversation, ConversationCreate


class ConversationService:
    """
    Service class to handle business logic for conversations.
    """

    @staticmethod
    def create_conversation(session: Session, conversation_data: ConversationCreate) -> Conversation:
        """
        Create a new conversation for a user.
        """
        conversation = Conversation.from_orm(conversation_data)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for a specific user.
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_conversations_by_user(session: Session, user_id: int) -> List[Conversation]:
        """
        Get all conversations for a user.
        """
        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        return session.exec(statement).all()

    @staticmethod
    def update_conversation_title(session: Session, conversation_id: int, user_id: int, title: str) -> Optional[Conversation]:
        """
        Update the title of a conversation.
        """
        conversation = ConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    @staticmethod
    def delete_conversation(session: Session, conversation_id: int, user_id: int) -> bool:
        """
        Delete a specific conversation for a user.
        """
        conversation = ConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if conversation:
            session.delete(conversation)
            session.commit()
            return True
        return False