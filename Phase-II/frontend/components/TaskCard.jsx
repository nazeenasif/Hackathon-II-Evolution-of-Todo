import { useState } from 'react';
import { FaRegCircle, FaCheckCircle, FaEdit, FaTrash } from 'react-icons/fa';
import Button from '@/components/ui/Button';

export default function TaskCard({ task, onEdit, onDelete, onToggleComplete }) {
  const [showActions, setShowActions] = useState(false);

  const handleToggleComplete = () => {
    onToggleComplete(task.id, !task.completed);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-destructive text-destructive-foreground';
      case 'medium':
        return 'bg-amber-500 text-foreground';
      case 'low':
        return 'bg-emerald-500 text-foreground';
      default:
        return 'bg-secondary text-secondary-foreground';
    }
  };

  return (
    <div
      className={`p-5 rounded-xl border bg-card text-card-foreground shadow-sm transition-all duration-200 hover:shadow-md ${
        task.completed ? 'opacity-75 bg-secondary/30' : 'bg-card'
      }`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-4 flex-1 min-w-0">
          <button
            onClick={handleToggleComplete}
            className="mt-0.5 flex-shrink-0 transition-transform hover:scale-105"
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          >
            {task.completed ? (
              <FaCheckCircle className="text-primary text-xl" />
            ) : (
              <FaRegCircle className="text-muted-foreground text-xl hover:text-primary" />
            )}
          </button>
          <div className="flex-1 min-w-0">
            <h3 className={`font-semibold text-base ${task.completed ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm mt-2 ${task.completed ? 'text-muted-foreground' : 'text-muted-foreground'}`}>
                {task.description}
              </p>
            )}
            <div className="flex flex-wrap gap-2 mt-3">
              {task.priority && (
                <span className={`text-xs px-2.5 py-1 rounded-full ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
              )}
              {task.tags && task.tags.split(',').map((tag, index) => (
                <span key={index} className="text-xs px-2.5 py-1 bg-secondary text-secondary-foreground rounded-full">
                  {tag.trim()}
                </span>
              ))}
              {task.due_date && (
                <span className="text-xs px-2.5 py-1 bg-accent text-accent-foreground rounded-full">
                  {new Date(task.due_date).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>
        </div>
        {(showActions || false) && (
          <div className="flex space-x-2 ml-2 flex-shrink-0">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit(task)}
              aria-label="Edit task"
              className="h-8 w-8 p-0"
            >
              <FaEdit className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(task.id)}
              aria-label="Delete task"
              className="h-8 w-8 p-0 text-destructive hover:text-destructive hover:bg-destructive/20"
            >
              <FaTrash className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}