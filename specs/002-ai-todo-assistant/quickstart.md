# Quickstart Guide: AI Todo Assistant

## Overview
The AI Todo Assistant allows users to manage their tasks using natural language commands. It operates statelessly via MCP tools to interact with the database.

## Supported Commands

### Adding Tasks
- "add [task description]"
- "create [task description]"
- "remember [task description]"

### Listing Tasks
- "show my tasks"
- "list tasks"
- "see my todos"
- "what do I need to do?"

### Completing Tasks
- "done [task description]"
- "complete [task description]"
- "finished [task description]"

### Deleting Tasks
- "delete [task description]"
- "remove [task description]"
- "cancel [task description]"

### Updating Tasks
- "change [task description] to [new description]"
- "update [task description] to [new description]"
- "rename [task description] to [new description]"

## Example Conversations

### Adding a Task
User: "Add buy groceries"
AI: "Task 'buy groceries' added successfully."

### Listing Tasks
User: "Show my tasks"
AI: "Here are your tasks: 1. Buy groceries [pending] 2. Call mom [pending]"

### Completing a Task
User: "Done with buy groceries"
AI: "Task 'buy groceries' marked as complete."

### Handling Ambiguity
User: "Remove the task"
AI: "Which task would you like to remove? Here are your current tasks: 1. Buy groceries 2. Call mom"

## Error Handling
- If a task doesn't exist: The AI will apologize and explain the task wasn't found
- If a request is unclear: The AI will ask for clarification or list available tasks
- All errors are handled gracefully without exposing technical details