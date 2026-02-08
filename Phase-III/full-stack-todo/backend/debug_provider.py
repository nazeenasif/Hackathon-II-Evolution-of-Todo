#!/usr/bin/env python3
"""Debug script to test provider configuration"""

import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from src.ai_providers.provider_factory import get_default_provider
from src.core.config import settings

print("=== Debug Provider Configuration ===")
print(f"Environment AI_PROVIDER: {os.getenv('AI_PROVIDER')}")
print(f"Settings AI_PROVIDER: {settings.AI_PROVIDER}")

try:
    print("Creating default provider...")
    provider = get_default_provider()
    print(f"Success! Provider type: {type(provider).__name__}")
    print("Provider creation successful!")
except Exception as e:
    print(f"Error creating provider: {e}")
    import traceback
    traceback.print_exc()