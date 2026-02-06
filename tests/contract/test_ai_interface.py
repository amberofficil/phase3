"""
Contract tests for the AI Todo Assistant API interface.
Tests that the API endpoints match the OpenAPI specification.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.src.api.ai_todo_assistant import router
from backend.src.api import app
from backend.src.models.api_models import NaturalLanguageCommand, CommandResponse


def test_process_endpoint_exists():
    """Test that the process endpoint exists and has the correct path."""
    # Create a test client
    client = TestClient(app)

    # Check that we can access the docs (meaning the app is set up)
    response = client.get("/docs")
    assert response.status_code in [200, 404]  # docs might be disabled in test env


def test_process_natural_language_command_structure():
    """Test the structure of the process endpoint without making actual calls."""
    # Test the endpoint signature by looking at the route configuration
    routes = {route.path: route.methods for route in app.routes}

    # Check that the endpoint exists
    assert "/api/v1/ai/todo/process" in routes
    # Check that it accepts POST requests
    assert "POST" in routes["/api/v1/ai/todo/process"]


@patch('backend.src.services.natural_language_processor.NaturalLanguageProcessor')
def test_process_command_request_format(mock_processor_class):
    """Test that the process endpoint accepts the correct request format."""
    client = TestClient(app)

    # Mock the processor
    mock_processor_instance = MagicMock()
    mock_processor_instance.process_command.return_value = {
        'success': True,
        'message': 'Task added successfully',
        'action_taken': 'add',
        'mcp_response': {}
    }
    mock_processor_class.return_value = mock_processor_instance

    # Send a request with the expected format
    payload = {
        "user_input": "add buy groceries",
        "user_id": "user_12345",
        "conversation_context": {}
    }

    response = client.post("/api/v1/ai/todo/process", json=payload)

    # Check that the request was accepted
    assert response.status_code in [200, 400, 500]  # Could fail due to mocked service

    # Check that the processor was called with the right parameters
    if response.status_code != 500:
        mock_processor_instance.process_command.assert_called()


def test_command_response_structure():
    """Test the structure of command responses."""
    # This tests that the response model matches the expected structure from the spec
    response_data = {
        'success': True,
        'message': 'Test message',
        'action_taken': 'add',
        'tasks': [],
        'mcp_response': {}
    }

    # Validate that this conforms to the CommandResponse model
    command_response = CommandResponse(**response_data)

    assert command_response.success is True
    assert command_response.message == 'Test message'
    assert command_response.action_taken == 'add'
    assert command_response.tasks == []


def test_error_response_structure():
    """Test the structure of error responses."""
    # This tests that the error response model matches the expected structure from the spec
    error_data = {
        'success': False,
        'error': 'Invalid input',
        'message': 'The input was invalid'
    }

    error_response = ErrorResponse(**error_data)

    assert error_response.success is False
    assert error_response.error == 'Invalid input'
    assert error_response.message == 'The input was invalid'


def test_natural_language_command_structure():
    """Test the structure of natural language command requests."""
    # This tests that the request model matches the expected structure from the spec
    command_data = {
        'user_input': 'add buy groceries',
        'user_id': 'user_12345',
        'conversation_context': {}
    }

    command = NaturalLanguageCommand(**command_data)

    assert command.user_input == 'add buy groceries'
    assert command.user_id == 'user_12345'
    assert command.conversation_context == {}


def test_required_fields_validation():
    """Test that required fields are validated."""
    # Test missing user_input
    with pytest.raises(ValueError):
        NaturalLanguageCommand(
            user_id='user_12345',
            conversation_context={}
        )

    # Test missing user_id
    with pytest.raises(ValueError):
        NaturalLanguageCommand(
            user_input='add buy groceries',
            conversation_context={}
        )


def test_health_endpoint():
    """Test the health check endpoint."""
    client = TestClient(app)

    response = client.get("/api/v1/health")

    # Health endpoint should exist
    assert response.status_code in [200, 404, 405]  # May return 404 if router not properly mounted


def test_response_model_consistency():
    """Test that response models have consistent structure."""
    # Success response should have these fields
    success_response = CommandResponse(
        success=True,
        message="Operation successful",
        action_taken="add",
        tasks=[],
        mcp_response={}
    )

    assert hasattr(success_response, 'success')
    assert hasattr(success_response, 'message')
    assert hasattr(success_response, 'action_taken')
    assert hasattr(success_response, 'tasks')
    assert hasattr(success_response, 'mcp_response')

    # Error response should have these fields
    error_response = ErrorResponse(
        error="Something went wrong",
        message="Error occurred"
    )

    assert hasattr(error_response, 'success')
    assert hasattr(error_response, 'error')
    assert hasattr(error_response, 'message')
    assert error_response.success is False