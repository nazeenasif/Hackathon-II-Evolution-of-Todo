# MCP Server Quickstart Guide

This guide will help you set up and run the MCP server for the todo application.

## Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- The todo backend application must be running and accessible

## Installation

1. Navigate to the backend directory:
   ```bash
   cd full-stack-todo/backend
   ```

2. Install the required dependencies (including MCP SDK):
   ```bash
   pip install -r requirements.txt
   ```

   Or if using Poetry:
   ```bash
   poetry install
   ```

## Running the MCP Server

1. Start the MCP server:
   ```bash
   python -m src.mcp_server.server
   ```

2. The server will start on `localhost:3000` by default.

## Testing the Server

You can test the server using the following steps:

1. Once the server is running, you can use an MCP client to connect to it.
2. The server exposes the following tools:
   - `add_task`: Create new tasks
   - `list_tasks`: List existing tasks
   - `update_task`: Update existing tasks
   - `complete_task`: Mark tasks as completed
   - `delete_task`: Delete tasks

## Example Usage

The MCP server allows AI agents to interact with your todo system using natural language. For example, an AI agent could:
- "Create a task called 'Buy groceries' with high priority"
- "Show me all pending tasks"
- "Mark task #5 as completed"
- "Update the due date for task #3"

## Troubleshooting

- If the server fails to start, ensure that the backend database is accessible
- Check that all required dependencies are installed
- Verify that the port 3000 is not already in use