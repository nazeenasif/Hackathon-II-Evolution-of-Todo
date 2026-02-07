# Quickstart: MCP Server & Tooling Integration

## Overview
This guide explains how to set up and use the MCP (Model Context Protocol) server that exposes todo task operations as standardized tools for AI agents.

## Prerequisites
- Python 3.11+
- Existing backend services running (FastAPI, SQLModel, Neon PostgreSQL)
- MCP-compatible AI agent

## Installation
1. Install the MCP server module in your backend:
   ```bash
   pip install mcp-sdk  # Official MCP SDK
   ```

2. The MCP server will be integrated into the existing backend application

## Running the MCP Server
The MCP server runs as part of the main backend application:
```bash
cd backend
python -m src.mcp_server.server
```

Or run the entire application which includes the MCP server:
```bash
cd backend
uvicorn src.main:app --reload
```

## Using MCP Tools
Once the server is running, AI agents can connect to the MCP server and use the following tools:

### add_task
Create a new task:
```json
{
  "method": "tools/call",
  "params": {
    "name": "add_task",
    "arguments": {
      "title": "Buy groceries",
      "description": "Milk, bread, eggs",
      "priority": "medium"
    }
  }
}
```

### list_tasks
Retrieve a list of tasks:
```json
{
  "method": "tools/call",
  "params": {
    "name": "list_tasks",
    "arguments": {
      "status": "pending",
      "limit": 10
    }
  }
}
```

### update_task
Update an existing task:
```json
{
  "method": "tools/call",
  "params": {
    "name": "update_task",
    "arguments": {
      "task_id": 123,
      "title": "Updated task title",
      "priority": "high"
    }
  }
}
```

### complete_task
Mark a task as completed:
```json
{
  "method": "tools/call",
  "params": {
    "name": "complete_task",
    "arguments": {
      "task_id": 123
    }
  }
}
```

### delete_task
Delete a task:
```json
{
  "method": "tools/call",
  "params": {
    "name": "delete_task",
    "arguments": {
      "task_id": 123
    }
  }
}
```

## Testing
Run the MCP integration tests to verify everything works correctly:
```bash
cd backend
pytest tests/mcp_integration/
```

## Troubleshooting
- If tools are not available, ensure the MCP server is properly started
- Check that the AI agent is connecting to the correct MCP endpoint
- Verify that authentication tokens are being passed correctly for protected operations