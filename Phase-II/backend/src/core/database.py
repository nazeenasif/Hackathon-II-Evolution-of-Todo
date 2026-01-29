from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import engine
from contextlib import contextmanager
from typing import Generator, AsyncGenerator
from src.core.config import settings
import asyncio


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=(settings.ENVIRONMENT == "development"),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300
)


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This should be called when starting the application.
    """
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def get_async_session() -> AsyncGenerator[Session, None]:
    """
    Provide an async transactional scope around a series of operations.
    This is the async version for use with FastAPI dependency injection.
    """
    with get_session() as session:
        yield session


def get_session_override():
    """
    Dependency override for testing purposes.
    """
    yield get_session()