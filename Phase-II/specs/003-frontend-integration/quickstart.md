# Quickstart Guide: Frontend Development

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to backend API (running on http://localhost:8000 by default)

## Setup Instructions

### 1. Clone and Initialize Project
```bash
npx create-next-app@latest todo-frontend
cd todo-frontend
```

### 2. Install Dependencies
```bash
npm install better-auth axios @better-auth/react react-icons
# or
yarn add better-auth axios @better-auth/react react-icons
```

### 3. Configure Environment Variables
Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-here
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-here
```

### 4. Configure Better Auth
Create `lib/auth.js`:
```javascript
import { init } from "better-auth";

export const auth = init({
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
  // Add your authentication configuration here
});
```

### 5. Create API Client
Create `lib/api.js`:
```javascript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Add JWT token to all requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login if token is invalid/expired
      localStorage.removeItem('jwt_token');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### 6. Basic Task Service
Create `services/taskService.js`:
```javascript
import apiClient from '@/lib/api';

export const taskService = {
  // Get all tasks for a user
  getTasks: async (userId, queryParams = {}) => {
    const response = await apiClient.get(`/api/${userId}/tasks`, { params: queryParams });
    return response.data;
  },

  // Create a new task
  createTask: async (userId, taskData) => {
    const response = await apiClient.post(`/api/${userId}/tasks`, taskData);
    return response.data;
  },

  // Get a specific task
  getTask: async (userId, taskId) => {
    const response = await apiClient.get(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Update a task
  updateTask: async (userId, taskId, taskData) => {
    const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  // Delete a task
  deleteTask: async (userId, taskId) => {
    const response = await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Toggle task completion
  toggleTaskCompletion: async (userId, taskId, completed) => {
    const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`, {
      completed
    });
    return response.data;
  }
};
```

### 7. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000

## Key Components to Implement

### Protected Route Component
```jsx
// components/ProtectedRoute.jsx
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@better-auth/react';

export default function ProtectedRoute({ children }) {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/signin');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || !isAuthenticated) {
    return <div>Loading...</div>;
  }

  return children;
}
```

### Task List Component
```jsx
// components/TaskList.jsx
import { useState, useEffect } from 'react';
import TaskCard from './TaskCard';
import { taskService } from '@/services/taskService';

export default function TaskList({ userId }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    completed: null,
    priority: null,
    search: ''
  });

  useEffect(() => {
    fetchTasks();
  }, [userId, filters]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const queryParams = {
        completed: filters.completed,
        priority: filters.priority,
        search: filters.search
      };
      const data = await taskService.getTasks(userId, queryParams);
      setTasks(data);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading tasks...</div>;

  return (
    <div className="space-y-4">
      {tasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}
```