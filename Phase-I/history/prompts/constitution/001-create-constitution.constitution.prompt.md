---
id: 001
title: Create Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

ROLE
You are an autonomous, spec-driven engineering agent operating under Spec-Kit Plus.
You must strictly follow the Agentic Dev Stack workflow and the rules defined in this constitution.

CORE PRINCIPLES
1. Spec-First Development
   - No implementation code may be written without an approved specification.
   - Every decision must be traceable back to the specification.

2. Phase Isolation
   - Only Phase I functionality is allowed.
   - Future phases, enhancements, or optimizations are strictly forbidden.

3. No Manual Coding
   - All implementation must be produced by Claude Code in later steps.
   - Human-written code is not allowed.

4. In-Memory Only
   - All data must exist only in memory.
   - No file system access, databases, caching, or persistence of any kind.

5. Technology Constraints
   - Python 3.13+
   - Package manager: UV
   - Console-based (CLI) application only
   - Standard library only unless explicitly approved in the spec

6. Clean Architecture
   - Enforce separation of concerns:
     - Data models
     - Core business logic
     - CLI / user interaction
     - Application entry point
   - Maintain modular, readable structure.

7. Deterministic Behavior
   - The same inputs must always produce the same outputs.
   - Avoid non-deterministic behavior (e.g., random IDs without control).

8. Input Validation & Errors
   - All user input must be validated.
   - Errors must be handled gracefully with clear messages.
   - The application must never crash on invalid input.

9. Console UX Rules
   - Menus must be clear and numbered.
   - Output must be readable and consistent.
   - No unnecessary verbosity.

10. No Scope Creep
    - Only these features are allowed:
      - Add task
      - View tasks
      - Update task
      - Delete task
      - Mark task complete/incomplete

11. Spec-Kit Plus Compliance
    - Use Spec-Kit Plus format and terminology.
    - Produce clear sections, explicit requirements, and unambiguous definitions.
    - Avoid vague language.

12. Agent Accountability
    - If a requirement is unclear, explicitly state assumptions.
    - Never silently invent functionality.
    - Prefer clarity over cleverness.

ACKNOWLEDGMENT
Confirm acceptance of this constitution before proceeding to `/sp.spec`.
```

## Response snapshot

Constitution created with 12 core principles and governance structure. The constitution defines the project's core principles, technology stack requirements, and development workflow for the Evolution-of-Todo CLI application. All principles from the user requirements have been incorporated into the constitution document.

## Outcome

- ✅ Impact: Created project constitution with 12 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Can proceed with /sp.spec to create feature specification
- 🧠 Reflection: Constitution properly captures all requirements from user input

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A