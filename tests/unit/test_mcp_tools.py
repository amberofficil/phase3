"""
Unit tests for MCP tools in the AI Todo Assistant.
Tests the MCP tool implementations to ensure they behave as expected.
"""

import pytest
from backend.src.lib.mcp_tools import add_task, list_tasks, complete_task, delete_task, update_task


def test_add_task_success():
    """Test successful addition of a task."""
    result = add_task("Test task description")

    assert result["success"] is True
    assert "Test task description" in result["message"]
    assert result["data"] is not None
    assert result["data"].description == "Test task description"
    assert result["data"].completed is False


def test_add_task_empty_description():
    """Test adding a task with empty description."""
    result = add_task("")

    assert result["success"] is False
    assert "empty" in result["message"]


def test_add_task_whitespace_only():
    """Test adding a task with whitespace-only description."""
    result = add_task("   ")

    assert result["success"] is False
    assert "empty" in result["message"]


def test_add_task_long_description():
    """Test adding a task with a description that exceeds the limit."""
    long_desc = "x" * 501  # Exceeds 500 character limit
    result = add_task(long_desc)

    assert result["success"] is False
    assert "exceeds" in result["message"]


def test_list_tasks_empty():
    """Test listing tasks when no tasks exist."""
    result = list_tasks()

    assert result["success"] is True
    assert result["data"] == []


def test_list_tasks_by_completion_status():
    """Test filtering tasks by completion status."""
    # Test with completed=None (no filter)
    result = list_tasks(completed=None)
    assert result["success"] is True

    # Test with completed=True
    result = list_tasks(completed=True)
    assert result["success"] is True

    # Test with completed=False
    result = list_tasks(completed=False)
    assert result["success"] is True


def test_complete_task_success():
    """Test successfully completing a task."""
    result = complete_task("Test task")

    assert result["success"] is True
    assert "marked as complete" in result["message"]
    assert result["data"] is not None


def test_complete_task_empty_identifier():
    """Test completing a task with empty identifier."""
    result = complete_task("")

    assert result["success"] is False
    assert "empty" in result["message"]


def test_delete_task_success():
    """Test successfully deleting a task."""
    result = delete_task("Test task")

    assert result["success"] is True
    assert "deleted" in result["message"]


def test_delete_task_empty_identifier():
    """Test deleting a task with empty identifier."""
    result = delete_task("")

    assert result["success"] is False
    assert "empty" in result["message"]


def test_update_task_success():
    """Test successfully updating a task."""
    result = update_task("Old task", "New task description")

    assert result["success"] is True
    assert "updated" in result["message"]
    assert result["data"] is not None


def test_update_task_empty_old_identifier():
    """Test updating a task with empty old identifier."""
    result = update_task("", "New task description")

    assert result["success"] is False
    assert "empty" in result["message"]


def test_update_task_empty_new_description():
    """Test updating a task with empty new description."""
    result = update_task("Old task", "")

    assert result["success"] is False
    assert "empty" in result["message"]


def test_update_task_whitespace_new_description():
    """Test updating a task with whitespace-only new description."""
    result = update_task("Old task", "   ")

    assert result["success"] is False
    assert "empty" in result["message"]


def test_update_task_long_new_description():
    """Test updating a task with new description that exceeds limit."""
    long_desc = "x" * 501  # Exceeds 500 character limit
    result = update_task("Old task", long_desc)

    assert result["success"] is False
    assert "exceeds" in result["message"]