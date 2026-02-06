"""
Pydantic models for API requests and responses in the AI Todo Assistant.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Request Models
class NaturalLanguageCommand(BaseModel):
    """Request model for natural language commands to the AI assistant."""
    user_input: str = Field(..., description="The natural language command from the user", example="add buy groceries")
    user_id: str = Field(..., description="The ID of the user making the request", example="user_12345")
    conversation_context: Optional[dict] = Field(default=None, description="Optional conversation history for context")


# Response Models
class TaskResponse(BaseModel):
    """Response model for task data."""
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class CommandResponse(BaseModel):
    """Response model for command processing results."""
    success: bool
    message: str
    action_taken: str
    tasks: Optional[List[TaskResponse]] = None
    mcp_response: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    success: bool = False
    error: str
    message: str


# MCP Tool Response Models
class MCPTaskResponse(BaseModel):
    """Response model from MCP tools for task operations."""
    success: bool
    message: str
    data: Optional[TaskResponse] = None


class MCPTasksResponse(BaseModel):
    """Response model from MCP tools for listing operations."""
    success: bool
    message: str
    data: Optional[List[TaskResponse]] = None