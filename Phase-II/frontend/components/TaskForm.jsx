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
    <form onSubmit={handleSubmit} className="space-y-5 p-5 bg-card rounded-xl border shadow-sm">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-foreground mb-2">
          Title *
        </label>
        <Input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className={`${errors.title ? 'border-destructive' : ''}`}
          placeholder="Task title"
        />
        {errors.title && <p className="mt-2 text-sm text-destructive">{errors.title}</p>}
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-foreground mb-2">
          Description
        </label>
        <Input
          type="text"
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Task description"
        />
        {errors.description && <p className="mt-2 text-sm text-destructive">{errors.description}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-foreground mb-2">
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors duration-200"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label htmlFor="due_date" className="block text-sm font-medium text-foreground mb-2">
            Due Date
          </label>
          <Input
            type="datetime-local"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
          />
        </div>
      </div>

      <div>
        <label htmlFor="tags" className="block text-sm font-medium text-foreground mb-2">
          Tags (comma-separated)
        </label>
        <Input
          type="text"
          id="tags"
          name="tags"
          value={formData.tags}
          onChange={handleChange}
          placeholder="work, personal, urgent"
        />
      </div>

      <div className="flex items-center space-x-3 pt-2">
        <input
          type="checkbox"
          id="completed"
          name="completed"
          checked={formData.completed}
          onChange={handleChange}
          className="h-4 w-4 rounded border-input bg-background ring-offset-background focus:ring-2 focus:ring-ring focus:ring-offset-2"
        />
        <label htmlFor="completed" className="text-sm text-foreground">
          Completed
        </label>
      </div>

      <div className="flex space-x-3 pt-4">
        <Button type="submit" size="lg">
          {task ? 'Update Task' : 'Create Task'}
        </Button>
        {onCancel && (
          <Button type="button" variant="outline" size="lg" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}