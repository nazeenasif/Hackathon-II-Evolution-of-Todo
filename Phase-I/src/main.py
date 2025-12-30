"""
Main entry point for the In-Memory Python Console Todo Application.

This application provides core functionality for adding, viewing, updating,
deleting, and marking tasks as complete/incomplete through a numbered menu interface.
All data is stored in memory only as required by the constitution.
"""
from src.services.task_manager import TaskManager
from src.cli.menu import MenuSystem


def main():
    """
    Main entry point for the application.
    Initializes the TaskManager and MenuSystem and starts the application loop.
    """
    # Initialize the task manager and menu system
    task_manager = TaskManager()
    menu_system = MenuSystem(task_manager)

    # Run the application
    menu_system.run()


if __name__ == "__main__":
    main()