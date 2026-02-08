from typing import Optional
from .base_provider import BaseAIProvider
from .openai_provider import OpenAIProvider
from .cohere_provider import CohereProvider
from .gemini_provider import GeminiProvider
import os
from src.core.config import settings


class AIProviderFactory:
    """
    Factory class to create AI provider instances based on configuration
    """

    @staticmethod
    def create_provider(provider_name: Optional[str] = None, model: Optional[str] = None) -> BaseAIProvider:
        """
        Create an AI provider instance based on the provider name or environment configuration.

        Args:
            provider_name: Name of the provider ('openai', 'cohere', or None to use environment)
            model: Model name to use (defaults will be used if not provided)

        Returns:
            BaseAIProvider instance
        """
        if not provider_name:
            # Default to environment variable, then to settings default
            provider_name = os.getenv("AI_PROVIDER", settings.AI_PROVIDER).lower()

        provider_name = provider_name.lower()

        if provider_name == "openai":
            model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            return OpenAIProvider(model=model)

        elif provider_name == "cohere":
            model = model or os.getenv("COHERE_MODEL", "command-nightly")
            return CohereProvider(model=model)

        elif provider_name == "gemini":
            model = model or os.getenv("GEMINI_MODEL", "gemini-pro")
            return GeminiProvider(model=model)

        else:
            raise ValueError(f"Unsupported AI provider: {provider_name}. Supported: 'openai', 'cohere', 'gemini'")

    @staticmethod
    def get_available_providers() -> list:
        """
        Get list of available providers
        """
        return ["openai", "cohere", "gemini"]


def get_default_provider() -> BaseAIProvider:
    """
    Helper function to get the default configured provider
    """
    return AIProviderFactory.create_provider()


def get_provider(provider_name: str, model: Optional[str] = None) -> BaseAIProvider:
    """
    Helper function to get a specific provider
    """
    return AIProviderFactory.create_provider(provider_name, model)