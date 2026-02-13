# Todo Backend API

Backend Core & Database Layer for Multi-User Todo Application

## Overview

This is a FastAPI-based backend system for a multi-user todo application using SQLModel ORM with Neon Serverless PostgreSQL. The system provides RESTful API endpoints for task management with user isolation, supporting CRUD operations, priorities, tags/categories, search, filter, and sort capabilities.

## Features

- Multi-user task management with user isolation
- CRUD operations for tasks
- Priority levels (high, medium, low)
- Tags/categories for organization
- Search, filter, and sort capabilities
- RESTful API design
- Data persistence with PostgreSQL

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel
- SQLAlchemy
- Pydantic
- PostgreSQL (Neon Serverless)

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and update with your database credentials and `BETTER_AUTH_SECRET`
6. Run database migrations: `alembic upgrade head`
7. Start the server: `uvicorn src.main:app --reload`

### Authentication Setup

To use the authentication system:
1. Configure Better Auth on the frontend with the same `BETTER_AUTH_SECRET`
2. Ensure the `BETTER_AUTH_SECRET` in your backend `.env` file matches the secret used by Better Auth
3. The frontend will issue JWT tokens that the backend will validate using this shared secret

## API Endpoints

The API provides the following endpoints:

### Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

The JWT tokens are issued by Better Auth on the frontend and must be signed with the same secret configured in `BETTER_AUTH_SECRET`.

### Task Management

- `GET /api/{user_id}/tasks` - List tasks with optional filtering
  - Query parameters:
    - `completed`: Filter by completion status (true/false)
    - `priority`: Filter by priority ('high', 'medium', 'low')
    - `tag`: Filter by tag/category
    - `search`: Search term for title or description
    - `sort_by`: Field to sort by ('due_date', 'priority', 'title')
    - `order`: Sort order ('asc', 'desc')

- `POST /api/{user_id}/tasks` - Create a new task
  - Request body: `{"title": "Task title", "description": "Optional description", "priority": "medium", "tags": "comma,separated,tags", "due_date": "2023-12-31T10:00:00Z"}`

- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task

- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
  - Request body: Partial task data to update

- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task

- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion
  - Request body: `{"completed": true}`

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: 'development', 'staging', or 'production'
- `LOG_LEVEL`: Logging level ('debug', 'info', 'warning', 'error')
- `SECRET_KEY`: Secret key for JWT token generation
- `BETTER_AUTH_SECRET`: Shared secret for JWT token validation (must match the secret used by Better Auth on the frontend)

## Running Migrations

To apply database migrations:
```bash
alembic upgrade head
```

To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

## Development

To run the application in development mode:
```bash
uvicorn src.main:app --reload
```

Or using the poetry script:
```bash
poetry run dev
```

## Testing

Run unit tests:
```bash
pytest tests/unit/
```

Run integration tests:
```bash
pytest tests/integration/
```