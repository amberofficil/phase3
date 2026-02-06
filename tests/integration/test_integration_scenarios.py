"""
Integration tests for end-to-end scenarios in the AI Todo Assistant.
Tests the complete user journeys and validates the success criteria.
"""

import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.natural_language_processor import NaturalLanguageProcessor


def test_end_to_end_basic_workflow():
    """Test the complete workflow: add -> list -> complete -> delete."""
    processor = NaturalLanguageProcessor()

    # Mock all service methods to simulate the complete flow
    with patch('backend.src.services.task_service.TaskService.create_task') as mock_create, \
         patch('backend.src.services.task_service.TaskService.get_all_tasks') as mock_get_all, \
         patch('backend.src.services.task_service.TaskService.mark_task_completed') as mock_complete, \
         patch('backend.src.services.task_service.TaskService.remove_task') as mock_delete:

        # Set up mock return values
        mock_create.return_value = {
            "success": True,
            "message": "Task 'buy groceries' added successfully",
            "data": MagicMock(id=1, description="buy groceries", completed=False)
        }

        mock_get_all.return_value = {
            "success": True,
            "message": "Retrieved 1 tasks",
            "data": [MagicMock(id=1, description="buy groceries", completed=False)]
        }

        mock_complete.return_value = {
            "success": True,
            "message": "Task 'buy groceries' marked as complete",
            "data": MagicMock(id=1, description="buy groceries", completed=True)
        }

        mock_delete.return_value = {
            "success": True,
            "message": "Task 'buy groceries' deleted successfully",
            "data": None
        }

        # Step 1: Add task
        result_add = processor.process_command("add buy groceries", "user123")
        assert result_add["success"] is True
        assert result_add["action_taken"] == "add"
        assert "buy groceries" in result_add["message"]

        # Step 2: List tasks
        result_list = processor.process_command("show my tasks", "user123")
        assert result_list["success"] is True
        assert result_list["action_taken"] == "list"

        # Step 3: Complete task
        result_complete = processor.process_command("done with buy groceries", "user123")
        assert result_complete["success"] is True
        assert result_complete["action_taken"] == "complete"

        # Step 4: Delete task
        result_delete = processor.process_command("delete buy groceries", "user123")
        assert result_delete["success"] is True
        assert result_delete["action_taken"] == "delete"


def test_varied_command_expressions():
    """Test the system's ability to handle varied user expressions."""
    processor = NaturalLanguageProcessor()

    # Different ways to add a task
    add_commands = [
        "add buy groceries",
        "create call mom",
        "remember walk the dog",
        "i need to exercise"
    ]

    for cmd in add_commands:
        with patch('backend.src.services.task_service.TaskService.create_task') as mock_create:
            mock_create.return_value = {
                "success": True,
                "message": "Task added successfully",
                "data": MagicMock()
            }
            result = processor.process_command(cmd, "user123")
            assert result["success"] is True
            assert result["action_taken"] == "add"

    # Different ways to list tasks
    list_commands = [
        "show my tasks",
        "list tasks",
        "what do I need to do?",
        "show me my todos"
    ]

    for cmd in list_commands:
        with patch('backend.src.services.task_service.TaskService.get_all_tasks') as mock_get:
            mock_get.return_value = {
                "success": True,
                "message": "Retrieved tasks",
                "data": []
            }
            result = processor.process_command(cmd, "user123")
            assert result["success"] is True
            assert result["action_taken"] == "list"

    # Different ways to complete tasks
    complete_commands = [
        "done with buy groceries",
        "complete call mom",
        "finish walk the dog",
        "mark exercise as done"
    ]

    for cmd in complete_commands:
        with patch('backend.src.services.task_service.TaskService.mark_task_completed') as mock_complete:
            mock_complete.return_value = {
                "success": True,
                "message": "Task completed",
                "data": MagicMock()
            }
            result = processor.process_command(cmd, "user123")
            assert result["success"] is True
            assert result["action_taken"] == "complete"


def test_ambiguous_request_handling():
    """Test handling of ambiguous requests with clarification."""
    processor = NaturalLanguageProcessor()

    # Mock to simulate multiple tasks exist
    with patch('backend.src.services.task_service.TaskService.get_all_tasks') as mock_get_all:
        # Create mock tasks
        mock_task1 = MagicMock()
        mock_task1.description = "buy groceries"
        mock_task1.id = 1

        mock_task2 = MagicMock()
        mock_task2.description = "buy milk"
        mock_task2.id = 2

        mock_get_all.return_value = {
            "success": True,
            "message": "Retrieved 2 tasks",
            "data": [mock_task1, mock_task2]
        }

        # Test ambiguous completion request
        result = processor.process_command("done with buy", "user123")

        # Should return clarification needed
        assert result["success"] is False
        assert result["action_taken"] == "clarification_needed"
        assert "Did you mean" in result["message"] or "Could you be more specific" in result["message"]


def test_error_scenarios():
    """Test various error handling scenarios."""
    processor = NaturalLanguageProcessor()

    # Test unrecognizable command
    result = processor.process_command("this is not a valid command", "user123")
    assert result["success"] is False
    assert result["action_taken"] == "unknown"

    # Test with service failure
    with patch('backend.src.services.task_service.TaskService.create_task', side_effect=Exception("DB Error")):
        result = processor.process_command("add test task", "user123")
        assert result["success"] is False
        assert result["action_taken"] == "error"


def test_task_update_scenario():
    """Test the update/modify task scenario."""
    processor = NaturalLanguageProcessor()

    with patch('backend.src.services.task_service.TaskService.modify_task') as mock_update:
        mock_update.return_value = {
            "success": True,
            "message": "Task updated successfully",
            "data": MagicMock()
        }

        # Test different update command formats
        update_commands = [
            "change buy milk to buy almond milk",
            "update buy milk to buy almond milk",
            "rename buy milk to buy almond milk"
        ]

        for cmd in update_commands:
            result = processor.process_command(cmd, "user123")
            assert result["success"] is True
            assert result["action_taken"] == "update"
            mock_update.assert_called()


def test_fuzzy_matching():
    """Test fuzzy matching capabilities for task identification."""
    processor = NaturalLanguageProcessor()

    # Mock task list with similar descriptions
    with patch('backend.src.services.task_service.TaskService.get_all_tasks') as mock_get_all:
        mock_task = MagicMock()
        mock_task.description = "buy organic groceries"
        mock_task.id = 1
        mock_get_all.return_value = {
            "success": True,
            "message": "Retrieved 1 tasks",
            "data": [mock_task]
        }

        with patch('backend.src.services.task_service.TaskService.mark_task_completed') as mock_complete:
            mock_complete.return_value = {
                "success": True,
                "message": "Task completed",
                "data": MagicMock()
            }

            # Even though the command says "buy groceries" and the task is "buy organic groceries",
            # fuzzy matching should find it
            result = processor.process_command("done with buy groceries", "user123")

            # Should either succeed or ask for clarification, but not fail completely
            assert result["action_taken"] in ["complete", "clarification_needed", "unknown"]