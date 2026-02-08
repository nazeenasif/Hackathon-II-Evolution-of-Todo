'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRegCircle, FaCheckCircle, FaEdit, FaTrash } from 'react-icons/fa';
import Button from '@/components/ui/Button';
import { getReducedMotion } from '@/lib/animations';
import { useTheme } from '@/components/ThemeProvider';

export default function TaskCard({ task, onEdit, onDelete, onToggleComplete }) {
  const [showActions, setShowActions] = useState(false);
  const { theme } = useTheme();

  const handleToggleComplete = () => {
    onToggleComplete(task.id, !task.completed);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return theme === 'dark'
          ? 'bg-red-600/30 text-red-200 border border-red-700/50'
          : 'bg-red-100 text-red-800 border border-red-300';
      case 'medium':
        return theme === 'dark'
          ? 'bg-amber-600/30 text-amber-200 border border-amber-700/50'
          : 'bg-amber-100 text-amber-800 border border-amber-300';
      case 'low':
        return theme === 'dark'
          ? 'bg-emerald-600/30 text-emerald-200 border border-emerald-700/50'
          : 'bg-emerald-100 text-emerald-800 border border-emerald-300';
      default:
        return theme === 'dark'
          ? 'bg-gray-600/30 text-gray-200 border border-gray-700/50'
          : 'bg-gray-100 text-gray-800 border border-gray-300';
    }
  };

  // Check if reduced motion is enabled
  const isReducedMotion = getReducedMotion();

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.3 }}
      className={`p-4 rounded-lg border shadow-sm transition-all duration-200 hover:shadow-md hover:border-primary/40 relative overflow-hidden ${
        theme === 'dark'
          ? task.completed
            ? 'opacity-75 bg-gray-700/30 border-gray-600/50 text-gray-200'
            : 'bg-gray-800/90 border-gray-700 text-white'
          : task.completed
            ? 'opacity-75 bg-gray-50/50 border-gray-200/70 text-gray-600'
            : 'bg-white border-gray-200 text-gray-900'
      }`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      {/* Subtle background effect */}
      <div className="absolute inset-0 bg-transparent rounded-lg opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
      <motion.div
        layout
        className="flex items-start justify-between"
        animate={{
          transition: isReducedMotion ? { duration: 0.01 } : { duration: 0.15 }
        }}
      >
        <div className="flex items-start space-x-3 flex-1 min-w-0">
          <motion.button
            onClick={handleToggleComplete}
            className="mt-0.5 flex-shrink-0 transition-transform hover:scale-105"
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
            whileHover={!isReducedMotion ? { scale: 1.05 } : {}}
            whileTap={!isReducedMotion ? { scale: 0.95 } : {}}
            transition={isReducedMotion ? { duration: 0.01 } : {}}
          >
            <AnimatePresence mode="wait">
              <motion.span
                key={task.completed ? 'completed' : 'incomplete'}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.15 }}
              >
                {task.completed ? (
                  <FaCheckCircle className="text-primary text-xl" />
                ) : (
                  <FaRegCircle className="text-foreground/60 text-xl hover:text-primary" />
                )}
              </motion.span>
            </AnimatePresence>
          </motion.button>
          <div className="flex-1 min-w-0">
            <motion.h3
              className={`font-semibold text-base ${task.completed ? 'line-through text-muted-foreground' : theme === 'dark' ? 'text-white' : 'text-gray-900'}`}
              animate={{
                color: task.completed ? '#6b7280' : theme === 'dark' ? '#ffffff' : '#111827',
              }}
              transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.15 }}
            >
              {task.title}
            </motion.h3>
            {task.description && (
              <motion.p
                className={`text-sm mt-2 ${task.completed ? 'text-muted-foreground' : theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}
                initial={false}
                animate={{ opacity: task.completed ? 0.7 : 1 }}
                transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.15 }}
              >
                {task.description}
              </motion.p>
            )}
            <motion.div
              className="flex flex-wrap gap-2 mt-3"
              layout
            >
              {task.priority && (
                <motion.span
                  className={`text-xs px-2.5 py-1 rounded-full border ${getPriorityColor(task.priority)}`}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.15, delay: 0.1 }}
                >
                  {task.priority}
                </motion.span>
              )}
              {task.tags && task.tags.split(',').map((tag, index) => (
                <motion.span
                  key={index}
                  className={`text-xs px-2.5 py-1 rounded-full border ${
                    theme === 'dark'
                      ? 'bg-gray-700/40 text-gray-200 border-gray-600'
                      : 'bg-gray-200 text-gray-800 border-gray-300'
                  }`}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.15, delay: 0.15 + index * 0.05 }}
                >
                  {tag.trim()}
                </motion.span>
              ))}
              {task.due_date && (
                <motion.span
                  className={`text-xs px-2.5 py-1 rounded-full border ${
                    theme === 'dark'
                      ? 'bg-blue-700/30 text-blue-200 border-blue-800/50'
                      : 'bg-blue-100 text-blue-800 border-blue-300'
                  }`}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.15, delay: 0.2 }}
                >
                  {new Date(task.due_date).toLocaleDateString()}
                </motion.span>
              )}
            </motion.div>
          </div>
        </div>
        <AnimatePresence>
          {(showActions || false) && (
            <motion.div
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 10 }}
              transition={isReducedMotion ? { duration: 0.01 } : { duration: 0.2 }}
              className="flex space-x-2 ml-2 flex-shrink-0"
            >
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onEdit(task)}
                aria-label="Edit task"
                className="h-8 w-8 p-0"
                animate={{ scale: showActions ? 1 : 0.9 }}
                whileHover={!isReducedMotion ? { scale: 1.05 } : {}}
                whileTap={!isReducedMotion ? { scale: 0.95 } : {}}
                transition={isReducedMotion ? { duration: 0.01 } : {}}
              >
                <FaEdit className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onDelete(task.id)}
                aria-label="Delete task"
                className="h-8 w-8 p-0 text-destructive hover:text-destructive hover:bg-destructive/20"
                animate={{ scale: showActions ? 1 : 0.9 }}
                whileHover={!isReducedMotion ? { scale: 1.05 } : {}}
                whileTap={!isReducedMotion ? { scale: 0.95 } : {}}
                transition={isReducedMotion ? { duration: 0.01 } : {}}
              >
                <FaTrash className="h-4 w-4" />
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}