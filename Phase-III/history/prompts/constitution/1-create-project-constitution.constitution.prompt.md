---
id: 1
title: Create Project Constitution
stage: constitution
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Naz
command: /sp.constitution
labels: [constitution, spec-kit-plus, todo-app]
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

Project: Todo Full-Stack Web Application with Secure Multi-User Authentication

Core principles:
- Spec-driven development (all implementation must follow written specifications)
- Automation-first (no manual coding; all work via Claude Code & Spec-Kit Plus)
- Security by design (authentication, authorization, and data isolation enforced)
- Reliability (consistent API behavior and persistent storage)
- Maintainability (clear structure, modular architecture, and readable outputs)

Key standards:
- All functionality must originate from specs (spec → plan → tasks → implementation)
- All API behavior must match documented endpoints and contracts
- Authentication must use Better Auth with JWT tokens
- Backend must verify JWT tokens and enforce per-user data ownership
- Database interactions must use SQLModel with Neon Serverless PostgreSQL
- Frontend must use Next.js 16+ App Router and attach JWT to all API requests
- No manual edits to generated code; only iterative improvements through updated specs

Constraints:
- Stack:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth with JWT
- Architecture: RESTful API with stateless authentication
- Data model: Multi-user with strict task ownership
- All endpoints must require authentication after security integration
- Environment secrets must be managed via environment variables (e.g., BETTER_AUTH_SECRET)

Success criteria:
- All 5 basic task features implemented as a web application
- REST API fully functional with CRUD + completion toggle
- JWT-based authentication working end-to-end
- Each user can only access and modify their own tasks
- Unauthorized requests return proper HTTP errors (401/403)
- Application persists data reliably in Neon PostgreSQL
- Frontend is responsive and production-ready
- Entire workflow (specs, plans, iterations) is reviewable and reproducible
```

## Response snapshot

Created a new constitution file at `.specify/memory/constitution.md` with the following content:

- Core Principles: Spec-Driven Development, Automation-First, Security by Design, Reliability, Maintainability
- Additional Constraints: Technology stack and architectural requirements
- Development Workflow: Specification-driven development with automated implementation
- Governance: Rules for following spec → plan → tasks → implementation sequence

The constitution defines the fundamental principles for developing a Todo Full-Stack Web Application with secure multi-user authentication, specifying the technology stack (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT) and development methodology (spec-driven, automation-first).

## Outcome

- ✅ Impact: Created project constitution document defining development principles
- 🧪 Tests: none
- 📁 Files: Created .specify/memory/constitution.md
- 🔁 Next prompts: Continue with spec, plan, and task creation
- 🧠 Reflection: Constitution provides foundation for spec-driven development approach

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): begin creating feature specification based on constitution