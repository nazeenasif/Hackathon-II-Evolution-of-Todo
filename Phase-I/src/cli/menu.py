"""
Menu system framework for the In-Memory Python Console Todo Application.

This module implements the console interface and menu system as specified
in the user interaction flow requirements.
"""
from typing import Optional
from src.services.task_manager import TaskManager
from src.models.task import Task
from src.utils.validation import validate_task_title, validate_task_id, sanitize_input


class MenuSystem:
    """
    Implements the console interface and menu system for the todo application.
    """

    def __init__(self, task_manager: TaskManager):
        """
        Initialize the MenuSystem with a TaskManager instance.

        Args:
            task_manager (TaskManager): The task manager to interact with
        """
        self.task_manager = task_manager

    def display_menu(self) -> None:
        """
        Display the main menu with numbered options.
        """
        print("\nWelcome to the Todo Application!")
        print("1. Add task")
        print("2. View tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Mark task complete/incomplete")
        print("6. Exit")

    def get_user_choice(self) -> int:
        """
        Get and validate the user's menu choice.

        Returns:
            int: The user's menu choice (1-6), or 0 if invalid input
        """
        try:
            choice = input("Choose an option: ").strip()
            if not choice.isdigit():
                return 0  # Invalid choice
            choice_int = int(choice)
            if 1 <= choice_int <= 6:
                return choice_int
            return 0  # Out of range
        except (ValueError, EOFError):
            return 0  # Invalid input

    def handle_add_task(self) -> None:
        """
        Handle the add task functionality.
        """
        try:
            title = input("Enter task title: ").strip()
            if not validate_task_title(title):
                print("Error: Task title must be a non-empty string.")
                return

            description = input("Enter task description (optional): ").strip()

            task = self.task_manager.add_task(title, description)
            print(f"Task added successfully with ID {task.id}!")
        except Exception as e:
            print(f"Error adding task: {str(e)}")

    def handle_view_tasks(self) -> None:
        """
        Handle the view tasks functionality.
        """
        try:
            tasks = self.task_manager.get_all_tasks()
            if not tasks:
                print("No tasks found.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                print(f"ID: {task.id}, Title: {task.title}, "
                      f"Description: {task.description}, Status: {task.status}")
        except Exception as e:
            print(f"Error viewing tasks: {str(e)}")

    def handle_update_task(self) -> None:
        """
        Handle the update task functionality.
        """
        try:
            task_id_input = input("Enter task ID to update: ").strip()
            if not validate_task_id(task_id_input):
                print("Error: Please enter a valid task ID (positive integer).")
                return

            task_id = int(task_id_input)
            task = self.task_manager.get_task(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            new_title = input(f"Enter new title (current: '{task.title}'): ").strip()
            new_description = input(f"Enter new description (current: '{task.description}'): ").strip()

            # If the user doesn't want to update a field, keep the existing value
            if not new_title:
                new_title = task.title
            if not new_description:
                new_description = task.description

            updated_task = self.task_manager.update_task(task_id, new_title, new_description)
            if updated_task:
                print(f"Task {task_id} updated successfully!")
            else:
                print(f"Error: Failed to update task {task_id}.")
        except Exception as e:
            print(f"Error updating task: {str(e)}")

    def handle_delete_task(self) -> None:
        """
        Handle the delete task functionality.
        """
        try:
            task_id_input = input("Enter task ID to delete: ").strip()
            if not validate_task_id(task_id_input):
                print("Error: Please enter a valid task ID (positive integer).")
                return

            task_id = int(task_id_input)
            success = self.task_manager.delete_task(task_id)
            if success:
                print(f"Task {task_id} deleted successfully!")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except Exception as e:
            print(f"Error deleting task: {str(e)}")

    def handle_toggle_status(self) -> None:
        """
        Handle the toggle task status functionality.
        """
        try:
            task_id_input = input("Enter task ID to toggle status: ").strip()
            if not validate_task_id(task_id_input):
                print("Error: Please enter a valid task ID (positive integer).")
                return

            task_id = int(task_id_input)
            task = self.task_manager.get_task(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            updated_task = self.task_manager.toggle_status(task_id)
            if updated_task:
                print(f"Task {task_id} status changed to: {updated_task.status}")
            else:
                print(f"Error: Failed to toggle status for task {task_id}.")
        except Exception as e:
            print(f"Error toggling task status: {str(e)}")

    def handle_exit(self) -> bool:
        """
        Handle the exit functionality.

        Returns:
            bool: True to indicate the application should exit
        """
        print("Goodbye!")
        return True

    def run(self) -> None:
        """
        Run the main application loop.
        """
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == 1:
                self.handle_add_task()
            elif choice == 2:
                self.handle_view_tasks()
            elif choice == 3:
                self.handle_update_task()
            elif choice == 4:
                self.handle_delete_task()
            elif choice == 5:
                self.handle_toggle_status()
            elif choice == 6:
                if self.handle_exit():
                    break
            else:
                print("Invalid option. Please choose a number between 1 and 6.")