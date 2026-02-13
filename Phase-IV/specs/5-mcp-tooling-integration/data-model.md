# Data Model: MCP Server & Tooling Integration

## MCP Tool Parameters and Responses

### Add Task Tool
**Input Parameters**:
- `title`: string (required) - Task title
- `description`: string (optional) - Task description
- `due_date`: string (optional) - Due date in ISO 8601 format
- `priority`: string (optional) - Priority level (low, medium, high)
- `tags`: array of strings (optional) - Task tags

**Response**:
- `success`: boolean - Whether the operation succeeded
- `task_id`: integer - ID of the created task
- `error`: string (optional) - Error message if operation failed

### List Tasks Tool
**Input Parameters**:
- `status`: string (optional) - Filter by status (all, pending, completed)
- `limit`: integer (optional) - Maximum number of tasks to return
- `offset`: integer (optional) - Offset for pagination
- `sort_by`: string (optional) - Sort field (created_at, due_date, priority)
- `order`: string (optional) - Sort order (asc, desc)

**Response**:
- `success`: boolean - Whether the operation succeeded
- `tasks`: array of task objects - List of tasks matching criteria
- `total_count`: integer - Total number of tasks matching criteria
- `error`: string (optional) - Error message if operation failed

### Update Task Tool
**Input Parameters**:
- `task_id`: integer (required) - ID of the task to update
- `title`: string (optional) - New task title
- `description`: string (optional) - New task description
- `due_date`: string (optional) - New due date in ISO 8601 format
- `priority`: string (optional) - New priority level
- `tags`: array of strings (optional) - New task tags

**Response**:
- `success`: boolean - Whether the operation succeeded
- `task_id`: integer - ID of the updated task
- `error`: string (optional) - Error message if operation failed

### Complete Task Tool
**Input Parameters**:
- `task_id`: integer (required) - ID of the task to mark as complete

**Response**:
- `success`: boolean - Whether the operation succeeded
- `task_id`: integer - ID of the completed task
- `error`: string (optional) - Error message if operation failed

### Delete Task Tool
**Input Parameters**:
- `task_id`: integer (required) - ID of the task to delete

**Response**:
- `success`: boolean - Whether the operation succeeded
- `task_id`: integer - ID of the deleted task
- `error`: string (optional) - Error message if operation failed

## Task Object Structure
All tools that return task information use this consistent structure:

- `id`: integer - Unique task identifier
- `title`: string - Task title
- `description`: string - Task description
- `status`: string - Task status (pending, completed)
- `due_date`: string - Due date in ISO 8601 format
- `priority`: string - Priority level (low, medium, high)
- `tags`: array of strings - Task tags
- `created_at`: string - Creation timestamp in ISO 8601 format
- `updated_at`: string - Last update timestamp in ISO 8601 format
- `user_id`: integer - ID of the user who owns the task

## Error Response Structure
All tools use this consistent error response structure:

- `success`: boolean - Always false for error responses
- `error`: string - Human-readable error message
- `error_code`: string - Machine-readable error code
- `details`: object (optional) - Additional error details