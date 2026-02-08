"""
MCP Server implementation for the Todo application.
Exposes task management operations as MCP-compliant tools for AI agents.
"""
import asyncio
from typing import Dict, Any, Optional

from .adapters.task_adapter import TaskAdapter


class MCPServer:
    """MCP Server that exposes task management tools for AI agents."""

    def __init__(self):
        try:
            from mcp.server import Server
            self.server = Server("todo-mcp-server")
        except ImportError:
            # Fallback when MCP SDK is not available
            self.server = None
        self.task_adapter = TaskAdapter()

    def get_tools(self):
        """Get all available MCP tools."""
        tools = {}

        # Add all tools from the tools module
        from .tools.add_task import get_add_task_tool
        from .tools.list_tasks import get_list_tasks_tool
        from .tools.update_task import get_update_task_tool
        from .tools.complete_task import get_complete_task_tool
        from .tools.delete_task import get_delete_task_tool

        tools['add_task'] = get_add_task_tool()
        tools['list_tasks'] = get_list_tasks_tool()
        tools['update_task'] = get_update_task_tool()
        tools['complete_task'] = get_complete_task_tool()
        tools['delete_task'] = get_delete_task_tool()

        return tools

    async def register_tools(self):
        """Register all tools with the MCP server."""
        if self.server is None:
            print("Warning: MCP SDK not available, skipping tool registration")
            return

        tools = self.get_tools()
        for tool_name, tool in tools.items():
            # Handle both actual Tool objects and dictionary representations
            if hasattr(tool, '__call__'):
                # If it's a callable, call it to get the actual tool
                actual_tool = tool()
                if isinstance(actual_tool, dict) and 'handler' in actual_tool:
                    # Register the handler separately if needed
                    self.server.add_tool(tool_name, actual_tool)
                    # Store the handler for later use
                    setattr(self.server, f"{tool_name}_handler", actual_tool['handler'])
                else:
                    self.server.add_tool(tool_name, actual_tool)
            else:
                self.server.add_tool(tool_name, tool)

    async def start(self, host: str = "localhost", port: int = 3000):
        """Start the MCP server."""
        if self.server is None:
            print("Error: Cannot start MCP server - MCP SDK not available")
            return

        await self.register_tools()
        print(f"MCP Server starting on {host}:{port}")
        await self.server.run_tcp(host, port)


# Global server instance for use in the application
mcp_server = MCPServer()


async def main():
    """Main entry point for the MCP server."""
    server_instance = MCPServer()
    await server_instance.start()


if __name__ == "__main__":
    asyncio.run(main())