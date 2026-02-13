from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json


class BaseAIProvider(ABC):
    """
    Abstract base class for AI providers (OpenAI, Cohere, etc.)
    """

    @abstractmethod
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform a chat completion with the AI model.

        Args:
            messages: List of messages in the conversation
            tools: List of available tools/functions
            tool_choice: How to handle tool selection ("auto", "required", "none", or specific tool)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dictionary containing the AI response with potential tool calls
        """
        pass


class ToolCall:
    """
    Represents a tool call extracted from AI response
    """
    def __init__(self, name: str, arguments: Dict[str, Any]):
        self.name = name
        self.arguments = arguments

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments
        }


class ChatResponse:
    """
    Standardized response from AI provider
    """
    def __init__(self, content: str, tool_calls: List[ToolCall] = None):
        self.content = content
        self.tool_calls = tool_calls or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "tool_calls": [tc.to_dict() for tc in self.tool_calls]
        }