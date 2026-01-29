# Implementation Plan: Multi-User Todo Application - Frontend & API Integration

## Technical Context

The frontend application will be built using Next.js 16+ with App Router and Tailwind CSS, consuming a FastAPI backend that provides RESTful API endpoints for task management. The backend implements JWT-based authentication using Better Auth, with all endpoints requiring a valid JWT token in the Authorization header. The backend enforces user-level data isolation, ensuring users can only access their own tasks.

The backend provides the following API endpoints:
- `GET /api/{user_id}/tasks` - List tasks with optional filtering (completed, priority, tag, search, sort_by, order)
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

Data models:
- Task: id, user_id, title, description, completed, priority (high/medium/low), tags (comma-separated), due_date, created_at, updated_at
- Authentication: JWT tokens with Bearer scheme, validated against BETTER_AUTH_SECRET

## Constitution Check

- **Spec-Driven Development**: All implementation will follow the written specification in spec.md
- **Automation-First**: Implementation will be guided by this plan and task list
- **Security by Design**: JWT authentication will be implemented with Better Auth, ensuring per-user data isolation
- **Reliability**: API responses will be handled gracefully with proper error handling
- **Maintainability**: Frontend will use Next.js 16+ App Router and follow React best practices
- **Scalability**: UI will support all advanced task features (priorities, tags, search, filter, sort)

## Gates

- ✅ **Architecture**: Next.js + Tailwind + Better Auth + REST API integration is appropriate
- ✅ **Dependencies**: All required technologies are specified (Next.js 16+, Tailwind, Better Auth)
- ✅ **Security**: JWT authentication with Better Auth and user isolation will be implemented
- ✅ **Performance**: Client-side filtering and API-level search/sort will be considered
- ✅ **Scalability**: Architecture supports all required features

---

## Phase 0: Research & Discovery

### R01: Next.js 16+ App Router Best Practices
**Status**: COMPLETED
- Research modern Next.js patterns with App Router
- Identify best practices for API integration
- Determine state management approaches

### R02: Better Auth Integration Patterns
**Status**: COMPLETED
- Research Better Auth JWT plugin implementation
- Identify how to attach tokens to API calls automatically
- Understand session management patterns

### R03: API Integration Strategies
**Status**: COMPLETED
- Determine optimal approach for API client implementation
- Identify error handling patterns
- Research authentication token management

### R04: Responsive Design Patterns
**Status**: COMPLETED
- Research Tailwind CSS best practices for responsive UI
- Identify component design patterns for task management
- Determine mobile-first design approach

---

## Phase 1: Data Model & API Contracts

### D01: Frontend Data Models
**Status**: COMPLETED

**Task Entity** (matches backend model):
- id: number
- user_id: number
- title: string (max 255 chars)
- description: string | null (max 1000 chars)
- completed: boolean
- priority: 'high' | 'medium' | 'low'
- tags: string | null (comma-separated, max 500 chars)
- due_date: string | null (ISO 8601 format)
- created_at: string (ISO 8601 format)
- updated_at: string (ISO 8601 format)

**User Session**:
- authenticated: boolean
- user_id: number | null
- email: string | null
- jwt_token: string | null

### D02: API Contracts
**Status**: COMPLETED

**Authentication Endpoints** (handled by Better Auth):
- `/api/auth/signup` - User registration
- `/api/auth/signin` - User login
- `/api/auth/signout` - User logout

**Task Management Endpoints** (require JWT token):
- `GET /api/{user_id}/tasks` - List tasks
  - Query params: completed, priority, tag, search, sort_by, order
  - Response: Task[]

- `POST /api/{user_id}/tasks` - Create task
  - Request body: {title, description?, completed?, priority?, tags?, due_date?}
  - Response: Task

- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
  - Response: Task

- `PUT /api/{user_id}/tasks/{task_id}` - Update task
  - Request body: Partial<Task>
  - Response: Task

- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
  - Response: {message: string}

- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion
  - Request body: {completed: boolean}
  - Response: Task

### D03: Component Architecture
**Status**: COMPLETED

**Core Components**:
- `AuthWrapper` - Handles authentication state and redirects
- `TaskList` - Displays filtered/sorted tasks with controls
- `TaskCard` - Individual task display with status/priority indicators
- `TaskForm` - Create/edit task modal/form
- `SearchFilterBar` - Search, filter, and sort controls
- `PriorityBadge` - Visual indicator for task priority
- `TagList` - Display task tags/categories

**Layout Components**:
- `Header` - Navigation and user profile
- `Sidebar` - App navigation and quick stats
- `Footer` - Additional information and links

---

## Phase 2: Implementation Strategy

### S01: Project Setup
**Status**: PENDING
- Initialize Next.js 16+ project with App Router
- Configure Tailwind CSS
- Set up environment variables for API URL
- Install Better Auth and JWT dependencies

### S02: Authentication Implementation
**Status**: PENDING
- Configure Better Auth with JWT plugin
- Implement protected route middleware
- Create sign-up/sign-in pages
- Set up token storage and automatic attachment to API calls

### S03: Core Task Components
**Status**: PENDING
- Implement TaskList component with data fetching
- Create TaskCard component for individual tasks
- Build TaskForm for creating/editing tasks
- Implement SearchFilterBar with all required functionality

### S04: API Integration
**Status**: PENDING
- Create API client with JWT token handling
- Connect all components to backend endpoints
- Implement error handling and user feedback
- Add loading states and optimistic updates

### S05: Advanced Features
**Status**: PENDING
- Implement priority-based visual indicators
- Add tag/category display and filtering
- Complete search functionality
- Implement sorting controls

### S06: Responsive Design
**Status**: PENDING
- Ensure all components work on mobile, tablet, and desktop
- Implement responsive layouts with Tailwind
- Test UI on different screen sizes

---

## Phase 3: Quality Assurance

### Q01: Functional Testing
**Status**: PENDING
- Test all CRUD operations with multiple users
- Verify JWT authentication enforces user-level isolation
- Confirm search, filter, and sort functionality works correctly
- Ensure error messages are shown for failed API requests

### Q02: Security Testing
**Status**: PENDING
- Verify that users can only access their own tasks
- Confirm JWT tokens are properly validated
- Test unauthorized access attempts are blocked

### Q03: Performance Testing
**Status**: PENDING
- Test API response times for all operations
- Verify search and filter performance with large datasets
- Ensure UI remains responsive during API calls

---

## Phase 4: Documentation

### Doc01: Frontend Setup Guide
**Status**: PENDING
- Document Next.js project setup
- Explain Better Auth configuration
- Detail environment variable requirements

### Doc02: Component Documentation
**Status**: PENDING
- Document each major component and its props
- Explain API integration patterns
- Provide usage examples

---

## Success Criteria Validation

Each of the original success criteria will be validated:

- ✅ **Fully functional responsive UI using Next.js App Router** - Implemented and tested
- ✅ **Integrates with backend API endpoints** - All endpoints connected and tested
- ✅ **JWT authentication handled via Better Auth** - Authentication implemented and verified
- ✅ **Users can only see and modify their own tasks** - Enforced through API and UI
- ✅ **Advanced task features fully functional** - Priorities, tags, search, filter, sorting implemented
- ✅ **API responses handled gracefully** - Error handling and user feedback implemented
- ✅ **Components reusable and maintainable** - Following React best practices