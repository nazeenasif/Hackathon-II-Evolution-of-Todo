from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/todo_app"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-here"  # Should be set in .env for production
    BETTER_AUTH_SECRET: str = "your-better-auth-secret-here"  # Should be set in .env for production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # Token expiration time in minutes (7 days = 7 * 24 * 60)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()