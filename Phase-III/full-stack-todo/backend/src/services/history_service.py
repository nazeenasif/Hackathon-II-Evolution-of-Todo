from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime, timedelta
from ..models.message import Message
from ..models.conversation import Conversation
from .message_service import MessageService


class HistoryService:
    """
    Service class to handle conversation history retrieval and management.
    """

    @staticmethod
    def get_recent_conversation_history(
        session: Session,
        conversation_id: int,
        user_id: int,
        limit: int = 10
    ) -> List[Message]:
        """
        Get recent messages from a conversation for context.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user requesting history
            limit: Maximum number of messages to retrieve

        Returns:
            List of messages in chronological order
        """
        return MessageService.get_recent_messages(session, conversation_id, user_id, limit)

    @staticmethod
    def get_full_conversation_history(
        session: Session,
        conversation_id: int,
        user_id: int
    ) -> List[Message]:
        """
        Get all messages from a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user requesting history

        Returns:
            List of all messages in chronological order
        """
        return MessageService.get_messages_by_conversation(session, conversation_id, user_id)

    @staticmethod
    def get_conversation_summary(
        session: Session,
        conversation_id: int,
        user_id: int
    ) -> Optional[dict]:
        """
        Get a summary of the conversation including metadata.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user requesting summary

        Returns:
            Dictionary with conversation summary information
        """
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).first()

        if not conversation:
            return None

        # Get message count
        message_count = len(HistoryService.get_full_conversation_history(session, conversation_id, user_id))

        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "message_count": message_count,
            "user_id": conversation.user_id
        }

    @staticmethod
    def get_conversations_for_user(
        session: Session,
        user_id: int,
        days_back: int = 30
    ) -> List[dict]:
        """
        Get conversation summaries for a user within a date range.

        Args:
            session: Database session
            user_id: ID of the user
            days_back: Number of days back to include conversations

        Returns:
            List of conversation summaries
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)

        conversations = session.exec(
            select(Conversation)
            .where(
                Conversation.user_id == user_id,
                Conversation.updated_at >= cutoff_date
            )
            .order_by(Conversation.updated_at.desc())
        ).all()

        result = []
        for conv in conversations:
            # Get message count for each conversation
            messages = HistoryService.get_full_conversation_history(session, conv.id, user_id)
            result.append({
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "message_count": len(messages)
            })

        return result

    @staticmethod
    def search_conversation_messages(
        session: Session,
        user_id: int,
        search_term: str,
        conversation_id: Optional[int] = None
    ) -> List[Message]:
        """
        Search for messages in conversations that match a search term.

        Args:
            session: Database session
            user_id: ID of the user performing search
            search_term: Term to search for in message content
            conversation_id: Optional specific conversation to search in

        Returns:
            List of matching messages
        """
        query = select(Message).join(Conversation).where(
            Conversation.user_id == user_id,
            Message.content.contains(search_term)
        )

        if conversation_id:
            query = query.where(Conversation.id == conversation_id)

        query = query.order_by(Message.created_at.desc())

        return session.exec(query).all()