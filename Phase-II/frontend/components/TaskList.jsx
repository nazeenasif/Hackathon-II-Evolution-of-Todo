import { useState, useEffect } from 'react';
import TaskCard from '@/components/TaskCard';
import SearchFilterBar from '@/components/SearchFilterBar';

export default function TaskList({ userId, tasks, onUpdateTask, onDeleteTask }) {
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [filters, setFilters] = useState({
    sort_by: 'due_date',
    order: 'asc'
  });

  useEffect(() => {
    applyFiltersAndSorting();
  }, [tasks, filters]);

  const applyFiltersAndSorting = () => {
    let result = [...tasks];

    // Apply search filter
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchTerm) ||
        (task.description && task.description.toLowerCase().includes(searchTerm))
      );
    }

    // Apply priority filter
    if (filters.priority) {
      result = result.filter(task => task.priority === filters.priority);
    }

    // Apply completion filter
    if (filters.completed !== undefined && filters.completed !== null) {
      result = result.filter(task => task.completed === filters.completed);
    }

    // Apply tag filter
    if (filters.tag) {
      const tagFilter = filters.tag.toLowerCase();
      result = result.filter(task =>
        task.tags && task.tags.toLowerCase().split(',').some(tag => tag.trim() === tagFilter)
      );
    }

    // Apply sorting
    result.sort((a, b) => {
      let aValue, bValue;

      switch (filters.sort_by) {
        case 'title':
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
          break;
        case 'priority':
          // Define priority order: high > medium > low
          const priorityOrder = { 'high': 3, 'medium': 2, 'low': 1 };
          aValue = priorityOrder[a.priority];
          bValue = priorityOrder[b.priority];
          break;
        case 'due_date':
        default:
          // Handle null due dates by treating them as future dates
          aValue = a.due_date ? new Date(a.due_date) : new Date('9999-12-31');
          bValue = b.due_date ? new Date(b.due_date) : new Date('9999-12-31');
          break;
      }

      if (aValue < bValue) return filters.order === 'asc' ? -1 : 1;
      if (aValue > bValue) return filters.order === 'asc' ? 1 : -1;
      return 0;
    });

    setFilteredTasks(result);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleDelete = (taskId) => {
    onDeleteTask(taskId);
  };

  const handleToggleComplete = (taskId, completed) => {
    onUpdateTask(taskId, { completed });
  };

  const handleEdit = (task) => {
    // This would typically open a modal or navigate to an edit page
    console.log('Edit task:', task);
  };

  return (
    <div className="p-5 bg-card rounded-xl border shadow-sm">
      <SearchFilterBar onFilterChange={handleFilterChange} />
      <div className="space-y-4 mt-4">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            No tasks found. Create your first task!
          </div>
        ) : (
          filteredTasks.map(task => (
            <TaskCard
              key={task.id}
              task={task}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onToggleComplete={handleToggleComplete}
            />
          ))
        )}
      </div>
    </div>
  );
}