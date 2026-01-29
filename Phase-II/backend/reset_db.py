#!/usr/bin/env python3
"""
Script to reset the database by dropping and recreating all tables.
"""

from sqlmodel import SQLModel
from src.core.database import engine
from src.models.user import User
from src.models.task import Task

def reset_database():
    """Drop all tables and recreate them."""
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("All tables dropped.")

    print("Creating all tables...")
    SQLModel.metadata.create_all(engine)
    print("All tables created.")

    print("Database reset complete!")

if __name__ == "__main__":
    reset_database()