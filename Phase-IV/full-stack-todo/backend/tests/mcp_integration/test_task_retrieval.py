"""
Integration test for the task retrieval flow using the list_tasks MCP tool.
Tests the complete flow from tool invocation to database interaction.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.mcp_server.tools.list_tasks import list_tasks_handler
from src.mcp_server.adapters.task_adapter import TaskAdapter


@pytest.mark.asyncio
async def test_list_tasks_integration_happy_path(mock_task_adapter):
    """Test successful task listing via list_tasks tool."""
    # Arrange: Set up mock return value
    mock_task_adapter.get_tasks = AsyncMock(return_value={
        "tasks": [
            {
                "id": 1,
                "title": "Test Task 1",
                "description": "Description 1",
                "status": "pending",
                "due_date": datetime.now().isoformat(),
                "priority": "medium",
                "tags": ["test"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "user_id": 1
            },
            {
                "id": 2,
                "title": "Test Task 2",
                "description": "Description 2",
                "status": "completed",
                "due_date": datetime.now().isoformat(),
                "priority": "high",
                "tags": ["important"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "user_id": 1
            }
        ],
        "total_count": 2
    })

    # Act: Call the handler
    params = {
        "status": "all",
        "limit": 10,
        "offset": 0
    }
    result = await list_tasks_handler(params)

    # Assert: Check the response format
    assert "success" in result
    assert result["success"] is True
    assert "tasks" in result
    assert "total_count" in result
    assert len(result["tasks"]) == 2
    assert result["total_count"] == 2


@pytest.mark.asyncio
async def test_list_tasks_integration_with_filters():
    """Test task listing with various filter parameters."""
    from src.mcp_server.utils import validate_list_tasks_input

    # Test various combinations of filter parameters
    test_cases = [
        {"status": "pending"},
        {"limit": 5},
        {"offset": 10},
        {"sort_by": "created_at", "order": "desc"},
        {
            "status": "pending",
            "limit": 5,
            "offset": 0,
            "sort_by": "priority",
            "order": "asc"
        }
    ]

    for params in test_cases:
        validation_result = validate_list_tasks_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) == 0, f"Validation failed for {params}: {validation_result['errors']}"


@pytest.mark.asyncio
async def test_list_tasks_integration_default_params():
    """Test that list_tasks works with default parameters."""
    from src.mcp_server.utils import validate_list_tasks_input

    # Empty params should be valid (use defaults)
    params = {}
    validation_result = validate_list_tasks_input(params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) == 0


@pytest.mark.asyncio
async def test_list_tasks_handler_with_mock_adapter(monkeypatch):
    """Test the full handler with a mocked adapter."""
    # Create a mock adapter
    mock_adapter = AsyncMock()
    mock_adapter.get_tasks = AsyncMock(return_value={
        "tasks": [{"id": 1, "title": "Test Task", "status": "pending"}],
        "total_count": 1
    })

    # Patch the adapter in the module
    import src.mcp_server.tools.list_tasks
    monkeypatch.setattr(src.mcp_server.tools.list_tasks.TaskAdapter, '__new__', lambda cls: mock_adapter)

    # Call the handler
    params = {"status": "pending"}
    result = await list_tasks_handler(params)

    # Verify the result
    assert result["success"] is True
    assert len(result["tasks"]) == 1
    assert result["total_count"] == 1

    # Verify the adapter was called with correct parameters
    mock_adapter.get_tasks.assert_called_once()
    call_args = mock_adapter.get_tasks.call_args
    assert call_args[1]["status"] == "pending"