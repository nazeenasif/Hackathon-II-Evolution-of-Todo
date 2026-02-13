"""
Contract test for the update_task MCP tool.
Verifies that the tool accepts the expected parameters and returns the expected response format.
"""
import pytest
from src.mcp_server.utils import validate_update_task_input


@pytest.mark.asyncio
async def test_update_task_contract_valid_params():
    """Test that update_task accepts valid parameters."""
    # Test various valid parameter combinations
    valid_cases = [
        {"task_id": 1, "title": "Updated Title"},
        {"task_id": 1, "description": "Updated Description"},
        {"task_id": 1, "priority": "high"},
        {"task_id": 1, "due_date": "2023-12-31T23:59:59"},
        {"task_id": 1, "tags": ["updated", "tags"]},
        {
            "task_id": 1,
            "title": "Fully Updated Task",
            "description": "Updated Description",
            "priority": "low",
            "due_date": "2023-12-31T23:59:59",
            "tags": ["work", "important"]
        }
    ]

    for params in valid_cases:
        validation_result = validate_update_task_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) == 0, f"Validation failed for {params}: {validation_result['errors']}"


@pytest.mark.asyncio
async def test_update_task_contract_missing_task_id():
    """Test that update_task rejects requests without task_id."""
    invalid_params = {"title": "Updated Title"}
    validation_result = validate_update_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("task_id is required" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_update_task_contract_invalid_task_id():
    """Test that update_task rejects invalid task_id values."""
    invalid_cases = [
        {"task_id": 0},      # Zero
        {"task_id": -1},     # Negative
        {"task_id": "abc"},  # String
        {"task_id": None}    # Null
    ]

    for params in invalid_cases:
        validation_result = validate_update_task_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) > 0
        assert any("task_id must be a positive integer" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_update_task_contract_invalid_priority():
    """Test that update_task rejects invalid priority values."""
    invalid_params = {
        "task_id": 1,
        "priority": "invalid_priority"
    }

    validation_result = validate_update_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("priority must be one of" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_update_task_contract_invalid_due_date():
    """Test that update_task rejects invalid due date formats."""
    invalid_params = {
        "task_id": 1,
        "due_date": "not-a-date"
    }

    validation_result = validate_update_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("due_date must be in ISO 8601 format" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_update_task_contract_too_many_tags():
    """Test that update_task rejects too many tags."""
    invalid_params = {
        "task_id": 1,
        "tags": [f"tag{i}" for i in range(15)]  # More than 10 tags
    }

    validation_result = validate_update_task_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("cannot have more than 10 tags" in error for error in validation_result["errors"])