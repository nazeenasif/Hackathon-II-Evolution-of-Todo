# ADR-6: Conversation and Message Data Model for AI Chat System

## Status
Proposed

## Date
2026-02-02

## Context
The AI chat system requires persistent storage for conversation history and message exchanges. The system must maintain compatibility with the existing data architecture (SQLModel, PostgreSQL, integer-based primary keys) while supporting AI-specific features like tool calls and structured responses. The data model needs to handle user isolation, conversation relationships, and efficient querying patterns for chat history retrieval.

Key constraints include:
- Must use integer primary keys to match existing system
- Must maintain user data isolation
- Need to store structured AI interactions (tool calls, results)
- Must support efficient chronological message retrieval
- Need to maintain conversation metadata (titles, timestamps)

## Decision
We will implement two related entities with integer primary keys:

1. **Conversation Entity** with fields: id (int), user_id (int), title (string), created_at, updated_at
2. **Message Entity** with fields: id (int), conversation_id (int), role (enum), content (text), tool_calls (JSONB), tool_call_results (JSONB), created_at

The model will include:
- Foreign key relationships between entities
- Proper indexing for user-based and chronological queries
- JSONB fields for flexible tool call storage
- Timestamps for audit and ordering
- Role enumeration for message types (user, assistant, system, tool)

## Consequences

### Positive
- Consistent with existing data modeling patterns
- Efficient querying with proper indexing
- Flexible storage for AI-specific data using JSONB
- Clear relationship model between conversations and messages
- Maintains user data isolation through foreign keys

### Negative
- JSONB fields may be difficult to query in complex ways
- Additional complexity for managing conversation state
- Storage overhead for tool call metadata
- Need for proper data validation on JSON fields

## Alternatives Considered

### Alternative 1: Document Database
Use MongoDB or similar for chat history
- Pros: Natural fit for conversation data, flexible schema
- Cons: Breaks consistency with existing PostgreSQL-based architecture, adds operational complexity

### Alternative 2: Single Combined Table
Store conversation and message data in one table
- Pros: Simplified schema
- Cons: Less normalized, harder to maintain referential integrity, inefficient querying

### Alternative 3: UUID Primary Keys
Use UUIDs instead of integers for better distributed systems support
- Pros: Better for distributed systems, globally unique
- Cons: Inconsistent with existing integer-based system, larger storage requirements

## References
- specs/1-ai-chat-agent/data-model.md
- specs/1-ai-chat-agent/impl-plan.md
- specs/1-ai-chat-agent/research.md