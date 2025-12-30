import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

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