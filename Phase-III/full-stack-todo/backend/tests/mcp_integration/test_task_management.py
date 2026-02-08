"""
Integration test for the task management flow using update_task, complete_task, and delete_task MCP tools.
Tests the complete flow from tool invocation to database interaction.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.mcp_server.tools.update_task import update_task_handler
from src.mcp_server.tools.complete_task import complete_task_handler
from src.mcp_server.tools.delete_task import delete_task_handler
from src.mcp_server.adapters.task_adapter import TaskAdapter


@pytest.mark.asyncio
async def test_update_task_integration_happy_path(mock_task_adapter):
    """Test successful task update via update_task tool."""
    # Arrange: Set up mock return value
    mock_task_adapter.update_task = AsyncMock(return_value={
        "id": 1,
        "title": "Updated Task",
        "description": "Updated Description",
        "status": "pending",
        "due_date": datetime.now().isoformat(),
        "priority": "high",
        "tags": ["updated", "important"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "user_id": 1
    })

    # Act: Call the handler
    params = {
        "task_id": 1,
        "title": "Updated Task",
        "description": "Updated Description",
        "priority": "high"
    }
    result = await update_task_handler(params)

    # Assert: Check the response format
    assert "success" in result
    assert result["success"] is True
    assert "task_id" in result
    assert result["task_id"] == 1


@pytest.mark.asyncio
async def test_complete_task_integration_happy_path(mock_task_adapter):
    """Test successful task completion via complete_task tool."""
    # Arrange: Set up mock return value
    mock_task_adapter.complete_task = AsyncMock(return_value={
        "id": 1,
        "title": "Completed Task",
        "description": "Original Description",
        "status": "completed",
        "due_date": datetime.now().isoformat(),
        "priority": "medium",
        "tags": ["test"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "user_id": 1
    })

    # Act: Call the handler
    params = {"task_id": 1}
    result = await complete_task_handler(params)

    # Assert: Check the response format
    assert "success" in result
    assert result["success"] is True
    assert "task_id" in result
    assert result["task_id"] == 1
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_task_integration_happy_path(mock_task_adapter):
    """Test successful task deletion via delete_task tool."""
    # Arrange: Set up mock return value
    mock_task_adapter.delete_task = AsyncMock(return_value=True)

    # Act: Call the handler
    params = {"task_id": 1}
    result = await delete_task_handler(params)

    # Assert: Check the response format
    assert "success" in result
    assert result["success"] is True


@pytest.mark.asyncio
async def test_task_management_handlers_with_mock_adapters(monkeypatch):
    """Test the full handlers with mocked adapters."""

    # Test update_task handler
    update_mock_adapter = AsyncMock()
    update_mock_adapter.update_task = AsyncMock(return_value={
        "id": 123,
        "title": "Updated Title",
        "status": "pending"
    })

    import src.mcp_server.tools.update_task
    monkeypatch.setattr(src.mcp_server.tools.update_task.TaskAdapter, '__new__', lambda cls: update_mock_adapter)

    params = {"task_id": 123, "title": "Updated Title"}
    result = await update_task_handler(params)
    assert result["success"] is True
    assert result["task_id"] == 123
    update_mock_adapter.update_task.assert_called_once()

    # Test complete_task handler
    complete_mock_adapter = AsyncMock()
    complete_mock_adapter.complete_task = AsyncMock(return_value={
        "id": 456,
        "status": "completed"
    })

    import src.mcp_server.tools.complete_task
    monkeypatch.setattr(src.mcp_server.tools.complete_task.TaskAdapter, '__new__', lambda cls: complete_mock_adapter)

    params = {"task_id": 456}
    result = await complete_task_handler(params)
    assert result["success"] is True
    assert result["task_id"] == 456
    complete_mock_adapter.complete_task.assert_called_once()

    # Test delete_task handler
    delete_mock_adapter = AsyncMock()
    delete_mock_adapter.delete_task = AsyncMock(return_value=True)

    import src.mcp_server.tools.delete_task
    monkeypatch.setattr(src.mcp_server.tools.delete_task.TaskAdapter, '__new__', lambda cls: delete_mock_adapter)

    params = {"task_id": 789}
    result = await delete_task_handler(params)
    assert result["success"] is True
    delete_mock_adapter.delete_task.assert_called_once()


@pytest.mark.asyncio
async def test_task_management_validation():
    """Test that validation works for task management tools."""
    from src.mcp_server.utils import validate_update_task_input, validate_task_id_input

    # Test update_task validation
    invalid_update_params = {"title": "No task_id"}  # Missing required task_id
    validation_result = validate_update_task_input(invalid_update_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("task_id is required" in error for error in validation_result["errors"])

    # Test complete_task/delete_task validation
    invalid_id_params = {"invalid_param": "value"}  # Missing required task_id
    validation_result = validate_task_id_input(invalid_id_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("task_id is required" in error for error in validation_result["errors"])