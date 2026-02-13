"""
Contract test for the complete_task MCP tool.
Verifies that the tool accepts the expected parameters and returns the expected response format.
"""
import pytest
from src.mcp_server.utils import validate_task_id_input


@pytest.mark.asyncio
async def test_complete_task_contract_valid_params():
    """Test that complete_task accepts valid parameters."""
    # Test valid parameter
    valid_params = {"task_id": 1}
    validation_result = validate_task_id_input(valid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) == 0, f"Validation failed for {valid_params}: {validation_result['errors']}"


@pytest.mark.asyncio
async def test_complete_task_contract_missing_task_id():
    """Test that complete_task rejects requests without task_id."""
    invalid_params = {"other_param": "value"}
    validation_result = validate_task_id_input(invalid_params)
    assert "errors" in validation_result
    assert len(validation_result["errors"]) > 0
    assert any("task_id is required" in error for error in validation_result["errors"])


@pytest.mark.asyncio
async def test_complete_task_contract_invalid_task_id():
    """Test that complete_task rejects invalid task_id values."""
    invalid_cases = [
        {"task_id": 0},      # Zero
        {"task_id": -1},     # Negative
        {"task_id": "abc"},  # String
        {"task_id": None}    # Null
    ]

    for params in invalid_cases:
        validation_result = validate_task_id_input(params)
        assert "errors" in validation_result
        assert len(validation_result["errors"]) > 0
        assert any("task_id must be a positive integer" in error for error in validation_result["errors"])