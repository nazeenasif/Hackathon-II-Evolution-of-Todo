import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models.task import Task, TaskCreate
from src.models.user import User, UserCreate


def test_task_crud_operations(client: TestClient, session: Session):
    """Test basic CRUD operations for tasks (FR-001, FR-003, FR-004, FR-005, FR-006)"""

    # Create a user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser"
    }
    user_response = client.post("/api/999/tasks", json={
        "title": "Temporary task to create user",
        "user_id": 999
    })
    # We expect a 422 error because user doesn't exist, but we just need the user created

    # Create user manually for test
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # 1. Create a task (FR-003)
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium"
    }
    response = client.post(f"/api/{user.id}/tasks", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    assert created_task["title"] == "Test Task"
    assert created_task["user_id"] == user.id

    # 2. Retrieve the task (FR-004)
    task_id = created_task["id"]
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Test Task"

    # 3. Update the task (FR-005)
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    response = client.put(f"/api/{user.id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] is True

    # 4. Delete the task (FR-006)
    response = client.delete(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 200

    # Verify deletion
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 404


def test_user_isolation(client: TestClient, session: Session):
    """Test that users can only access their own tasks (FR-002)"""

    # Create two users
    user1 = User(email="user1@example.com", username="user1")
    user2 = User(email="user2@example.com", username="user2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create task for user1
    task_data = {"title": "User1's Task", "priority": "high"}
    response = client.post(f"/api/{user1.id}/tasks", json=task_data)
    assert response.status_code == 200
    task1 = response.json()

    # Create task for user2
    task_data = {"title": "User2's Task", "priority": "low"}
    response = client.post(f"/api/{user2.id}/tasks", json=task_data)
    assert response.status_code == 200
    task2 = response.json()

    # Verify user1 can access their own task
    response = client.get(f"/api/{user1.id}/tasks/{task1['id']}")
    assert response.status_code == 200

    # Verify user1 cannot access user2's task
    response = client.get(f"/api/{user1.id}/tasks/{task2['id']}")
    assert response.status_code == 404

    # Verify user2 can access their own task
    response = client.get(f"/api/{user2.id}/tasks/{task2['id']}")
    assert response.status_code == 200


def test_advanced_features(client: TestClient, session: Session):
    """Test advanced task features: priorities, tags, search, filter (FR-008, FR-009, FR-010, FR-011)"""

    # Create a user
    user = User(email="advtest@example.com", username="advtestuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create multiple tasks with different properties
    tasks_data = [
        {"title": "High Priority Task", "priority": "high", "tags": "important,work"},
        {"title": "Low Priority Task", "priority": "low", "tags": "personal"},
        {"title": "Medium Priority Task", "priority": "medium", "tags": "work"},
        {"title": "Completed Task", "priority": "medium", "completed": True, "tags": "done"},
    ]

    created_tasks = []
    for task_data in tasks_data:
        response = client.post(f"/api/{user.id}/tasks", json=task_data)
        assert response.status_code == 200
        created_tasks.append(response.json())

    # Test filtering by priority (FR-011)
    response = client.get(f"/api/{user.id}/tasks", params={"priority": "high"})
    assert response.status_code == 200
    filtered_tasks = response.json()
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["priority"] == "high"

    # Test filtering by completion status (FR-011)
    response = client.get(f"/api/{user.id}/tasks", params={"completed": "true"})
    assert response.status_code == 200
    completed_tasks = response.json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["completed"] is True

    # Test search functionality (FR-010)
    response = client.get(f"/api/{user.id}/tasks", params={"search": "High"})
    assert response.status_code == 200
    search_results = response.json()
    assert len(search_results) >= 1
    assert any("High" in task["title"] for task in search_results)


def test_sorting_functionality(client: TestClient, session: Session):
    """Test sorting functionality (FR-012)"""

    # Create a user
    user = User(email="sorttest@example.com", username="sorttestuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create tasks with different due dates and priorities
    import datetime
    future_date = (datetime.datetime.now() + datetime.timedelta(days=5)).isoformat()
    past_date = (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat()

    tasks_data = [
        {"title": "Future Task", "priority": "low", "due_date": future_date},
        {"title": "Past Task", "priority": "high", "due_date": past_date},
        {"title": "Today Task", "priority": "medium", "due_date": datetime.datetime.now().isoformat()},
    ]

    for task_data in tasks_data:
        response = client.post(f"/api/{user.id}/tasks", json=task_data)
        assert response.status_code == 200

    # Test sorting by due date (FR-012)
    response = client.get(f"/api/{user.id}/tasks", params={"sort_by": "due_date", "order": "asc"})
    assert response.status_code == 200
    sorted_tasks = response.json()

    # Verify that tasks are sorted by due date (ascending)
    for i in range(len(sorted_tasks) - 1):
        if sorted_tasks[i]['due_date'] and sorted_tasks[i+1]['due_date']:
            assert sorted_tasks[i]['due_date'] <= sorted_tasks[i+1]['due_date']

    # Test sorting by priority (FR-012)
    response = client.get(f"/api/{user.id}/tasks", params={"sort_by": "priority", "order": "desc"})
    assert response.status_code == 200
    sorted_by_priority = response.json()

    # Verify descending priority order (high to low)
    priority_order = {"high": 3, "medium": 2, "low": 1}
    for i in range(len(sorted_by_priority) - 1):
        current_prio = priority_order[sorted_by_priority[i]['priority']]
        next_prio = priority_order[sorted_by_priority[i+1]['priority']]
        assert current_prio >= next_prio


def test_completion_toggle(client: TestClient, session: Session):
    """Test completion toggle functionality"""

    # Create a user
    user = User(email="toggletest@example.com", username="toggletestuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task
    task_data = {"title": "Toggle Task", "priority": "medium"}
    response = client.post(f"/api/{user.id}/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()

    # Toggle completion status
    response = client.patch(f"/api/{user.id}/tasks/{task['id']}/complete")
    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["completed"] is True

    # Toggle again to set to False
    response = client.patch(f"/api/{user.id}/tasks/{task['id']}/complete")
    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["completed"] is False