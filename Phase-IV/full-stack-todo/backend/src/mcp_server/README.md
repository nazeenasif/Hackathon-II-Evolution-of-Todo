# MCP Server Module for Todo Application

This module implements an MCP (Model Context Protocol) server that exposes todo task operations as standardized tools for AI agents.

## Overview

The MCP server provides a standardized interface for AI agents to interact with the todo application. It exposes common task operations as tools that can be invoked by AI agents to create, retrieve, update, and manage tasks.

## Tools Available

### 1. add_task
- **Description**: Create a new task in the todo system
- **Parameters**:
  - `title` (string, required): Task title
  - `description` (string, optional): Task description
  - `due_date` (string, optional): Due date in ISO 8601 format
  - `priority` (string, optional): Priority level (low, medium, high; defaults to medium)
  - `tags` (array, optional): Task tags (max 10)

### 2. list_tasks
- **Description**: List tasks in the todo system with optional filters
- **Parameters**:
  - `status` (string, optional): Filter by status (all, pending, completed; defaults to all)
  - `limit` (integer, optional): Max number of tasks to return (1-100; defaults to 20)
  - `offset` (integer, optional): Offset for pagination (defaults to 0)
  - `sort_by` (string, optional): Field to sort by (created_at, due_date, priority, title; defaults to created_at)
  - `order` (string, optional): Sort order (asc, desc; defaults to desc)

### 3. update_task
- **Description**: Update an existing task in the todo system
- **Parameters**:
  - `task_id` (integer, required): Task ID to update
  - `title` (string, optional): New task title
  - `description` (string, optional): New task description
  - `due_date` (string, optional): New due date in ISO 8601 format
  - `priority` (string, optional): New priority level (low, medium, high)
  - `tags` (array, optional): New task tags (max 10)

### 4. complete_task
- **Description**: Mark a task as completed in the todo system
- **Parameters**:
  - `task_id` (integer, required): Task ID to complete

### 5. delete_task
- **Description**: Delete a task from the todo system
- **Parameters**:
  - `task_id` (integer, required): Task ID to delete

## Architecture

The MCP server follows a layered architecture:

1. **Tools Layer**: Implements individual MCP tools with validation and error handling
2. **Adapters Layer**: Bridges MCP tools with existing backend services
3. **Backend Services**: Reuses existing task management functionality

## Security

- Authentication is handled via the `require_auth` decorator
- All operations are user-scoped (users can only operate on their own tasks)
- Input validation is performed on all parameters

## Testing

Unit and integration tests are available in the `tests/mcp_integration/` directory. Run them using:

```bash
pytest tests/mcp_integration/
```

## Running the Server

To start the MCP server:

```bash
cd full-stack-todo/backend
python -m src.mcp_server.server
```

The server will start on localhost:3000 by default.