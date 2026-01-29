import logging
from src.core.config import settings


def setup_logging():
    """
    Configure logging based on environment settings.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # Set lower log levels for specific loggers if needed
    if settings.ENVIRONMENT == "development":
        # Reduce noise from external libraries in development
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    """
    return logging.getLogger(name)


# Setup logging when this module is imported
setup_logging()