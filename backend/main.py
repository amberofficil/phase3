# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the main FastAPI app
app = FastAPI(
    title="Todo Application Backend API",
    description="Backend API for the Todo Application with JWT authentication and AI Todo Assistant integration",
    version="1.0.0"
)

# -------------------------------
# CORS middleware
# -------------------------------
origins = [
    "http://172.22.64.1:3000",  # aapka frontend URL
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Include routes from your app
# -------------------------------
try:
    from routes import tasks
    app.include_router(tasks.router)
except ImportError:
    print("No tasks router found. Skipping tasks routes.")

# -------------------------------
# Include AI Todo Assistant API
# -------------------------------
try:
    # Delayed import to avoid reload conflicts
    from src.api.ai_todo_assistant import router as ai_todo_router
    app.include_router(ai_todo_router, prefix="/api/v1")
except ImportError:
    print("AI Todo Assistant router not found. Skipping AI routes.")

# -------------------------------
# Health check endpoint
# -------------------------------
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-backend"}

# -------------------------------
# Root endpoint
# -------------------------------
@app.get("/")
def read_root():
    return {"message": "Todo Application Backend API with AI Todo Assistant"}
