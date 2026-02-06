"""
Basic FastAPI application structure for the AI Todo Assistant.
"""
from .ai_todo_assistant import router

from fastapi import FastAPI
from .ai_todo_assistant import router as ai_todo_router

# Create the main FastAPI app
app = FastAPI(
    title="AI Todo Assistant API",
    description="API for the AI-powered Todo Assistant that processes natural language commands",
    version="1.0.0"
)

# Include the AI Todo Assistant router
app.include_router(ai_todo_router, prefix="/api/v1", tags=["ai-todo"])