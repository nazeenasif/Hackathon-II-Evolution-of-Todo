'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import Header from '@/components/Header';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import ChatModal from '@/components/ChatModal';
import { taskService } from '@/services/taskService';

export default function DashboardPage() {
  const router = useRouter();
  const [userId, setUserId] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showChat, setShowChat] = useState(false);

  useEffect(() => {
    // Get user ID from JWT token
    const token = localStorage.getItem('jwt_token');
    if (token) {
      try {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        setUserId(tokenPayload.sub);
      } catch (e) {
        console.error('Error decoding token:', e);
        router.push('/signin');
      }
    } else {
      router.push('/signin');
    }
  }, [router]);

  // Fetch tasks when userId changes
  useEffect(() => {
    const fetchTasks = async () => {
      if (userId) {
        setIsLoading(true);
        try {
          const data = await taskService.getTasks(userId);
          setTasks(data);
        } catch (err) {
          console.error('Error fetching tasks:', err);
        } finally {
          setIsLoading(false);
        }
      }
    };

    fetchTasks();
  }, [userId]);

  const handleSubmitTask = async (taskData) => {
    if (editingTask) {
      // Optimistic update for task editing
      const previousTasks = [...tasks];
      setTasks(tasks.map(task =>
        task.id === editingTask.id ? { ...task, ...taskData } : task
      ));

      try {
        const updatedTask = await taskService.updateTask(userId, editingTask.id, taskData);
        // Replace with server response to ensure consistency
        setTasks(prev => prev.map(task =>
          task.id === editingTask.id ? updatedTask : task
        ));
        setShowForm(false);
        setEditingTask(null);
      } catch (err) {
        // Revert on error
        setTasks(previousTasks);
        console.error('Error updating task:', err);
        alert('Failed to update task');
      }
    } else {
      // Optimistic update for task creation
      const newTask = {
        id: Date.now(), // Temporary ID
        user_id: userId,
        ...taskData,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      setTasks(prev => [newTask, ...prev]);

      try {
        const createdTask = await taskService.createTask(userId, taskData);
        // Replace temporary task with server task
        setTasks(prev => prev.map(task =>
          task.id === newTask.id ? createdTask : task
        ));
        setShowForm(false);
      } catch (err) {
        // Remove optimistic task on error
        setTasks(prev => prev.filter(task => task.id !== newTask.id));
        console.error('Error creating task:', err);
        alert('Failed to create task');
      }
    }
  };

  const handleCreateTask = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/5 rounded-full blur-2xl"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/5 rounded-full blur-2xl"></div>
        </div>

        <Header />
        <main className="py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
              <div>
                <h1 className="text-3xl font-bold text-foreground">My Tasks 📝</h1>
                <div className="flex items-center mt-2 space-x-4">
                  <span className="text-muted-foreground text-sm">
                    {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} • {tasks.filter(t => t.completed).length} completed
                  </span>
                  <span className="text-gray-400 text-sm">refresh to get updated tasks!</span>
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setShowChat(true)}
                  className="bg-purple-700 hover:bg-purple-600 text-white px-4 py-2 rounded-md font-medium transition-colors duration-200"
                >
                  <div className="flex items-center space-x-2">
                    <span>AI Assistant</span>
                  </div>
                </button>
                <button
                  onClick={handleCreateTask}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground px-4 py-2 rounded-md font-medium transition-colors duration-200"
                >
                  <div className="flex items-center space-x-2">
                    <span>+</span>
                    <span>Add Task</span>
                  </div>
                </button>
              </div>
            </div>

            {showForm ? (
              <div className="animate-in fade-in slide-in-from-top-4 duration-300">
                <TaskForm
                  task={editingTask}
                  onSubmit={handleSubmitTask}
                  onCancel={handleCancelForm}
                />
              </div>
            ) : null}

            {isLoading ? (
              <div className="flex flex-col items-center justify-center py-12 space-y-4">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                <p className="text-muted-foreground">Loading your tasks...</p>
              </div>
            ) : tasks.length === 0 ? (
              <div className="text-center py-12">
                <div className="mx-auto h-24 w-24 flex items-center justify-center rounded-full bg-accent mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">No tasks yet</h3>
                <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                  You haven't created any tasks yet. Get started by creating your first task and start organizing your day!
                </p>
                <button
                  onClick={handleCreateTask}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground px-6 py-3 rounded-md font-medium transition-colors duration-200"
                >
                  Create your first task
                </button>
                <p className="text-sm text-muted-foreground mt-4">
                  Or try our AI assistant to help you get started!
                </p>
              </div>
            ) : (
              <div className="relative">
                {/* Stats bar */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-card rounded-lg p-4 border border-border">
                    <div className="text-2xl font-bold text-foreground">{tasks.length}</div>
                    <div className="text-sm text-muted-foreground">Total Tasks</div>
                  </div>
                  <div className="bg-card rounded-lg p-4 border border-border">
                    <div className="text-2xl font-bold text-foreground">{tasks.filter(t => t.completed).length}</div>
                    <div className="text-sm text-muted-foreground">Completed</div>
                  </div>
                  <div className="bg-card rounded-lg p-4 border border-border">
                    <div className="text-2xl font-bold text-foreground">{tasks.filter(t => !t.completed).length}</div>
                    <div className="text-sm text-muted-foreground">Pending</div>
                  </div>
                </div>

                <div className="bg-card rounded-xl border shadow-sm overflow-hidden">
                  <TaskList
                    userId={userId}
                    tasks={tasks}
                    onUpdateTask={async (taskId, updates) => {
                      // Optimistic update
                      const previousTasks = [...tasks];
                      setTasks(tasks.map(task =>
                        task.id === taskId ? { ...task, ...updates } : task
                      ));

                      try {
                        await taskService.updateTask(userId, taskId, updates);
                        // Success: task stays updated (already reflected in UI)
                      } catch (err) {
                        // Revert on error
                        setTasks(previousTasks);
                        console.error('Error updating task:', err);
                        alert('Failed to update task');
                      }
                    }}
                    onDeleteTask={async (taskId) => {
                      // Optimistic update: remove task immediately
                      const taskToDelete = tasks.find(task => task.id === taskId);
                      if (!taskToDelete) return;

                      const previousTasks = [...tasks];
                      setTasks(tasks.filter(task => task.id !== taskId));

                      try {
                        await taskService.deleteTask(userId, taskId);
                        // Success: task stays removed
                      } catch (err) {
                        // Revert on error
                        setTasks(previousTasks);
                        console.error('Error deleting task:', err);
                        alert('Failed to delete task');
                      }
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        </main>

        {/* Chat Modal */}
        <ChatModal
          isOpen={showChat}
          onClose={() => setShowChat(false)}
        />
      </div>
    </ProtectedRoute>
  );
}