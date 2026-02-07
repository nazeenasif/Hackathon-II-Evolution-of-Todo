# ADR-5: AI Chat Agent Architecture for Task Management

## Status
Proposed

## Date
2026-02-02

## Context
The team needs to integrate an AI-powered conversational interface into the existing full-stack todo application. The system must allow users to manage tasks using natural language while maintaining compatibility with the existing architecture (Next.js frontend, Python FastAPI backend, PostgreSQL database). The solution must handle conversation state management, integrate with existing task operations, and maintain security requirements.

Key constraints include:
- Must leverage existing backend functionality without modifying CRUD operations
- Must maintain stateless server architecture
- Must integrate with existing JWT-based authentication
- Need to support natural language processing for task operations

## Decision
We will implement a layered AI chat architecture consisting of:

1. **Frontend Layer**: ChatKit modal component integrated into existing Next.js app
2. **Backend Layer**: Stateless chat endpoint using OpenAI Assistants API
3. **Data Layer**: Conversation and Message entities with integer primary keys to match existing system
4. **Integration Layer**: MCP tools that map AI intents to existing task operations

The architecture will use:
- OpenAI Assistants API for AI processing and conversation management
- JWT authentication inherited from existing system
- Integer-based user IDs consistent with existing models
- MCP tools as intermediaries between AI and existing task operations

## Consequences

### Positive
- Maintains existing security model and authentication flow
- Preserves existing task CRUD operations, reducing risk
- Leverages OpenAI's managed conversation state while keeping server stateless
- Consistent data modeling with integer primary keys
- Clear separation of concerns between AI layer and business logic

### Negative
- Adds dependency on external AI service (OpenAI)
- Potential latency from AI processing affecting user experience
- Possible rate limiting constraints from AI provider
- Additional complexity from MCP tool layer

## Alternatives Considered

### Alternative 1: Custom NLP Solution
Build in-house natural language processing instead of using OpenAI
- Pros: Full control, no external dependencies, potentially lower cost at scale
- Cons: Significant development effort, less sophisticated AI capabilities, maintenance overhead

### Alternative 2: Direct Database Integration
Have AI agent directly manipulate task records instead of using MCP tools
- Pros: Simpler integration path
- Cons: Violates architectural constraint of not modifying existing CRUD operations, breaks security model

### Alternative 3: Client-Side AI Processing
Move AI processing to the frontend
- Pros: Reduced backend complexity
- Cons: Security concerns with API keys exposure, inconsistent UX across devices

## References
- specs/1-ai-chat-agent/impl-plan.md
- specs/1-ai-chat-agent/research.md
- specs/1-ai-chat-agent/data-model.md
- specs/1-ai-chat-agent/contracts/chat-api.yaml