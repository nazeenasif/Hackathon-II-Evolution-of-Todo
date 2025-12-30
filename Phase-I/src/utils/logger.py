"""
Logging utilities for the In-Memory Python Console Todo Application.

This module provides basic logging functionality for debugging purposes.
"""
import datetime
from typing import Any


class Logger:
    """
    A simple logging utility for the application.
    """

    @staticmethod
    def log_info(message: str) -> None:
        """
        Log an informational message.

        Args:
            message (str): The message to log
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] {timestamp} - {message}")

    @staticmethod
    def log_error(message: str) -> None:
        """
        Log an error message.

        Args:
            message (str): The error message to log
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ERROR] {timestamp} - {message}")

    @staticmethod
    def log_debug(message: str) -> None:
        """
        Log a debug message.

        Args:
            message (str): The debug message to log
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[DEBUG] {timestamp} - {message}")

    @staticmethod
    def log_warning(message: str) -> None:
        """
        Log a warning message.

        Args:
            message (str): The warning message to log
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[WARNING] {timestamp} - {message}")