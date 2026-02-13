#!/usr/bin/env python3
"""
Test script to verify bcrypt functionality
"""

from passlib.context import CryptContext

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    # Test hashing a simple password
    test_password = "test123"
    print(f"Testing password: {test_password}")

    hashed = pwd_context.hash(test_password)
    print(f"Hashed successfully: {hashed[:20]}...")

    # Test verification
    is_valid = pwd_context.verify(test_password, hashed)
    print(f"Verification result: {is_valid}")

    print("Bcrypt functionality test passed!")

except Exception as e:
    print(f"Error during bcrypt test: {e}")
    import traceback
    traceback.print_exc()