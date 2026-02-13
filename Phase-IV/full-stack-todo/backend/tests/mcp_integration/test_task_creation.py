"""
Integration test for the task creation flow using the add_task MCP tool.
Tests the complete flow from tool invocation to database interaction.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.mcp_server.tools.add_task import add_task_handler
from src.mcp_server.adapters.task_adapter import TaskAdapter


@pytest.mark.asyncio
async def test_add_task_integration_happy_path(mock_task_adapter):
    """Test successful task creation via add_task tool."""
    # Arrange: Set up mock return value
    expected_task = MagicMock(
        id=1,
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        tags=["test", "important"],
        due_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user_id=1
    )
    mock_task_adapter.create_task = AsyncMock(return_value={
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
        "due_date": datetime.now().isoformat(),
        "priority": "medium",
        "tags": ["test", "important"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "user_id": 1
    })

    # Act: Call the handler
    params = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium",
        "tags": ["test", "important"]
    }
    result = await add_task_handler(params)

    # Assert: Check the response format
    assert "success" in result
    assert result["success"] is True
    assert "task_id" in result
    assert result["task_id"] == 1


@pytest.mark.asyncio
async def test_add_task_integration_with_optional_params():
    """Test task creation with various optional parameters."""
    # Since we can't easily mock the actual adapter in this context,
    # we'll test the validation and handler separately
    from src.mcp_server.utils import validate_add_task_input

    # Test various combinations of optional parameters
    test_cases = [
        {"title": "Task with description", "description": "A description"},
        {"title": "Task with due date", "due_date": "2023-12-31T23:59:59"},
        {"title": "Task with priority", "priority": "high"},
        {"title": "Task with tags", "tags": ["tag1", "tag2"]},
        {
            "title": "Full task",
            "description": "A complete task",
            "due_date": "2023-12-31T23:59:59",
            "priority": "low",
            "tags": ["work", "personal"]
        }
    ]

    for params in test_cases:
        validation_result = validate_add_task_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) == 0, f"Validation failed for {params}: {validation_result['errors']}"


@pytest.mark.asyncio
async def test_add_task_integration_invalid_priority():
    """Test that add_task rejects invalid priority values."""
    from src.mcp_server.utils import validate_add_task_input

    invalid_params = {
        "title": "Test Task",
        "priority": "invalid_priority"
    }

    validation_result = validate_add_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("priority must be one of" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_add_task_integration_invalid_due_date():
    """Test that add_task rejects invalid due date formats."""
    from src.mcp_server.utils import validate_add_task_input

    invalid_params = {
        "title": "Test Task",
        "due_date": "not-a-date"
    }

    validation_result = validate_add_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("due_date must be in ISO 8601 format" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_add_task_integration_too_many_tags():
    """Test that add_task rejects too many tags."""
    from src.mcp_server.utils import validate_add_task_input

    invalid_params = {
        "title": "Test Task",
        "tags": [f"tag{i}" for i in range(15)]  # More than 10 tags
    }

    validation_result = validate_add_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("cannot have more than 10 tags" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_add_task_handler_with_mock_adapter(monkeypatch):
    """Test the full handler with a mocked adapter."""
    # Create a mock adapter
    mock_adapter = AsyncMock()
    mock_adapter.create_task = AsyncMock(return_value={
        "id": 123,
        "title": "Created Task",
        "status": "pending",
        "user_id": 1
    })

    # Patch the adapter in the module
    import src.mcp_server.tools.add_task
    monkeypatch.setattr(src.mcp_server.tools.add_task.TaskAdapter, '__new__', lambda cls: mock_adapter)

    # Call the handler
    params = {"title": "Created Task"}
    result = await add_task_handler(params)

    # Verify the result
    assert result["success"] is True
    assert result["task_id"] == 123

    # Verify the adapter was called with correct parameters
    mock_adapter.create_task.assert_called_once()
    call_args = mock_adapter.create_task.call_args
    assert call_args[1]["title"] == "Created Task"