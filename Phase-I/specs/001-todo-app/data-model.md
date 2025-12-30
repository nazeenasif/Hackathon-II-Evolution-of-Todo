# Data Model: In-Memory Python Console Todo Application

## Task Entity

**Fields:**
- `id` (int): Unique identifier for the task, auto-incremented from 1
- `title` (str): Required title of the task, minimum 1 character
- `description` (str): Optional description of the task, can be empty string
- `status` (str): Task completion status, either "Incomplete" or "Complete"

**Validation Rules:**
- `id` must be unique within the application session
- `title` must be a non-empty string (1+ characters)
- `status` must be one of the allowed values: "Complete", "Incomplete"
- `description` can be any string including empty string

**State Transitions:**
- Default state: "Incomplete" when task is created
- Transition: "Incomplete" ↔ "Complete" when user toggles completion status

## Task List Structure

**In-Memory Storage:**
- Python dictionary with `id` as key and Task object as value
- Provides O(1) lookup performance for task operations
- Maintains data only during application runtime (in-memory only)

**Operations Supported:**
- Create: Add new task with auto-generated unique ID
- Read: Retrieve task by ID or list all tasks
- Update: Modify title/description of existing task
- Delete: Remove task by ID
- Toggle: Change status between "Complete"/"Incomplete"