# Frontend Data Models: Multi-User Todo Application

## Task Entity

### Task Interface
```typescript
interface Task {
  id: number;
  user_id: number;
  title: string;           // Max 255 characters
  description: string | null; // Max 1000 characters, optional
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  tags: string | null;     // Comma-separated tags, max 500 characters
  due_date: string | null; // ISO 8601 format (e.g., "2023-12-31T10:00:00Z")
  created_at: string;      // ISO 8601 format
  updated_at: string;      // ISO 8601 format
}
```

### Task Creation Interface
```typescript
interface TaskCreate {
  title: string;
  description?: string;
  priority?: 'high' | 'medium' | 'low';
  tags?: string;
  due_date?: string;       // ISO 8601 format
}
```

### Task Update Interface
```typescript
interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  tags?: string;
  due_date?: string;       // ISO 8601 format
}
```

### Task Toggle Completion Interface
```typescript
interface TaskToggleComplete {
  completed: boolean;
}
```

## User Session Entity

### Session Interface
```typescript
interface UserSession {
  authenticated: boolean;
  user_id: number | null;
  email: string | null;
  jwt_token: string | null;
  expires_at: string | null; // ISO 8601 format
}
```

## API Response Models

### Task List Response
```typescript
type TaskListResponse = Task[];
```

### Task Single Response
```typescript
type TaskResponse = Task;
```

### Task Creation Response
```typescript
type TaskCreationResponse = Task;
```

### Task Update Response
```typescript
type TaskUpdateResponse = Task;
```

### Task Deletion Response
```typescript
interface TaskDeletionResponse {
  message: string;
}
```

## Filter and Query Parameters

### Get Tasks Query Parameters
```typescript
interface GetTasksQuery {
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  tag?: string;
  search?: string;
  sort_by?: 'due_date' | 'priority' | 'title';
  order?: 'asc' | 'desc';
}
```

## UI State Models

### Task List State
```typescript
interface TaskListState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  filters: {
    completed: boolean | null;
    priority: 'high' | 'medium' | 'low' | null;
    tag: string | null;
    search: string;
  };
  sort: {
    by: 'due_date' | 'priority' | 'title';
    order: 'asc' | 'desc';
  };
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}
```

### Task Form State
```typescript
interface TaskFormState {
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  tags: string;
  due_date: string;
  completed: boolean;
  errors: {
    title?: string;
    description?: string;
    due_date?: string;
  };
  submitting: boolean;
}
```

## Validation Rules

### Task Creation Validation
- Title: Required, max 255 characters
- Description: Optional, max 1000 characters
- Priority: Required if provided, must be 'high', 'medium', or 'low'
- Tags: Optional, max 500 characters (comma-separated)
- Due date: Optional, must be valid ISO 8601 date format

### Task Update Validation
- Title: Optional, max 255 characters if provided
- Description: Optional, max 1000 characters if provided
- Priority: Optional, must be 'high', 'medium', or 'low' if provided
- Tags: Optional, max 500 characters if provided
- Due date: Optional, must be valid ISO 8601 date format if provided

### Search and Filter Validation
- Search term: Max 255 characters
- Tag filter: Max 100 characters
- Priority filter: Must be 'high', 'medium', or 'low' if provided
- Sort by: Must be 'due_date', 'priority', or 'title'
- Sort order: Must be 'asc' or 'desc'