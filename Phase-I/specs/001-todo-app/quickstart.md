# Quickstart Guide: In-Memory Python Console Todo Application

## Prerequisites
- Python 3.13+ installed
- UV package manager installed (if using dependencies beyond standard library)

## Setup
1. Clone or create the project directory
2. Ensure Python 3.13+ is available in your environment
3. No additional dependencies needed beyond Python standard library

## Running the Application
1. Navigate to the project root directory
2. Run the application: `python src/main.py`
3. The main menu will display with numbered options

## Basic Usage
1. **Add Task**: Select option 1, enter task title and optional description
2. **View Tasks**: Select option 2, see all tasks with ID, title, description, and status
3. **Update Task**: Select option 3, enter task ID and new title/description
4. **Delete Task**: Select option 4, enter task ID to remove permanently
5. **Mark Complete/Incomplete**: Select option 5, enter task ID to toggle status
6. **Exit**: Select option 6 to terminate the application

## Example Workflow
```
Welcome to the Todo Application!
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
Choose an option: 1
Enter task title: Buy groceries
Enter task description (optional): Milk, bread, eggs
Task added successfully with ID 1!

Choose an option: 2
ID: 1, Title: Buy groceries, Description: Milk, bread, eggs, Status: Incomplete

Choose an option: 5
Enter task ID to toggle status: 1
Task 1 status changed to: Complete

Choose an option: 2
ID: 1, Title: Buy groceries, Description: Milk, bread, eggs, Status: Complete

Choose an option: 6
Goodbye!
```

## Error Handling
- Invalid menu selections will show an error message and return to the main menu
- Invalid task IDs will show appropriate error messages
- Empty titles will be rejected when adding tasks
- All errors are handled gracefully without application crashes