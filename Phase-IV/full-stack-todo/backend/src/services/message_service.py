from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.message import Message, MessageCreate, RoleEnum
from ..models.conversation import Conversation


class MessageService:
    """
    Service class to handle business logic for messages.
    """

    @staticmethod
    def create_message(session: Session, message_data: MessageCreate) -> Message:
        """
        Create a new message in a conversation.
        """
        message = Message.from_orm(message_data)
        session.add(message)
        session.commit()
        session.refresh(message)

        # Update conversation's updated_at timestamp
        conversation_statement = select(Conversation).where(Conversation.id == message.conversation_id)
        conversation = session.exec(conversation_statement).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()

        return message

    @staticmethod
    def get_message_by_id(session: Session, message_id: int, user_id: int) -> Optional[Message]:
        """
        Get a specific message by ID for a user (verifies user has access to the conversation).
        """
        statement = select(Message).join(Conversation).where(
            Message.id == message_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_messages_by_conversation(session: Session, conversation_id: int, user_id: int) -> List[Message]:
        """
        Get all messages in a specific conversation for a user.
        """
        statement = select(Message).join(Conversation).where(
            Message.conversation_id == conversation_id,
            Conversation.user_id == user_id
        ).order_by(Message.created_at.asc())
        return session.exec(statement).all()

    @staticmethod
    def get_recent_messages(session: Session, conversation_id: int, user_id: int, limit: int = 10) -> List[Message]:
        """
        Get recent messages in a conversation for a user.
        """
        statement = select(Message).join(Conversation).where(
            Message.conversation_id == conversation_id,
            Conversation.user_id == user_id
        ).order_by(Message.created_at.desc()).limit(limit)
        messages = session.exec(statement).all()
        # Return in chronological order
        return list(reversed(messages))

    @staticmethod
    def delete_message(session: Session, message_id: int, user_id: int) -> bool:
        """
        Delete a specific message for a user (verifies user has access to the conversation).
        """
        message = MessageService.get_message_by_id(session, message_id, user_id)
        if message:
            session.delete(message)
            session.commit()
            return True
        return False