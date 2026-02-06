# Data Model: AI Todo Assistant

## Task Entity

### Fields
- `id`: Integer (Primary Key, Auto-generated)
- `description`: String (Required, Max length: 500 characters)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime (Auto-generated on creation)
- `updated_at`: DateTime (Auto-generated on update)

### Validation Rules
- Description must be 1-500 characters
- Description cannot be empty or whitespace only
- Task ID must be valid (exists in database)

### State Transitions
- New Task → Pending (Initial state when created)
- Pending → Completed (When marked as done)
- Completed → Pending (When unmarked, if supported)

## User Intent Entity

### Fields
- `action_type`: Enum (add, list, complete, delete, update)
- `task_identifier`: String (Task description or ID for reference)
- `new_value`: String (New description for update actions, optional)

## MCP Tool Response Entity

### Fields
- `success`: Boolean (Indicates if the MCP tool call succeeded)
- `message`: String (Human-readable result message)
- `data`: Object (Response data from the tool, varies by tool type)
- `timestamp`: DateTime (When the response was generated)

## Relationships
- Tasks are managed exclusively through MCP tools
- Intent entities map to specific MCP tool calls
- Response entities provide feedback on tool execution outcomes