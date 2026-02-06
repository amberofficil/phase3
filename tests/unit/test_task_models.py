"""
Unit tests for the Task model in the AI Todo Assistant.
"""

import pytest
from datetime import datetime
from backend.src.models.task import Task, TaskBase


def test_task_base_creation():
    """Test creating a TaskBase instance."""
    task_base = TaskBase(description="Test task", completed=False)

    assert task_base.description == "Test task"
    assert task_base.completed is False


def test_task_base_validation():
    """Test validation rules for TaskBase."""
    # Test minimum length validation
    with pytest.raises(ValueError):
        TaskBase(description="", completed=False)

    # Test maximum length validation
    long_description = "x" * 501
    with pytest.raises(ValueError):
        TaskBase(description=long_description, completed=False)


def test_task_creation():
    """Test creating a Task instance."""
    task = Task(description="Test task", completed=False)

    assert task.description == "Test task"
    assert task.completed is False
    assert task.id is None  # Will be set by database


def test_task_str_representation():
    """Test string representation of Task."""
    task = Task(description="Buy groceries", completed=False)
    assert "Buy groceries [pending]" in str(task)

    task.completed = True
    assert "Buy groceries [completed]" in str(task)


def test_task_defaults():
    """Test default values for Task."""
    task = Task(description="Test task")

    assert task.completed is False  # Default value
    assert task.description == "Test task"


def test_task_table_metadata():
    """Test that Task is properly configured as a table."""
    # Verify that the Task class has the required table attributes
    assert hasattr(Task, '__table__') or Task.__dict__.get('__tablename__')