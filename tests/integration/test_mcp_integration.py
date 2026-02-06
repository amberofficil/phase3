"""
Integration tests for the AI Todo Assistant MCP tools integration.
Tests that the various components work together properly.
"""

import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.natural_language_processor import NaturalLanguageProcessor
from backend.src.services.task_service import TaskService
from backend.src.lib.mcp_tools import add_task, list_tasks, complete_task, delete_task, update_task


def test_full_add_task_flow():
    """Test the full flow from natural language to task addition."""
    processor = NaturalLanguageProcessor()

    # Test that the natural language command can be processed end-to-end
    with patch('backend.src.services.task_service.TaskService.create_task') as mock_create:
        mock_create.return_value = {
            "success": True,
            "message": "Task 'buy groceries' added successfully",
            "data": None
        }

        result = processor.process_command("add buy groceries", "user123")

        # Assert that the result has the expected structure
        assert result["success"] is True
        assert result["action_taken"] == "add"
        assert "buy groceries" in result["message"]

        # Assert that the create_task method was called
        mock_create.assert_called_once_with("buy groceries")


def test_full_list_task_flow():
    """Test the full flow from natural language to task listing."""
    processor = NaturalLanguageProcessor()

    with patch('backend.src.services.task_service.TaskService.get_all_tasks') as mock_get_all:
        mock_get_all.return_value = {
            "success": True,
            "message": "Retrieved 2 tasks",
            "data": []
        }

        result = processor.process_command("show my tasks", "user123")

        assert result["success"] is True
        assert result["action_taken"] == "list"
        assert "tasks" in result

        mock_get_all.assert_called_once()


def test_full_complete_task_flow():
    """Test the full flow from natural language to task completion."""
    processor = NaturalLanguageProcessor()

    with patch('backend.src.services.task_service.TaskService.mark_task_completed') as mock_complete:
        mock_complete.return_value = {
            "success": True,
            "message": "Task 'buy groceries' marked as complete",
            "data": None
        }

        result = processor.process_command("done with buy groceries", "user123")

        assert result["success"] is True
        assert result["action_taken"] == "complete"
        assert "buy groceries" in result["message"]

        mock_complete.assert_called_once_with("buy groceries")


def test_full_delete_task_flow():
    """Test the full flow from natural language to task deletion."""
    processor = NaturalLanguageProcessor()

    with patch('backend.src.services.task_service.TaskService.remove_task') as mock_remove:
        mock_remove.return_value = {
            "success": True,
            "message": "Task 'old task' deleted successfully",
            "data": None
        }

        result = processor.process_command("delete old task", "user123")

        assert result["success"] is True
        assert result["action_taken"] == "delete"
        assert "old task" in result["message"]

        mock_remove.assert_called_once_with("old task")


def test_full_update_task_flow():
    """Test the full flow from natural language to task update."""
    processor = NaturalLanguageProcessor()

    with patch('backend.src.services.task_service.TaskService.modify_task') as mock_modify:
        mock_modify.return_value = {
            "success": True,
            "message": "Task 'old task' updated to 'new task'",
            "data": None
        }

        result = processor.process_command("change old task to new task", "user123")

        assert result["success"] is True
        assert result["action_taken"] == "update"
        assert "old task" in result["message"]
        assert "new task" in result["message"]

        mock_modify.assert_called_once_with("old task", "new task")


def test_error_handling_in_processing():
    """Test error handling when processing commands."""
    processor = NaturalLanguageProcessor()

    # Test when a service method raises an exception
    with patch('backend.src.services.task_service.TaskService.create_task', side_effect=Exception("Database error")):
        result = processor.process_command("add test task", "user123")

        assert result["success"] is False
        assert result["action_taken"] == "error"
        assert "Database error" in result["message"]


def test_task_service_integration():
    """Test the integration between TaskService and MCP tools."""
    service = TaskService()

    # Test that TaskService methods call the appropriate MCP tools
    with patch('backend.src.services.task_service.add_task') as mock_add:
        mock_add.return_value = {
            "success": True,
            "message": "Task added",
            "data": None
        }

        result = service.create_task("test task")

        assert result["success"] is True
        mock_add.assert_called_once_with("test task")


def test_task_service_validation():
    """Test validation in TaskService methods."""
    service = TaskService()

    # Test validation in create_task
    result = service.create_task("")
    assert result["success"] is False
    assert "cannot be empty" in result["message"]

    # Test validation in modify_task
    result = service.modify_task("", "new desc")
    assert result["success"] is False
    assert "cannot be empty" in result["message"]

    result = service.modify_task("old desc", "")
    assert result["success"] is False
    assert "cannot be empty" in result["message"]


def test_mcp_tool_mock_integration():
    """Test that MCP tools work with mocked implementations."""
    # Test add_task
    result = add_task("Test task description")
    assert result["success"] is True
    assert result["data"] is not None

    # Test list_tasks
    result = list_tasks()
    assert result["success"] is True

    # Test complete_task
    result = complete_task("Test task")
    assert result["success"] is True

    # Test delete_task
    result = delete_task("Test task")
    assert result["success"] is True

    # Test update_task
    result = update_task("Old task", "New task")
    assert result["success"] is True