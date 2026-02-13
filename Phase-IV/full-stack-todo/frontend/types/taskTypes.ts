export interface Task {
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

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: 'high' | 'medium' | 'low';
  tags?: string;
  due_date?: string;       // ISO 8601 format
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  tags?: string;
  due_date?: string;       // ISO 8601 format
}

export interface TaskToggleComplete {
  completed: boolean;
}

export interface UserSession {
  authenticated: boolean;
  user_id: number | null;
  email: string | null;
  jwt_token: string | null;
  expires_at: string | null; // ISO 8601 format
}

export type TaskListResponse = Task[];

export interface TaskDeletionResponse {
  message: string;
}

export interface GetTasksQuery {
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  tag?: string;
  search?: string;
  sort_by?: 'due_date' | 'priority' | 'title';
  order?: 'asc' | 'desc';
}

export interface TaskListState {
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

export interface TaskFormState {
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