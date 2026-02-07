# Data Model: Backend Core & Database Layer for Multi-User Todo Application

## Entity Definitions

### Task Entity
**Description**: Represents a user's todo item with various organizational features

**Fields**:
- `id`: Integer (Primary Key, Auto-incrementing)
- `user_id`: Integer (Foreign Key, references User.id, required)
- `title`: String (Required, max length 255)
- `description`: String (Optional, max length 1000)
- `completed`: Boolean (Default: False)
- `priority`: String (Enum: 'high', 'medium', 'low', Default: 'medium')
- `tags`: String (Optional, comma-separated values, max length 500)
- `due_date`: DateTime (Optional, nullable)
- `created_at`: DateTime (Auto-generated, timezone-aware)
- `updated_at`: DateTime (Auto-generated, timezone-aware, updates on change)

**Relationships**:
- Belongs to: User (via user_id foreign key)
- Validation: Must belong to an existing user

**Indexes**:
- Index on `(user_id)` for efficient user-based queries
- Index on `(user_id, completed)` for efficient status filtering
- Index on `(user_id, priority)` for efficient priority filtering
- Index on `(user_id, due_date)` for efficient date-based queries
- Composite index on `(user_id, completed, priority)` for combined filtering

### User Entity
**Description**: Represents a user account that owns tasks

**Fields**:
- `id`: Integer (Primary Key, Auto-incrementing)
- `email`: String (Unique, required, max length 255, validated format)
- `username`: String (Unique, required, max length 50)
- `created_at`: DateTime (Auto-generated, timezone-aware)
- `updated_at`: DateTime (Auto-generated, timezone-aware, updates on change)

**Relationships**:
- Has many: Tasks (via tasks.user_id foreign key)

**Indexes**:
- Unique index on `email`
- Unique index on `username`

## Validation Rules

### Task Validation
1. Title is required and must be 1-255 characters
2. Description, if provided, must be 1-1000 characters
3. Priority must be one of 'high', 'medium', 'low'
4. Due date, if provided, must be a valid future or past date
5. User_id must reference an existing user
6. Completed status must be boolean

### User Validation
1. Email is required, must be unique, and follow valid email format
2. Username is required, must be unique, and 1-50 characters
3. Both email and username must be unique across all users

## State Transitions

### Task State Transitions
- **Creation**: New task is created with completed=False (default)
- **Update**: Task details can be modified (title, description, priority, tags, due_date)
- **Completion Toggle**: completed status can be toggled between True/False
- **Deletion**: Task is removed from database (hard delete)

## Business Logic Constraints

1. **User Isolation**: A task can only be accessed/modified by the user who owns it (via user_id)
2. **Data Integrity**: Foreign key constraints prevent orphaned tasks
3. **Required Fields**: Essential fields (title, user_id) cannot be null
4. **Domain Validation**: Priority values restricted to predefined enum values
5. **Timestamp Management**: created_at and updated_at are automatically managed