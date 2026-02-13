# ADR-7: AI Chat API Contract Design

## Status
Proposed

## Date
2026-02-02

## Context
The AI chat system requires well-defined API endpoints that integrate seamlessly with the existing authentication system and follow RESTful patterns. The API must handle natural language input, return AI-generated responses, manage conversation state, and maintain compatibility with the existing JWT-based authentication. The design must support both chat functionality and conversation management operations.

Key constraints include:
- Must use existing JWT authentication mechanism
- Should follow existing API patterns in the application
- Need to handle AI-specific responses with tool call information
- Must support conversation lifecycle management
- Should be efficient for mobile and web clients

## Decision
We will implement a clean API design with:

1. **Chat Endpoint**: POST `/api/chat` for processing natural language input
2. **Conversation Endpoints**: GET/DELETE `/api/conversations` and `/api/conversations/{id}` for management
3. **Authentication**: JWT tokens in Authorization header (reusing existing auth system)
4. **Request/Response Format**: JSON with structured fields for conversation context and tool calls

The API will:
- Accept conversation_id and message in request body
- Return conversation_id, response text, and optional tool calls
- Support pagination for conversation listing
- Follow consistent error handling patterns
- Maintain backward compatibility with existing endpoints

## Consequences

### Positive
- Consistent with existing authentication patterns
- Clean separation of concerns between chat and conversation management
- Supports structured AI responses with tool call information
- Compatible with existing API design patterns
- Supports client-side caching and offline scenarios

### Negative
- New endpoint patterns may require additional client-side logic
- AI-specific response formats may complicate client handling
- Additional complexity for managing conversation state
- Potential rate limiting requirements from AI provider

## Alternatives Considered

### Alternative 1: WebSocket-based Real-time API
Use WebSockets for real-time chat interactions
- Pros: Real-time messaging, reduced latency, better for live interactions
- Cons: More complex implementation, harder to maintain, additional infrastructure needs

### Alternative 2: GraphQL API
Use GraphQL for more flexible queries and mutations
- Pros: More flexible client queries, reduced over-fetching
- Cons: Breaks consistency with existing REST API, additional learning curve

### Alternative 3: User-ID in Paths
Include user_id in API paths like `/api/users/{user_id}/chat`
- Pros: Explicit user identification
- Cons: Inconsistent with existing auth system that uses JWT tokens, redundant

## References
- specs/1-ai-chat-agent/contracts/chat-api.yaml
- specs/1-ai-chat-agent/impl-plan.md
- specs/1-ai-chat-agent/research.md