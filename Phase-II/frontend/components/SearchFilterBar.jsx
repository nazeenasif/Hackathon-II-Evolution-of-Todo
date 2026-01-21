import { useState } from 'react';
import Input from '@/components/ui/Input';

export default function SearchFilterBar({ onFilterChange }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [completionFilter, setCompletionFilter] = useState('');
  const [tagFilter, setTagFilter] = useState('');
  const [sortBy, setSortBy] = useState('due_date');
  const [sortOrder, setSortOrder] = useState('asc');

  const handleInputChange = (setter, value) => {
    setter(value);
    triggerFilterUpdate();
  };

  const triggerFilterUpdate = () => {
    const filters = {
      search: searchTerm || undefined,
      priority: priorityFilter || undefined,
      completed: completionFilter ? completionFilter === 'completed' : undefined,
      tag: tagFilter || undefined,
      sort_by: sortBy,
      order: sortOrder
    };

    // Remove undefined values
    Object.keys(filters).forEach(key => {
      if (filters[key] === undefined) {
        delete filters[key];
      }
    });

    onFilterChange(filters);
  };

  const handleReset = () => {
    setSearchTerm('');
    setPriorityFilter('');
    setCompletionFilter('');
    setTagFilter('');
    setSortBy('due_date');
    setSortOrder('asc');

    onFilterChange({
      sort_by: 'due_date',
      order: 'asc'
    });
  };

  return (
    <div className="bg-card p-5 rounded-xl border shadow-sm mb-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Search */}
        <div>
          <label htmlFor="search" className="block text-sm font-medium text-foreground mb-2">
            Search
          </label>
          <Input
            type="text"
            id="search"
            value={searchTerm}
            onChange={(e) => handleInputChange(setSearchTerm, e.target.value)}
            placeholder="Search tasks..."
            className="w-full"
          />
        </div>

        {/* Priority Filter */}
        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-foreground mb-2">
            Priority
          </label>
          <select
            id="priority"
            value={priorityFilter}
            onChange={(e) => handleInputChange(setPriorityFilter, e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors duration-200"
          >
            <option value="">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        {/* Completion Filter */}
        <div>
          <label htmlFor="completion" className="block text-sm font-medium text-foreground mb-2">
            Status
          </label>
          <select
            id="completion"
            value={completionFilter}
            onChange={(e) => handleInputChange(setCompletionFilter, e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors duration-200"
          >
            <option value="">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
          </select>
        </div>

        {/* Tag Filter */}
        <div>
          <label htmlFor="tag" className="block text-sm font-medium text-foreground mb-2">
            Tag
          </label>
          <Input
            type="text"
            id="tag"
            value={tagFilter}
            onChange={(e) => handleInputChange(setTagFilter, e.target.value)}
            placeholder="Tag name..."
            className="w-full"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-5 pt-5 border-t border-border">
        {/* Sort By */}
        <div>
          <label htmlFor="sort-by" className="block text-sm font-medium text-foreground mb-2">
            Sort By
          </label>
          <select
            id="sort-by"
            value={sortBy}
            onChange={(e) => handleInputChange(setSortBy, e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors duration-200"
          >
            <option value="due_date">Due Date</option>
            <option value="priority">Priority</option>
            <option value="title">Title</option>
          </select>
        </div>

        {/* Sort Order */}
        <div>
          <label htmlFor="sort-order" className="block text-sm font-medium text-foreground mb-2">
            Sort Order
          </label>
          <select
            id="sort-order"
            value={sortOrder}
            onChange={(e) => handleInputChange(setSortOrder, e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors duration-200"
          >
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </div>
      </div>

      <div className="flex justify-end mt-5">
        <button
          type="button"
          onClick={handleReset}
          className="bg-secondary hover:bg-secondary/80 text-secondary-foreground px-4 py-2 rounded-md font-medium transition-colors duration-200 shadow-sm hover:shadow-md"
        >
          Reset Filters
        </button>
      </div>
    </div>
  );
}