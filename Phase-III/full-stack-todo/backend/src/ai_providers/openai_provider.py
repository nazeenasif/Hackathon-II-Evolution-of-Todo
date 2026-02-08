from typing import List, Dict, Any, Optional
from .base_provider import BaseAIProvider, ToolCall, ChatResponse
from openai import OpenAI
import os
import json


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI implementation of the AI provider interface
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto",
        **kwargs
    ) -> ChatResponse:
        """
        Perform a chat completion using OpenAI API.
        """
        try:
            # Prepare the API call parameters
            params = {
                "model": self.model,
                "messages": messages
            }

            # Add tools if provided
            if tools:
                params["tools"] = tools
                params["tool_choice"] = tool_choice

            # Add any additional parameters
            params.update(kwargs)

            # Call OpenAI API
            response = self.client.chat.completions.create(**params)

            # Extract the response message
            response_message = response.choices[0].message

            # Extract content
            content = response_message.content or ""

            # Extract tool calls
            tool_calls = []
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    tool_calls.append(ToolCall(function_name, function_args))

            return ChatResponse(content=content, tool_calls=tool_calls)

        except Exception as e:
            raise RuntimeError(f"Error calling OpenAI API: {str(e)}")


def get_openai_provider(model: str = "gpt-3.5-turbo") -> OpenAIProvider:
    """
    Helper function to get OpenAI provider instance
    """
    return OpenAIProvider(model=model)