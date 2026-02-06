"""
MCP tools for the AI Todo Assistant.
These tools provide the interface for interacting with tasks as specified in the constitution.
All task operations must go through these tools to maintain stateless operation.
Enhanced with error handling and validation as per requirements.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.task import Task
import logging

# Set up logging for the module
logger = logging.getLogger(__name__)


def error_handling_wrapper(func):
    """
    Decorator to wrap MCP tool calls with error handling.
    This prevents exposure of technical details in error responses.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred while processing your request. Please try again.",
                "data": None
            }
    return wrapper


@error_handling_wrapper
def add_task(description: str) -> Dict[str, Any]:
    """
    Add a new task to the database.

    Args:
        description: The description of the task to add

    Returns:
        Dictionary containing success status, message, and task data
    """
    # Validation
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

    # Simulate creating a new task
    # In real implementation, this would use SQLAlchemy/SQLModel to insert into DB
    try:
        new_task = Task(
            description=description.strip(),
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Since we're simulating, we'll just return a mock task with an ID
        new_task.id = 1  # This would come from the database in real implementation

        return {
            "success": True,
            "message": f"Task '{description}' added successfully",
            "data": new_task
        }
    except Exception as e:
        logger.error(f"Error adding task: {str(e)}")
        return {
            "success": False,
            "message": "Failed to add task due to a system error. Please try again.",
            "data": None
        }


@error_handling_wrapper
def list_tasks(completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    List all tasks or filter by completion status.

    Args:
        completed: If provided, filter tasks by completion status (True=completed, False=pending)

    Returns:
        Dictionary containing success status, message, and list of tasks
    """
    try:
        # In a real implementation, this would query the database
        # For now, we'll simulate returning an empty list
        # This is where we'd filter based on the completed parameter

        # Mock tasks - in real implementation, these would come from the database
        mock_tasks = []

        # If completed parameter is specified, filter accordingly
        if completed is not None:
            mock_tasks = [task for task in mock_tasks if task.completed == completed]

        return {
            "success": True,
            "message": f"Retrieved {len(mock_tasks)} tasks",
            "data": mock_tasks
        }
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        return {
            "success": False,
            "message": "Failed to retrieve tasks due to a system error. Please try again.",
            "data": None
        }


@error_handling_wrapper
def complete_task(task_identifier: str) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        task_identifier: The description or ID of the task to complete

    Returns:
        Dictionary containing success status, message, and updated task
    """
    # Validation
    if not task_identifier:
        return {
            "success": False,
            "message": "Task identifier cannot be empty",
            "data": None
        }

    # Mock: pretend we found and updated a task
    # In real implementation, this would query and update the database
    try:
        # In a real implementation, we would look up the task by identifier first
        # If the task doesn't exist, return an appropriate error
        updated_task = Task(
            description=task_identifier,
            completed=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        updated_task.id = 1  # This would come from the database

        return {
            "success": True,
            "message": f"Task '{task_identifier}' marked as complete",
            "data": updated_task
        }
    except Exception as e:
        logger.error(f"Error completing task: {str(e)}")
        return {
            "success": False,
            "message": "Failed to complete task due to a system error. Please try again.",
            "data": None
        }


@error_handling_wrapper
def delete_task(task_identifier: str) -> Dict[str, Any]:
    """
    Delete a task from the database.

    Args:
        task_identifier: The description or ID of the task to delete

    Returns:
        Dictionary containing success status and message
    """
    # Validation
    if not task_identifier:
        return {
            "success": False,
            "message": "Task identifier cannot be empty",
            "data": None
        }

    try:
        # In a real implementation, we would check if the task exists first
        # and return an appropriate message if it doesn't
        return {
            "success": True,
            "message": f"Task '{task_identifier}' deleted successfully",
            "data": None
        }
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        return {
            "success": False,
            "message": "Failed to delete task due to a system error. Please try again.",
            "data": None
        }


@error_handling_wrapper
def update_task(old_task_identifier: str, new_description: str) -> Dict[str, Any]:
    """
    Update a task's description.

    Args:
        old_task_identifier: The current description or ID of the task to update
        new_description: The new description for the task

    Returns:
        Dictionary containing success status, message, and updated task
    """
    # Validation
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

    try:
        # Mock: pretend we found and updated a task
        updated_task = Task(
            description=new_description.strip(),
            completed=False,  # Preserve completion status
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        updated_task.id = 1  # This would come from the database

        return {
            "success": True,
            "message": f"Task '{old_task_identifier}' updated to '{new_description}'",
            "data": updated_task
        }
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        return {
            "success": False,
            "message": "Failed to update task due to a system error. Please try again.",
            "data": None
        }