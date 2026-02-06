"""
Task service layer for the AI Todo Assistant.
Handles business logic for task operations, using MCP tools for data persistence.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from .mcp_tools import add_task, list_tasks, complete_task, delete_task, update_task


class TaskService:
    """Service layer for handling task business logic."""

    @staticmethod
    def create_task(description: str) -> Dict[str, Any]:
        """
        Create a new task using the add_task MCP tool.

        Args:
            description: The description of the task to create

        Returns:
            Result from the MCP tool
        """
        # Validate input
        if not description or description.strip() == "":
            return {
                "success": False,
                "message": "Task description cannot be empty",
                "data": None
            }

        if len(description) > 500:
            return {
                "success": False,
                "message": "Task description exceeds 500 character limit",
                "data": None
            }

        # Use MCP tool to add the task
        return add_task(description)

    @staticmethod
    def get_all_tasks(completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get all tasks or filter by completion status.

        Args:
            completed: If provided, filter tasks by completion status (True=completed, False=pending)

        Returns:
            Result from the MCP tool
        """
        # Use MCP tool to list tasks
        return list_tasks(completed)

    @staticmethod
    def mark_task_completed(task_identifier: str) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            task_identifier: The description or ID of the task to complete

        Returns:
            Result from the MCP tool
        """
        # Validate input
        if not task_identifier:
            return {
                "success": False,
                "message": "Task identifier cannot be empty",
                "data": None
            }

        # Use MCP tool to complete the task
        return complete_task(task_identifier)

    @staticmethod
    def remove_task(task_identifier: str) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            task_identifier: The description or ID of the task to delete

        Returns:
            Result from the MCP tool
        """
        # Validate input
        if not task_identifier:
            return {
                "success": False,
                "message": "Task identifier cannot be empty",
                "data": None
            }

        # Use MCP tool to delete the task
        return delete_task(task_identifier)

    @staticmethod
    def modify_task(old_task_identifier: str, new_description: str) -> Dict[str, Any]:
        """
        Update a task's description.

        Args:
            old_task_identifier: The current description or ID of the task to update
            new_description: The new description for the task

        Returns:
            Result from the MCP tool
        """
        # Validate inputs
        if not old_task_identifier:
            return {
                "success": False,
                "message": "Old task identifier cannot be empty",
                "data": None
            }

        if not new_description or new_description.strip() == "":
            return {
                "success": False,
                "message": "New task description cannot be empty",
                "data": None
            }

        if len(new_description) > 500:
            return {
                "success": False,
                "message": "New task description exceeds 500 character limit",
                "data": None
            }

        # Use MCP tool to update the task
        return update_task(old_task_identifier, new_description)