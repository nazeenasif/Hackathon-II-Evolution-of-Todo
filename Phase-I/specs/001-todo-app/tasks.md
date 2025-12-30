---
description: "Task list for In-Memory Python Console Todo Application implementation"
---

# Tasks: In-Memory Python Console Todo Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
- [x] T002 Initialize Python 3.13+ project with standard library only
- [x] T003 [P] Create src/models/, src/services/, src/cli/, and main.py directories/files

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task data model in src/models/task.py with id, title, description, status fields
- [x] T005 Create TaskManager service in src/services/task_manager.py with in-memory storage
- [x] T006 [P] Implement input validation utilities in src/utils/validation.py
- [x] T007 [P] Create menu system framework in src/cli/menu.py
- [x] T008 Setup application state management for in-memory storage

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with title and optional description, assigning unique IDs with default "Incomplete" status

**Independent Test**: Run application, select "Add task", enter title and description, verify task appears in list with unique ID and "Incomplete" status

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Unit test for Task creation in tests/unit/test_task.py
- [ ] T010 [P] [US1] Unit test for TaskManager.add_task in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [x] T011 [US1] Implement Task model with validation in src/models/task.py
- [x] T012 [US1] Implement TaskManager.add_task method in src/services/task_manager.py
- [x] T013 [US1] Implement add task functionality in src/cli/menu.py
- [x] T014 [US1] Add input validation for task creation in src/utils/validation.py
- [x] T015 [US1] Update main.py to integrate add task functionality

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to see all tasks currently stored in memory with ID, title, description, and status

**Independent Test**: Add one or more tasks, select "View tasks", verify all tasks are displayed with correct information

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Unit test for TaskManager.get_all_tasks in tests/unit/test_task_manager.py
- [ ] T017 [P] [US2] Integration test for viewing tasks in tests/integration/test_cli.py

### Implementation for User Story 2

- [x] T018 [US2] Implement TaskManager.get_all_tasks method in src/services/task_manager.py
- [x] T019 [US2] Implement view tasks functionality in src/cli/menu.py
- [x] T020 [US2] Add display formatting for tasks in src/cli/menu.py
- [x] T021 [US2] Update main.py to integrate view tasks functionality

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 6 - Exit Application (Priority: P1)

**Goal**: Enable users to close the application gracefully when done working with tasks

**Independent Test**: Select "Exit" from main menu, verify application terminates gracefully

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [ ] T022 [P] [US6] Integration test for exit functionality in tests/integration/test_cli.py

### Implementation for User Story 6

- [x] T023 [US6] Implement exit functionality in src/cli/menu.py
- [x] T024 [US6] Update main.py to handle exit gracefully
- [x] T025 [US6] Add proper cleanup if needed before exit

**Checkpoint**: Core application flow (add, view, exit) is now functional

---

## Phase 6: User Story 3 - Update Existing Task (Priority: P2)

**Goal**: Enable users to modify existing tasks by ID with new title and/or description while preserving status

**Independent Test**: Add a task, select "Update task", enter task ID and new information, verify task is updated with new information while status remains unchanged

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US3] Unit test for TaskManager.update_task in tests/unit/test_task_manager.py

### Implementation for User Story 3

- [x] T027 [US3] Implement TaskManager.update_task method in src/services/task_manager.py
- [x] T028 [US3] Implement update task functionality in src/cli/menu.py
- [x] T029 [US3] Add input validation for task updates in src/utils/validation.py
- [x] T030 [US3] Update main.py to integrate update task functionality

**Checkpoint**: At this point, User Stories 1, 2, 3, and 6 should all work independently

---

## Phase 7: User Story 4 - Delete Task (Priority: P2)

**Goal**: Enable users to remove tasks by ID from memory permanently

**Independent Test**: Add a task, select "Delete task", enter task ID, verify task is removed from system

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US4] Unit test for TaskManager.delete_task in tests/unit/test_task_manager.py

### Implementation for User Story 4

- [x] T032 [US4] Implement TaskManager.delete_task method in src/services/task_manager.py
- [x] T033 [US4] Implement delete task functionality in src/cli/menu.py
- [x] T034 [US4] Add confirmation logic if needed in src/cli/menu.py
- [x] T035 [US4] Update main.py to integrate delete task functionality

**Checkpoint**: At this point, User Stories 1, 2, 3, 4, and 6 should all work independently

---

## Phase 8: User Story 5 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Enable users to toggle task completion status between "Complete" and "Incomplete"

**Independent Test**: Add a task, select "Mark task complete/incomplete", enter task ID, verify status changes appropriately

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T036 [P] [US5] Unit test for TaskManager.toggle_status in tests/unit/test_task_manager.py

### Implementation for User Story 5

- [x] T037 [US5] Implement TaskManager.toggle_status method in src/services/task_manager.py
- [x] T038 [US5] Implement toggle status functionality in src/cli/menu.py
- [x] T039 [US5] Update main.py to integrate toggle status functionality

**Checkpoint**: All core functionality is now implemented and testable

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T040 [P] Add comprehensive error handling and user-friendly messages across all functions
- [x] T041 [P] Implement input validation for all user inputs with clear error messages
- [x] T042 [P] Add proper menu navigation and user experience improvements
- [x] T043 [P] Add documentation strings to all functions and classes
- [x] T044 [P] Add logging for debugging purposes in src/utils/logger.py
- [x] T045 Run quickstart.md validation to ensure all functionality works as expected
- [x] T046 [P] Add final integration tests covering all user stories in tests/integration/test_cli.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 6 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task creation in tests/unit/test_task.py"
Task: "Unit test for TaskManager.add_task in tests/unit/test_task_manager.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with validation in src/models/task.py"
Task: "Implement TaskManager.add_task method in src/services/task_manager.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence