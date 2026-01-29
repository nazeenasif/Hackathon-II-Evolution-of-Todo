# Feature Specification: Backend Core & Database Layer for Multi-User Todo Application

**Feature Branch**: `001-backend-todo-core`
**Created**: 2026-01-11
**Status**: Draft

## Scope

This specification defines the backend foundation for a multi-user Todo application, including database schema, persistence, and REST API behavior. It explicitly mandates automatic table creation in **Neon Serverless PostgreSQL** using **SQLModel** at application startup.

## Design Principles

* Spec-driven development (no manual code changes outside spec updates)
* Deterministic database schema creation
* Data integrity and strict user-level isolation
* Idempotent startup (safe to run multiple times without duplicating tables)

## User Scenarios & Testing

### User Story 1 - Create and Manage Individual Tasks (P1)

As a user, I want to create, read, update, and delete my personal tasks so that I can manage my daily activities.

**Acceptance Scenarios**:

1. Given a valid user_id, when a task is created, then it is persisted and associated with that user_id.
2. Given existing tasks, when fetching tasks for a user, then only that user's tasks are returned.
3. Given a task, when it is updated or deleted, then only the owner can affect it.

### User Story 2 - Advanced Task Features (P2)

As a user, I want priorities, categories/tags, search, filter, and completion tracking.

### User Story 3 - Sorting (P3)

As a user, I want to sort tasks by due date, priority, and alphabetically.

## Functional Requirements

* **FR-001**: Provide REST endpoints for CRUD operations.
* **FR-002**: Associate each task with a user_id and enforce isolation at query level.
* **FR-003**: Persist all data in Neon PostgreSQL using SQLModel.
* **FR-004**: Support priorities (high/medium/low).
* **FR-005**: Support tags/categories.
* **FR-006**: Support search, filtering, and sorting.
* **FR-007**: Enforce database-level constraints for data integrity.
* **FR-008**: **The system MUST automatically create all database tables in Neon at application startup.**
* **FR-009**: **All SQLModel models MUST be declared with `table=True`.**
* **FR-010**: **Table creation MUST be triggered via `SQLModel.metadata.create_all(engine)` during FastAPI startup.**
* **FR-011**: **All model definitions MUST be imported before table creation is executed.**
* **FR-012**: **The database connection MUST target Neon PostgreSQL with SSL enabled (`sslmode=require`).**

## Database Schema Requirements

### Task Entity

* id: primary key
* user_id: indexed, non-null
* title: non-null
* description: optional
* completed: boolean, default false
* priority: enum or constrained string (high/medium/low)
* category/tag: optional
* due_date: optional
* created_at: default now
* updated_at: auto-updated

### Constraints

* user_id + id must scope ownership
* invalid or missing required fields must be rejected

## Non-Goals

* Authentication and JWT (handled in Spec 2)
* Frontend UI (handled in Spec 3)
* Migrations beyond initial schema creation

## Success Criteria

* Tables are visible in Neon PostgreSQL after first startup
* Data persists across restarts
* CRUD, search, filter, and sort work without schema errors
* No cross-user data access
