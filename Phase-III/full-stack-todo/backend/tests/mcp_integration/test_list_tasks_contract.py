"""
Contract test for the list_tasks MCP tool.
Verifies that the tool accepts the expected parameters and returns the expected response format.
"""
import pytest
from src.mcp_server.utils import validate_list_tasks_input


@pytest.mark.asyncio
async def test_list_tasks_contract_valid_params():
    """Test that list_tasks accepts valid parameters."""
    # Test various valid parameter combinations
    valid_cases = [
        {},  # No parameters, should use defaults
        {"status": "pending"},
        {"status": "completed"},
        {"status": "all"},
        {"limit": 10},
        {"offset": 0},
        {"sort_by": "created_at"},
        {"order": "desc"},
        {
            "status": "pending",
            "limit": 10,
            "offset": 0,
            "sort_by": "created_at",
            "order": "desc"
        }
    ]

    for params in valid_cases:
        validation_result = validate_list_tasks_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) == 0, f"Validation failed for {params}: {validation_result['errors']}"


@pytest.mark.asyncio
async def test_list_tasks_contract_invalid_status():
    """Test that list_tasks rejects invalid status values."""
    invalid_params = {"status": "invalid_status"}
    validation_result = validate_list_tasks_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("status must be one of" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_list_tasks_contract_invalid_limit():
    """Test that list_tasks rejects invalid limit values."""
    invalid_cases = [
        {"limit": 0},      # Too small
        {"limit": 101},    # Too large
        {"limit": -5}      # Negative
    ]

    for params in invalid_cases:
        validation_result = validate_list_tasks_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) > 0
        assert any("limit must be an integer between" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_list_tasks_contract_invalid_offset():
    """Test that list_tasks rejects invalid offset values."""
    invalid_params = {"offset": -1}
    validation_result = validate_list_tasks_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("offset must be a non-negative integer" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_list_tasks_contract_invalid_sort_by():
    """Test that list_tasks rejects invalid sort_by values."""
    invalid_params = {"sort_by": "invalid_field"}
    validation_result = validate_list_tasks_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("sort_by must be one of" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_list_tasks_contract_invalid_order():
    """Test that list_tasks rejects invalid order values."""
    invalid_params = {"order": "invalid_order"}
    validation_result = validate_list_tasks_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("order must be one of" in error for error in validation_result["errors"])