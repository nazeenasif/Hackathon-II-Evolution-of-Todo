# Quickstart Guide: Backend Core & Database Layer for Multi-User Todo Application

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Neon Serverless PostgreSQL database
- Git (for version control)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file based on the `.env.example`:
```bash
cp .env.example .env
```

Update the `.env` file with your Neon PostgreSQL connection details:
```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

### 5. Database Initialization
Run the following command to initialize the database:
```bash
# Run migrations to create tables
alembic upgrade head
```

## Running the Application

### Development Mode
```bash
# Run the application with hot reload
uvicorn src.main:app --reload --port 8000
```

### Production Mode
```bash
# Run the application for production
uvicorn src.main:app --workers 4 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Task Management
- `GET /api/{user_id}/tasks` - List tasks with optional filtering
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

### Query Parameters (for GET /api/{user_id}/tasks)
- `completed`: Filter by completion status (true/false)
- `priority`: Filter by priority ('high', 'medium', 'low')
- `tag`: Filter by tag/category
- `search`: Search in title and description
- `sort_by`: Sort by 'due_date', 'priority', 'title' (default: 'due_date')
- `order`: Sort order 'asc' or 'desc' (default: 'asc')

## Testing

Run the test suite:
```bash
pytest tests/
```

Run specific test files:
```bash
pytest tests/unit/
pytest tests/integration/
```

## Configuration

The application uses environment variables for configuration:
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: 'development', 'staging', or 'production'
- `LOG_LEVEL`: Logging level ('debug', 'info', 'warning', 'error')