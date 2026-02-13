// Task service functions to be used in client components
// These functions will access localStorage directly but only in client-side context

export const taskService = {
  // Get all tasks for a user
  getTasks: async (userId, queryParams = {}) => {
    if (typeof window === 'undefined') {
      throw new Error('Cannot access localStorage on the server');
    }

    console.log('Fetching tasks for user:', userId, 'with params:', queryParams);

    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks${new URLSearchParams(queryParams)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      // Safely convert error objects to readable strings
      let errorMessage = `Failed to fetch tasks: ${response.status} ${response.statusText}`;

      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Join array of error objects into a single message
          errorMessage += ' - ' + errorData.detail.map(err =>
            typeof err === 'string' ? err : (err.msg || JSON.stringify(err))
          ).join('; ');
        } else if (typeof errorData.detail === 'string') {
          errorMessage += ' - ' + errorData.detail;
        } else {
          errorMessage += ' - ' + JSON.stringify(errorData.detail);
        }
      } else if (errorData.message) {
        errorMessage += ' - ' + errorData.message;
      }

      console.error('Task fetch error:', errorMessage);
      throw new Error(errorMessage);
    }

    const result = await response.json();
    console.log('Fetched tasks successfully:', result.length);
    return result;
  },

  // Create a new task
  createTask: async (userId, taskData) => {
    if (typeof window === 'undefined') {
      throw new Error('Cannot access localStorage on the server');
    }

    console.log('Creating task for user:', userId, 'with data:', taskData);

    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      // Safely convert error objects to readable strings
      let errorMessage = `Failed to create task: ${response.status} ${response.statusText}`;

      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Join array of error objects into a single message
          errorMessage += ' - ' + errorData.detail.map(err =>
            typeof err === 'string' ? err : (err.msg || JSON.stringify(err))
          ).join('; ');
        } else if (typeof errorData.detail === 'string') {
          errorMessage += ' - ' + errorData.detail;
        } else {
          errorMessage += ' - ' + JSON.stringify(errorData.detail);
        }
      } else if (errorData.message) {
        errorMessage += ' - ' + errorData.message;
      }

      console.error('Task creation error:', errorMessage);
      throw new Error(errorMessage);
    }

    const result = await response.json();
    console.log('Task created successfully:', result);
    return result;
  },

  // Get a specific task
  getTask: async (userId, taskId) => {
    if (typeof window === 'undefined') {
      throw new Error('Cannot access localStorage on the server');
    }

    console.log('Fetching task:', taskId, 'for user:', userId);

    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      // Safely convert error objects to readable strings
      let errorMessage = `Failed to fetch task: ${response.status} ${response.statusText}`;

      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Join array of error objects into a single message
          errorMessage += ' - ' + errorData.detail.map(err =>
            typeof err === 'string' ? err : (err.msg || JSON.stringify(err))
          ).join('; ');
        } else if (typeof errorData.detail === 'string') {
          errorMessage += ' - ' + errorData.detail;
        } else {
          errorMessage += ' - ' + JSON.stringify(errorData.detail);
        }
      } else if (errorData.message) {
        errorMessage += ' - ' + errorData.message;
      }

      console.error('Task fetch error:', errorMessage);
      throw new Error(errorMessage);
    }

    const result = await response.json();
    console.log('Task fetched successfully:', result);
    return result;
  },

  // Update a task
  updateTask: async (userId, taskId, taskData) => {
    if (typeof window === 'undefined') {
      throw new Error('Cannot access localStorage on the server');
    }

    console.log('Updating task:', taskId, 'for user:', userId, 'with data:', taskData);

    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      // Safely convert error objects to readable strings
      let errorMessage = `Failed to update task: ${response.status} ${response.statusText}`;

      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Join array of error objects into a single message
          errorMessage += ' - ' + errorData.detail.map(err =>
            typeof err === 'string' ? err : (err.msg || JSON.stringify(err))
          ).join('; ');
        } else if (typeof errorData.detail === 'string') {
          errorMessage += ' - ' + errorData.detail;
        } else {
          errorMessage += ' - ' + JSON.stringify(errorData.detail);
        }
      } else if (errorData.message) {
        errorMessage += ' - ' + errorData.message;
      }

      console.error('Task update error:', errorMessage);
      throw new Error(errorMessage);
    }

    const result = await response.json();
    console.log('Task updated successfully:', result);
    return result;
  },

  // Delete a task
  deleteTask: async (userId, taskId) => {
    if (typeof window === 'undefined') {
      throw new Error('Cannot access localStorage on the server');
    }

    console.log('Deleting task:', taskId, 'for user:', userId);

    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      // Safely convert error objects to readable strings
      let errorMessage = `Failed to delete task: ${response.status} ${response.statusText}`;

      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Join array of error objects into a single message
          errorMessage += ' - ' + errorData.detail.map(err =>
            typeof err === 'string' ? err : (err.msg || JSON.stringify(err))
          ).join('; ');
        } else if (typeof errorData.detail === 'string') {
          errorMessage += ' - ' + errorData.detail;
        } else {
          errorMessage += ' - ' + JSON.stringify(errorData.detail);
        }
      } else if (errorData.message) {
        errorMessage += ' - ' + errorData.message;
      }

      console.error('Task deletion error:', errorMessage);
      throw new Error(errorMessage);
    }

    const result = await response.json();
    console.log('Task deleted successfully:', result);
    return result;
  },

  // Toggle task completion
  toggleTaskCompletion: async (userId, taskId, completed) => {
    if (typeof window === 'undefined') {
      throw new Error('Cannot access localStorage on the server');
    }

    console.log('Toggling completion for task:', taskId, 'for user:', userId, 'to:', completed);

    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/tasks/${taskId}/complete`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ completed }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      // Safely convert error objects to readable strings
      let errorMessage = `Failed to toggle task completion: ${response.status} ${response.statusText}`;

      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Join array of error objects into a single message
          errorMessage += ' - ' + errorData.detail.map(err =>
            typeof err === 'string' ? err : (err.msg || JSON.stringify(err))
          ).join('; ');
        } else if (typeof errorData.detail === 'string') {
          errorMessage += ' - ' + errorData.detail;
        } else {
          errorMessage += ' - ' + JSON.stringify(errorData.detail);
        }
      } else if (errorData.message) {
        errorMessage += ' - ' + errorData.message;
      }

      console.error('Task completion toggle error:', errorMessage);
      throw new Error(errorMessage);
    }

    const result = await response.json();
    console.log('Task completion toggled successfully:', result);
    return result;
  }
};