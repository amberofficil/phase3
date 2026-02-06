# AI Todo Assistant

An AI-powered Todo Assistant that processes natural language commands to manage your tasks. Built with FastAPI backend and React frontend.

## Features

- Natural language processing for task management
- Add, list, complete, delete, and update tasks using plain English
- Smart intent recognition with fuzzy matching
- Clarification for ambiguous requests
- User-friendly error handling
- Chat-like interface for seamless interaction

## Architecture

### Backend (Python/FastAPI)
- **Natural Language Processor**: Handles intent recognition and command processing
- **MCP Tools**: Interface for task operations (add, list, complete, delete, update)
- **Task Service**: Business logic layer
- **Models**: Data models and validation

### Frontend (React)
- **TodoInterface**: Chat-like component for user interaction
- **AI Todo Client**: Service for API communication
- **Styling**: CSS modules for responsive design

## Installation

1. Clone the repository
2. Navigate to the backend directory: `cd backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Navigate to the frontend directory: `cd ../frontend`
7. Install dependencies: `npm install`

## Usage

### Backend
1. Navigate to the backend directory
2. Activate your virtual environment
3. Start the server: `uvicorn src.api:app --reload`
4. The API will be available at `http://localhost:8000`

### Frontend
1. Navigate to the frontend directory
2. Start the development server: `npm run dev`
3. Access the application in your browser

## API Endpoints

- `POST /api/v1/ai/todo/process` - Process natural language commands
- `GET /api/v1/health` - Health check

## Supported Commands

### Adding Tasks
- "add buy groceries"
- "create call mom"
- "remember walk the dog"

### Listing Tasks
- "show my tasks"
- "list tasks"
- "what do I need to do?"

### Completing Tasks
- "done with buy groceries"
- "complete call mom"
- "mark walk the dog as done"

### Deleting Tasks
- "delete buy groceries"
- "remove call mom"
- "cancel walk the dog"

### Updating Tasks
- "change buy groceries to buy organic groceries"
- "update call mom to call parents"
- "rename walk the dog to walk the puppy"

## Testing

Run backend tests with:
```
cd backend
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT"# phase3" 
