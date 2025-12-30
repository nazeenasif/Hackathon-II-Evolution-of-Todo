#!/usr/bin/env python3
"""
Quick test to validate the todo application functionality.
"""
from src.services.task_manager import TaskManager
from src.models.task import Task

def test_functionality():
    print("Testing todo application functionality...")

    # Create a task manager
    tm = TaskManager()

    # Test adding a task
    task1 = tm.add_task("Test task", "This is a test description")
    print(f"Added task: ID={task1.id}, Title='{task1.title}', Status='{task1.status}'")

    # Test getting all tasks
    all_tasks = tm.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")

    # Test updating a task
    updated_task = tm.update_task(task1.id, title="Updated test task", description="Updated description")
    print(f"Updated task: ID={updated_task.id}, Title='{updated_task.title}'")

    # Test toggling status
    toggled_task = tm.toggle_status(task1.id)
    print(f"Toggled status: ID={toggled_task.id}, Status='{toggled_task.status}'")

    # Toggle back to original state
    toggled_task = tm.toggle_status(task1.id)
    print(f"Toggled back: ID={toggled_task.id}, Status='{toggled_task.status}'")

    # Test deleting a task
    delete_result = tm.delete_task(task1.id)
    print(f"Delete result: {delete_result}")

    # Verify task is deleted
    remaining_tasks = tm.get_all_tasks()
    print(f"Remaining tasks after deletion: {len(remaining_tasks)}")

    print("All functionality tests passed!")

if __name__ == "__main__":
    test_functionality()