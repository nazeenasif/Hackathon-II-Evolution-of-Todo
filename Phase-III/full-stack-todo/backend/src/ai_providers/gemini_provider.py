from typing import List, Dict, Any, Optional
from .base_provider import BaseAIProvider, ToolCall, ChatResponse
import os
import json
import logging

logger = logging.getLogger(__name__)


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini implementation of the AI provider interface
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")

        # Import here to handle compatibility issues gracefully
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai package is required for Gemini provider. Install with: pip install google-generativeai")

        genai.configure(api_key=self.api_key)
        self.model_name = model

        # Initialize the model with function calling capability
        self.model = genai.GenerativeModel(model_name=self.model_name)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto",
        **kwargs
    ) -> ChatResponse:
        """
        Perform a chat completion using Google Gemini API.
        """
        try:
            # Prepare content for Gemini - separating system message
            contents = []
            system_instruction = None

            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "system":
                    system_instruction = content
                elif role == "user":
                    contents.append({"role": "user", "parts": [content]})
                elif role == "assistant":
                    contents.append({"role": "model", "parts": [content]})
                elif role == "tool":
                    # Handle tool results
                    contents.append({"role": "user", "parts": [f"Tool result: {content}"]})

            # Configure generation
            generation_config = {
                "temperature": kwargs.get("temperature", 0.7),
                "max_output_tokens": kwargs.get("max_tokens", 2048),
            }

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]

            # Prepare tools if available
            gemini_tools = None
            if tools and len(tools) > 0:
                gemini_tools = self._prepare_gemini_tools(tools)

            # Call the model with or without tools
            if gemini_tools:
                # Use the model with tools
                response = self.model.generate_content(
                    contents=contents,
                    tools=gemini_tools,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    system_instruction=system_instruction
                )
            else:
                # Use the model without tools
                response = self.model.generate_content(
                    contents=contents,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    system_instruction=system_instruction
                )

            # Extract content
            content = ""
            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                content += part.text or ""
                            elif hasattr(part, 'function_call'):
                                # Handle function calls in content
                                content += f"[Function call: {part.function_call.name}]"

            # Extract tool calls
            tool_calls = []
            if response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call'):
                                function_call = part.function_call

                                # Extract function name and arguments
                                function_name = function_call.name

                                # Convert arguments to dictionary
                                function_args = {}
                                if hasattr(function_call, 'args'):
                                    # Args is a proto-plus wrapper around a dict-like structure
                                    for key, value in function_call.args.items():
                                        function_args[key] = value

                                tool_calls.append(ToolCall(function_name, function_args))

            return ChatResponse(content=content, tool_calls=tool_calls)

        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise RuntimeError(f"Error calling Gemini API: {str(e)}")

    def _prepare_gemini_tools(self, tools: List[Dict[str, Any]]):
        """
        Prepare tools in Gemini format.
        """
        try:
            import google.generativeai as genai

            # Create function declarations
            function_declarations = []

            for tool in tools:
                if tool.get("type") == "function":
                    function_def = tool["function"]

                    # Create function declaration in the expected format
                    function_decl = genai.types.FunctionDeclaration(
                        name=function_def["name"],
                        description=function_def["description"],
                        parameters=function_def.get("parameters", {})
                    )
                    function_declarations.append(function_decl)

            if function_declarations:
                # Create Tool object with function declarations
                return [genai.types.Tool(
                    function_declarations=function_declarations
                )]
            else:
                return []

        except Exception as e:
            logger.warning(f"Could not prepare tools for Gemini: {e}")
            # Return empty list if tools preparation fails
            return []


def get_gemini_provider(model: str = "gemini-pro") -> GeminiProvider:
    """
    Helper function to get Gemini provider instance
    """
    return GeminiProvider(model=model)