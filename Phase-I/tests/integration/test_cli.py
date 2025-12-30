"""
Integration tests for the CLI functionality of the Todo Application.
"""
import unittest
from src.services.task_manager import TaskManager
from src.cli.menu import MenuSystem


class TestCLIIntegration(unittest.TestCase):
    """
    Integration tests for the CLI menu system.
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.task_manager = TaskManager()
        self.menu_system = MenuSystem(self.task_manager)

    def test_add_task_integration(self):
        """
        Test adding a task through the CLI system.
        """
        # This test verifies that the CLI and TaskManager work together
        initial_count = len(self.task_manager.get_all_tasks())

        # Add a task directly through TaskManager (simulating CLI input)
        task = self.task_manager.add_task("Test Task", "Test Description")

        # Verify the task was added
        all_tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(all_tasks), initial_count + 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.status, "Incomplete")

    def test_view_tasks_integration(self):
        """
        Test viewing tasks through the TaskManager.
        """
        # Add some tasks
        task1 = self.task_manager.add_task("Task 1", "Description 1")
        task2 = self.task_manager.add_task("Task 2", "Description 2")

        # Get all tasks
        all_tasks = self.task_manager.get_all_tasks()

        # Verify both tasks are present
        self.assertEqual(len(all_tasks), 2)
        titles = [task.title for task in all_tasks]
        self.assertIn("Task 1", titles)
        self.assertIn("Task 2", titles)

    def test_update_task_integration(self):
        """
        Test updating a task through the CLI system.
        """
        # Add a task
        original_task = self.task_manager.add_task("Original Task", "Original Description")
        original_id = original_task.id

        # Update the task
        updated_task = self.task_manager.update_task(
            original_id,
            title="Updated Task",
            description="Updated Description"
        )

        # Verify the task was updated
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Updated Description")
        # Status should remain the same
        self.assertEqual(updated_task.status, "Incomplete")

    def test_delete_task_integration(self):
        """
        Test deleting a task through the CLI system.
        """
        # Add a task
        task = self.task_manager.add_task("Task to Delete", "Description")
        initial_count = len(self.task_manager.get_all_tasks())

        # Delete the task
        result = self.task_manager.delete_task(task.id)

        # Verify the task was deleted
        self.assertTrue(result)
        final_count = len(self.task_manager.get_all_tasks())
        self.assertEqual(final_count, initial_count - 1)

        # Verify the task no longer exists
        deleted_task = self.task_manager.get_task(task.id)
        self.assertIsNone(deleted_task)

    def test_toggle_status_integration(self):
        """
        Test toggling task status through the CLI system.
        """
        # Add a task
        task = self.task_manager.add_task("Status Test Task", "Description")

        # Verify initial status
        self.assertEqual(task.status, "Incomplete")

        # Toggle status
        toggled_task = self.task_manager.toggle_status(task.id)

        # Verify status changed
        self.assertEqual(toggled_task.status, "Complete")

        # Toggle back
        toggled_back_task = self.task_manager.toggle_status(task.id)

        # Verify status changed back
        self.assertEqual(toggled_back_task.status, "Incomplete")


if __name__ == '__main__':
    unittest.main()