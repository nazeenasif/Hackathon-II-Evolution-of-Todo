# API Contracts: Multi-User Todo Application Frontend Integration

## Authentication API (via Better Auth)

### Sign Up
- **Endpoint**: `POST /api/auth/signup`
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string",
    "name": "string"
  }
  ```
- **Response**:
  ```json
  {
    "user": {
      "id": "number",
      "email": "string",
      "name": "string"
    },
    "token": "string"
  }
  ```
- **Headers**: Content-Type: application/json
- **Authentication**: None required

### Sign In
- **Endpoint**: `POST /api/auth/signin`
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "user": {
      "id": "number",
      "email": "string",
      "name": "string"
    },
    "token": "string"
  }
  ```
- **Headers**: Content-Type: application/json
- **Authentication**: None required

### Sign Out
- **Endpoint**: `POST /api/auth/signout`
- **Request Body**: None
- **Response**: `{ "success": true }`
- **Headers**: Authorization: Bearer {token}
- **Authentication**: Required

## Task Management API (via FastAPI Backend)

### Get User's Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Path Parameters**: `user_id: number`
- **Query Parameters**:
  - `completed`: boolean (optional) - Filter by completion status
  - `priority`: string (optional) - Filter by priority level (high, medium, low)
  - `tag`: string (optional) - Filter by tag/category
  - `search`: string (optional) - Search term for title or description
  - `sort_by`: string (optional, default: "due_date") - Field to sort by (due_date, priority, title)
  - `order`: string (optional, default: "asc") - Sort order (asc, desc)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "user_id": 123,
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "priority": "medium",
      "tags": "work,important",
      "due_date": "2023-12-31T10:00:00Z",
      "created_at": "2023-01-01T10:00:00Z",
      "updated_at": "2023-01-01T10:00:00Z"
    }
  ]
  ```
- **Headers**: Authorization: Bearer {token}
- **Authentication**: Required

### Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Path Parameters**: `user_id: number`
- **Request Body**:
  ```json
  {
    "title": "string (max 255)",
    "description": "string (max 1000, optional)",
    "priority": "string (high|medium|low, optional, default: medium)",
    "tags": "string (max 500, comma-separated, optional)",
    "due_date": "string (ISO 8601 format, optional)"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 123,
    "title": "New task",
    "description": "Task description",
    "completed": false,
    "priority": "high",
    "tags": "work,urgent",
    "due_date": "2023-12-31T10:00:00Z",
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
  ```
- **Headers**: Authorization: Bearer {token}
- **Authentication**: Required

### Get Specific Task
- **Endpoint**: `GET /api/{user_id}/tasks/{task_id}`
- **Path Parameters**:
  - `user_id: number`
  - `task_id: number`
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 123,
    "title": "Specific task",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "tags": "personal",
    "due_date": "2023-12-31T10:00:00Z",
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
  ```
- **Headers**: Authorization: Bearer {token}
- **Authentication**: Required

### Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`
- **Path Parameters**:
  - `user_id: number`
  - `task_id: number`
- **Request Body** (partial update):
  ```json
  {
    "title": "string (max 255, optional)",
    "description": "string (max 1000, optional)",
    "completed": "boolean (optional)",
    "priority": "string (high|medium|low, optional)",
    "tags": "string (max 500, comma-separated, optional)",
    "due_date": "string (ISO 8601 format, optional)"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 123,
    "title": "Updated task",
    "description": "Updated description",
    "completed": true,
    "priority": "high",
    "tags": "work,important,urgent",
    "due_date": "2023-12-31T10:00:00Z",
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-02T10:00:00Z"
  }
  ```
- **Headers**: Authorization: Bearer {token}
- **Authentication**: Required

### Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`
- **Path Parameters**:
  - `user_id: number`
  - `task_id: number`
- **Response**:
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```
- **Headers**: Authorization: Bearer {token}
- **Authentication**: Required

### Toggle Task Completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`
- **Path Parameters**:
  - `user_id: number`
  - `task_id: number`
- **Request Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 123,
    "title": "Completed task",
    "description": "Task description",
    "completed": true,
    "priority": "medium",
    "tags": "personal",
    "due_date": "2023-12-31T10:00:00Z",
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-02T10:00:00Z"
  }
  ```
- **Headers**: Authorization: Bearer {token}
- **Authentication**: Required

## Error Responses

### Authentication Error (401)
```json
{
  "detail": "Could not validate credentials"
}
```

### Authorization Error (403)
```json
  {
    "detail": "Access denied: You can only access your own resources"
  }
```

### Not Found Error (404)
```json
{
  "detail": "Task not found or doesn't belong to user"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

### General Error (500)
```json
{
  "detail": "Internal server error"
}
```

## Headers

### Required Headers for All Authenticated Requests
- `Authorization: Bearer {jwt_token}`

### Standard Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Authentication Flow

1. User signs up/signs in via Better Auth endpoints
2. JWT token is received and stored securely
3. JWT token is automatically attached to all subsequent API requests to the backend
4. Backend validates the token against BETTER_AUTH_SECRET
5. User ID is extracted from token and compared with requested user_id
6. Request proceeds if user_id matches, otherwise returns 403 Forbidden