from datetime import datetime
from sqlmodel import Session
from src.models.task import Task, TaskCreate, TaskUpdate, PriorityEnum
from src.services.task_service import TaskService


def test_create_task(session: Session):
    """Test creating a new task"""
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        user_id=1
    )

    created_task = TaskService.create_task(session, task_data)

    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    assert created_task.user_id == 1
    assert created_task.completed is False  # Default value
    assert created_task.priority == PriorityEnum.medium  # Default value
    assert created_task.created_at is not None
    assert created_task.updated_at is not None


def test_get_task_by_id(session: Session):
    """Test retrieving a task by ID"""
    # First create a task
    task_data = TaskCreate(title="Get Task Test", user_id=1)
    created_task = TaskService.create_task(session, task_data)

    # Retrieve the task
    retrieved_task = TaskService.get_task_by_id(session, created_task.id, 1)

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Get Task Test"


def test_update_task(session: Session):
    """Test updating a task"""
    # First create a task
    task_data = TaskCreate(title="Original Task", user_id=1)
    created_task = TaskService.create_task(session, task_data)

    # Update the task
    update_data = TaskUpdate(title="Updated Task", completed=True)
    updated_task = TaskService.update_task(session, created_task.id, 1, update_data)

    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.completed is True
    # Ensure updated_at was updated
    assert updated_task.updated_at > updated_task.created_at


def test_delete_task(session: Session):
    """Test deleting a task"""
    # First create a task
    task_data = TaskCreate(title="Delete Task Test", user_id=1)
    created_task = TaskService.create_task(session, task_data)

    # Verify task exists
    retrieved_task = TaskService.get_task_by_id(session, created_task.id, 1)
    assert retrieved_task is not None

    # Delete the task
    result = TaskService.delete_task(session, created_task.id, 1)
    assert result is True

    # Verify task no longer exists
    retrieved_task = TaskService.get_task_by_id(session, created_task.id, 1)
    assert retrieved_task is None


def test_get_tasks_filtering(session: Session):
    """Test filtering tasks"""
    user_id = 1

    # Create multiple tasks with different properties
    task1_data = TaskCreate(title="High Priority", priority=PriorityEnum.high, user_id=user_id)
    task2_data = TaskCreate(title="Medium Priority", priority=PriorityEnum.medium, user_id=user_id)
    task3_data = TaskCreate(title="Low Priority", priority=PriorityEnum.low, completed=True, user_id=user_id)

    TaskService.create_task(session, task1_data)
    TaskService.create_task(session, task2_data)
    TaskService.create_task(session, task3_data)

    # Test filtering by priority
    high_priority_tasks = TaskService.get_tasks(session, user_id, priority=PriorityEnum.high)
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0].priority == PriorityEnum.high

    # Test filtering by completion status
    completed_tasks = TaskService.get_tasks(session, user_id, completed=True)
    assert len(completed_tasks) == 1
    assert completed_tasks[0].completed is True


def test_get_tasks_search(session: Session):
    """Test searching tasks"""
    user_id = 1

    # Create tasks with different titles
    task1_data = TaskCreate(title="Important Meeting", user_id=user_id)
    task2_data = TaskCreate(title="Grocery Shopping", user_id=user_id)
    task3_data = TaskCreate(title="Doctor Appointment", user_id=user_id)

    TaskService.create_task(session, task1_data)
    TaskService.create_task(session, task2_data)
    TaskService.create_task(session, task3_data)

    # Test search functionality
    search_results = TaskService.get_tasks(session, user_id, search="Meeting")
    assert len(search_results) == 1
    assert "Meeting" in search_results[0].title


def test_toggle_task_completion(session: Session):
    """Test toggling task completion status"""
    # First create a task
    task_data = TaskCreate(title="Toggle Completion Test", user_id=1)
    created_task = TaskService.create_task(session, task_data)

    # Initially, task should not be completed
    assert created_task.completed is False

    # Toggle completion status
    toggled_task = TaskService.toggle_task_completion(session, created_task.id, 1)
    assert toggled_task is not None
    assert toggled_task.completed is True

    # Toggle again to set to False
    toggled_task = TaskService.toggle_task_completion(session, created_task.id, 1)
    assert toggled_task is not None
    assert toggled_task.completed is False


def test_get_tasks_sorting(session: Session):
    """Test sorting tasks"""
    user_id = 1

    # Create tasks with different priorities and due dates
    from datetime import datetime, timedelta

    task1_data = TaskCreate(
        title="Alpha Task",
        priority=PriorityEnum.low,
        due_date=datetime.now() + timedelta(days=3),
        user_id=user_id
    )
    task2_data = TaskCreate(
        title="Beta Task",
        priority=PriorityEnum.high,
        due_date=datetime.now() + timedelta(days=1),
        user_id=user_id
    )
    task3_data = TaskCreate(
        title="Gamma Task",
        priority=PriorityEnum.medium,
        due_date=datetime.now() + timedelta(days=2),
        user_id=user_id
    )

    TaskService.create_task(session, task1_data)
    TaskService.create_task(session, task2_data)
    TaskService.create_task(session, task3_data)

    # Test sorting by title (alphabetical)
    sorted_tasks = TaskService.get_tasks(session, user_id, sort_by="title", order="asc")
    titles = [task.title for task in sorted_tasks]
    assert titles == sorted(titles)

    # Test sorting by priority
    sorted_by_priority = TaskService.get_tasks(session, user_id, sort_by="priority", order="desc")
    priority_order = [task.priority for task in sorted_by_priority]
    expected_order = [PriorityEnum.high, PriorityEnum.medium, PriorityEnum.low]
    # Just check that high priority comes first
    assert priority_order[0] == PriorityEnum.high