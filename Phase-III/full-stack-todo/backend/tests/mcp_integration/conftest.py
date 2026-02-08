"""
Base test configuration for MCP integration tests.
Sets up fixtures and utilities for testing MCP tools.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, Any

# Mock the MCP SDK since we don't want to actually start a server during tests
from unittest.mock import patch

# Import the actual tools we'll be testing
from src.mcp_server.adapters.task_adapter import TaskAdapter
from src.mcp_server.utils import (
    validate_add_task_input,
    validate_list_tasks_input,
    validate_update_task_input,
    validate_task_id_input
)
from src.mcp_server.decorators import tool_handler


@pytest.fixture
def mock_task_service():
    """Mock task service for testing."""
    mock = AsyncMock()
    # Example mock responses
    mock.create_task.return_value = MagicMock(
        id=1,
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        tags=[],
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        user_id=1
    )
    return mock


@pytest.fixture
def mock_task_adapter(mock_task_service):
    """Mock task adapter with mocked service."""
    adapter = TaskAdapter()
    adapter.task_service = mock_task_service
    return adapter


@pytest.fixture
def valid_add_task_params():
    """Valid parameters for add_task."""
    return {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium",
        "tags": ["test", "important"]
    }


@pytest.fixture
def valid_list_tasks_params():
    """Valid parameters for list_tasks."""
    return {
        "status": "pending",
        "limit": 10,
        "offset": 0,
        "sort_by": "created_at",
        "order": "desc"
    }


@pytest.fixture
def valid_update_task_params():
    """Valid parameters for update_task."""
    return {
        "task_id": 1,
        "title": "Updated Task",
        "description": "Updated Description",
        "priority": "high"
    }


def assert_success_response(response: Dict[str, Any]):
    """Assert that a response is successful."""
    assert "success" in response
    assert response["success"] is True


def assert_error_response(response: Dict[str, Any], expected_error_code: str = None):
    """Assert that a response is an error."""
    assert "success" in response
    assert response["success"] is False
    assert "error" in response

    if expected_error_code:
        assert "error_code" in response
        assert response["error_code"] == expected_error_code