# API Contracts: In-Memory Python Console Todo Application

## Task Management Operations

### Add Task
- **Input**: title (string, required), description (string, optional)
- **Output**: task object with id, title, description, status
- **Success**: Returns created task with assigned ID and "Incomplete" status
- **Errors**: Invalid input (empty title), system errors

### View Tasks
- **Input**: None
- **Output**: Array of task objects
- **Success**: Returns all tasks in memory with all fields
- **Errors**: None (returns empty array if no tasks)

### Update Task
- **Input**: task_id (int), title (string, optional), description (string, optional)
- **Output**: updated task object
- **Success**: Returns task with updated fields
- **Errors**: Task not found, invalid task ID

### Delete Task
- **Input**: task_id (int)
- **Output**: success confirmation
- **Success**: Task removed from memory
- **Errors**: Task not found, invalid task ID

### Toggle Task Status
- **Input**: task_id (int)
- **Output**: updated task object
- **Success**: Returns task with toggled status
- **Errors**: Task not found, invalid task ID

## Data Contract

### Task Object
```
{
  "id": integer,
  "title": string,
  "description": string,
  "status": "Complete" | "Incomplete"
}
```