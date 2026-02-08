from typing import List, Dict, Any, Optional
from .base_provider import BaseAIProvider, ToolCall, ChatResponse
import cohere
import os
import json
import logging

logger = logging.getLogger(__name__)


class CohereProvider(BaseAIProvider):
    """
    Cohere implementation of the AI provider interface
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "command-nightly"):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Cohere API key is required. Set COHERE_API_KEY environment variable.")
        self.model = model
        self.client = cohere.Client(api_key=self.api_key)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto",
        **kwargs
    ) -> ChatResponse:
        """
        Perform a chat completion using Cohere API.
        """
        try:
            # Separate system message from other messages
            system_message = None
            user_assistant_messages = []

            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "system":
                    system_message = content
                else:
                    # Map roles to Cohere format
                    cohere_role = "USER" if role == "user" else "CHATBOT"
                    user_assistant_messages.append({
                        "role": cohere_role,
                        "message": content
                    })

            # Prepare tools for Cohere
            cohere_tools = []
            if tools:
                for tool in tools:
                    if tool.get("type") == "function":
                        function_def = tool["function"]

                        # Convert OpenAI function format to Cohere tool format
                        cohere_tool = {
                            "name": function_def["name"],
                            "description": function_def["description"],
                            "parameter_definitions": {}
                        }

                        # Convert parameters to Cohere format
                        params = function_def.get("parameters", {}).get("properties", {})
                        required_params = function_def.get("parameters", {}).get("required", [])

                        for param_name, param_info in params.items():
                            cohere_param = {
                                "type": param_info.get("type", "string"),
                                "description": param_info.get("description", ""),
                            }

                            # Handle enum values
                            if "enum" in param_info:
                                cohere_param["enum"] = param_info["enum"]

                            # Handle default values
                            if "default" in param_info:
                                cohere_param["default"] = param_info["default"]

                            # Mark as required if it's in the required list
                            cohere_param["required"] = param_name in required_params

                            cohere_tool["parameter_definitions"][param_name] = cohere_param

                        cohere_tools.append(cohere_tool)

            # Prepare the API call parameters
            params = {
                "message": user_assistant_messages[-1]["message"] if user_assistant_messages else "Hello",
                "chat_history": user_assistant_messages[:-1] if len(user_assistant_messages) > 1 else [],
                "model": self.model,
                "tools": cohere_tools if cohere_tools else [],
                "connectors": []  # Empty connectors list to avoid internet search
            }

            # Add preamble if system message exists
            if system_message:
                params["preamble"] = system_message

            # Add any additional parameters from kwargs
            for key, value in kwargs.items():
                if key not in ["message", "chat_history", "model", "tools", "preamble", "connectors"]:
                    params[key] = value

            # Call Cohere API
            response = self.client.chat(**params)

            # Extract content
            content = response.text or ""

            # Extract tool calls
            tool_calls = []
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    # Extract function name and arguments
                    if hasattr(tool_call, 'name') and hasattr(tool_call, 'parameters'):
                        function_name = tool_call.name
                        # Ensure parameters is a dict, not a string
                        if isinstance(tool_call.parameters, str):
                            try:
                                function_args = json.loads(tool_call.parameters)
                            except json.JSONDecodeError:
                                function_args = {}
                        else:
                            function_args = tool_call.parameters or {}
                        tool_calls.append(ToolCall(function_name, function_args))
                    elif hasattr(tool_call, 'name') and hasattr(tool_call, 'arguments'):
                        # Alternative attribute names
                        function_name = tool_call.name
                        # Ensure arguments is a dict, not a string
                        if isinstance(tool_call.arguments, str):
                            try:
                                function_args = json.loads(tool_call.arguments)
                            except json.JSONDecodeError:
                                function_args = {}
                        else:
                            function_args = tool_call.arguments or {}
                        tool_calls.append(ToolCall(function_name, function_args))

            return ChatResponse(content=content, tool_calls=tool_calls)

        except Exception as e:
            logger.error(f"Error calling Cohere API: {str(e)}")
            raise RuntimeError(f"Error calling Cohere API: {str(e)}")


def get_cohere_provider(model: str = "command-nightly") -> CohereProvider:
    """
    Helper function to get Cohere provider instance
    """
    return CohereProvider(model=model)