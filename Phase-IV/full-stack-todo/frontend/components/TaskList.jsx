'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence, LayoutGroup } from 'framer-motion';
import TaskCard from '@/components/TaskCard';
import SearchFilterBar from '@/components/SearchFilterBar';
import { getReducedMotion } from '@/lib/animations';

export default function TaskList({ userId, tasks, onUpdateTask, onDeleteTask }) {
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [filters, setFilters] = useState({
    sort_by: 'due_date',
    order: 'asc'
  });

  // Check if reduced motion is enabled
  const isReducedMotion = getReducedMotion();

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
    <motion.div
      className="p-4 bg-card rounded-lg border shadow-sm"
      initial={false}
      animate={isReducedMotion ? { transition: { duration: 0.01 } } : {}}
    >
      <SearchFilterBar onFilterChange={handleFilterChange} />
      <LayoutGroup>
        <motion.div
          className="space-y-4 mt-4"
          layout
          initial="hidden"
          animate="visible"
          variants={{
            hidden: { opacity: 0 },
            visible: {
              opacity: 1,
              transition: {
                staggerChildren: isReducedMotion ? 0 : 0.05,
                delayChildren: isReducedMotion ? 0 : 0.1
              }
            }
          }}
        >
          {filteredTasks.length === 0 ? (
            <motion.div
              className="text-center py-12 text-muted-foreground"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
            >
              No tasks found. Create your first task!
            </motion.div>
          ) : (
            <AnimatePresence>
              {filteredTasks.map((task, index) => (
                <motion.div
                  key={task.id}
                  layout
                  initial={false}
                  variants={{
                    hidden: { opacity: 0, y: 20 },
                    visible: { opacity: 1, y: 0 }
                  }}
                  transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.2 }}
                >
                  <TaskCard
                    task={task}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                    onToggleComplete={handleToggleComplete}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          )}
        </motion.div>
      </LayoutGroup>
    </motion.div>
  );
}