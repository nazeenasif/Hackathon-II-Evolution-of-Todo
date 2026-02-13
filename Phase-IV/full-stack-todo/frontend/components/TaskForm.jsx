import { useState, useEffect } from 'react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';

export default function TaskForm({ task = null, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium',
    tags: '',
    due_date: '',
    completed: false
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        priority: task.priority || 'medium',
        tags: task.tags || '',
        due_date: task.due_date ? task.due_date.substring(0, 16) : '', // Format for datetime-local input
        completed: task.completed || false
      });
    } else {
      setFormData({
        title: '',
        description: '',
        priority: 'medium',
        tags: '',
        due_date: '',
        completed: false
      });
    }
  }, [task]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 255) {
      newErrors.title = 'Title must be less than 256 characters';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be less than 1001 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (validate()) {
      onSubmit({
        ...formData,
        due_date: formData.due_date ? formData.due_date : null
      });
    }
  };

  return (
    <div className="border border-border rounded-lg shadow-sm p-1">
      <form onSubmit={handleSubmit} className="space-y-6 p-6 bg-background rounded-lg">
        <div className="space-y-2">
          <label htmlFor="title" className="block text-sm font-semibold text-foreground mb-2">
            Task Title *
          </label>
          <div className="relative">
            <Input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className={`w-full h-12 text-lg rounded-lg border-2 ${errors.title ? 'border-destructive/50' : 'border-input/50'} bg-background/80 text-foreground transition-all duration-200 focus:border-primary/70 focus:ring-4 focus:ring-primary/10`}
              placeholder="What needs to be done?"
            />
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              <span className="text-muted-foreground text-sm">{formData.title.length}/255</span>
            </div>
          </div>
          {errors.title && (
            <div className="mt-2 text-sm text-destructive flex items-center">
              <span>⚠️</span>
              <span className="ml-1">{errors.title}</span>
            </div>
          )}
        </div>

        <div className="space-y-2">
          <label htmlFor="description" className="block text-sm font-semibold text-foreground mb-2">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={3}
            className="w-full rounded-lg border-2 border-input/50 bg-background/50 p-3 text-foreground placeholder:text-muted-foreground focus:border-primary/70 focus:ring-4 focus:ring-primary/10 transition-all duration-200 resize-none"
            placeholder="Add more details about this task..."
          />
          {errors.description && (
            <div className="mt-2 text-sm text-destructive flex items-center">
              <span>⚠️</span>
              <span className="ml-1">{errors.description}</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label htmlFor="priority" className="block text-sm font-semibold text-foreground mb-2">
              Priority Level
            </label>
            <div className="relative">
              <select
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="w-full h-12 rounded-lg border-2 border-input/50 bg-background/50 px-4 text-foreground focus:border-primary/70 focus:ring-4 focus:ring-primary/10 transition-all duration-200 appearance-none cursor-pointer"
              >
                <option value="low" className="bg-background">Low Priority</option>
                <option value="medium" className="bg-background">Medium Priority</option>
                <option value="high" className="bg-background">High Priority</option>
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3">
                <svg className="h-5 w-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="due_date" className="block text-sm font-semibold text-foreground mb-2">
              Due Date & Time
            </label>
            <Input
              type="datetime-local"
              id="due_date"
              name="due_date"
              value={formData.due_date}
              onChange={handleChange}
              className="w-full h-12 rounded-lg border-2 border-input/50 bg-background/50 text-foreground focus:border-primary/70 focus:ring-4 focus:ring-primary/10 transition-all duration-200"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label htmlFor="tags" className="block text-sm font-semibold text-foreground mb-2">
            Tags (comma-separated)
          </label>
          <div className="relative">
            <Input
              type="text"
              id="tags"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              placeholder="e.g., work, personal, urgent, project-x"
              className="w-full h-12 rounded-lg border-2 border-input/50 bg-background/50 text-foreground placeholder:text-muted-foreground focus:border-primary/70 focus:ring-4 focus:ring-primary/10 transition-all duration-200"
            />
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              <span className="text-muted-foreground text-sm"># tags</span>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2">
          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="completed"
              name="completed"
              checked={formData.completed}
              onChange={handleChange}
              className="h-5 w-5 rounded border-input bg-background ring-offset-background focus:ring-2 focus:ring-ring focus:ring-offset-2 cursor-pointer transition-all duration-200"
            />
            <label htmlFor="completed" className="text-sm font-medium text-foreground cursor-pointer">
              Mark as completed
            </label>
          </div>

          <div className="flex items-center space-x-3">
            <Button
              type="button"
              variant="outline"
              size="lg"
              onClick={onCancel}
              className="px-6 hover:bg-secondary transition-colors duration-200"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              size="lg"
              className="px-8 bg-gradient-to-r from-primary to-blue-600 hover:from-primary/90 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 active:scale-95"
            >
              <div className="flex items-center space-x-2">
                <span>{task ? 'Update Task' : 'Create Task'}</span>
                <span>📋</span>
              </div>
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
}