from sqlmodel import Session, select
from typing import Optional
from datetime import datetime

from src.models.user import User, UserCreate, UserLogin
from src.core.auth_utils import get_password_hash, verify_password


class UserService:
    """
    Service layer for User operations including creation, retrieval, and authentication.
    """

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        """
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user with a hashed password.
        """
        # Hash the password from user_data
        hashed_password = get_password_hash(user_data.password)

        # Create user object with hashed password
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        """
        user = UserService.get_user_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user