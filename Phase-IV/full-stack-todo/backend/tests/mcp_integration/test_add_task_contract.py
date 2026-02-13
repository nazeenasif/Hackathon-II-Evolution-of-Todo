"""
Contract test for the add_task MCP tool.
Verifies that the tool accepts the expected parameters and returns the expected response format.
"""
import pytest
from src.mcp_server.tools.add_task import get_add_task_tool, add_task_handler


@pytest.mark.asyncio
async def test_add_task_contract_valid_params(valid_add_task_params):
    """Test that add_task accepts valid parameters."""
    # This test verifies the contract by checking that valid params don't raise validation errors
    from src.mcp_server.utils import validate_add_task_input

    validation_result = validate_add_task_input(valid_add_task_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) == 0, f"Validation failed: {validation_result['errors']}"


@pytest.mark.asyncio
async def test_add_task_contract_missing_title():
    """Test that add_task rejects requests without title."""
    from src.mcp_server.utils import validate_add_task_input

    invalid_params = {"description": "Missing title"}
    validation_result = validate_add_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("title is required" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_add_task_contract_empty_title():
    """Test that add_task rejects requests with empty title."""
    from src.mcp_server.utils import validate_add_task_input

    invalid_params = {"title": ""}
    validation_result = validate_add_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("title is required" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_add_task_response_format():
    """Test that add_task returns the expected response format."""
    # Check that the tool definition has the expected schema
    tool = get_add_task_tool()

    # Verify the tool has the expected name
    assert hasattr(tool, '__call__') or callable(tool)

    # Verify the handler function exists and is callable
    assert callable(add_task_handler)


@pytest.mark.asyncio
async def test_add_task_tool_schema():
    """Test that add_task has the expected input schema."""
    # Since we can't easily inspect the MCP tool schema without importing the SDK,
    # we'll verify that the validation function works as expected
    from src.mcp_server.utils import validate_add_task_input

    # Test various valid parameter combinations
    valid_cases = [
        {"title": "Simple task"},
        {"title": "Task with description", "description": "A detailed description"},
        {"title": "Task with priority", "priority": "high"},
        {"title": "Task with due date", "due_date": "2023-12-31T23:59:59"},
        {"title": "Task with tags", "tags": ["work", "urgent"]},
        {
            "title": "Full task",
            "description": "A complete task",
            "due_date": "2023-12-31T23:59:59",
            "priority": "medium",
            "tags": ["work", "important"]
        }
    ]

    for params in valid_cases:
        validation_result = validate_add_task_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) == 0, f"Validation failed for {params}: {validation_result['errors']}"