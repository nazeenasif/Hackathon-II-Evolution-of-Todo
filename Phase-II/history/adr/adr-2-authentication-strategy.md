# ADR-2: Authentication Strategy

## Title
Authentication Strategy: Better Auth with JWT Tokens for Frontend-Backend Integration

## Status
Accepted

## Date
2026-01-11

## Context
We need to implement secure authentication for the multi-user todo application that works seamlessly between the Next.js frontend and FastAPI backend. The authentication system must support user registration, login, session management, and JWT token generation/validation. The backend already expects JWT tokens in the Authorization header for all protected endpoints and enforces user-level data isolation.

## Decision
We will implement Better Auth with JWT plugin for frontend authentication, with the following characteristics:

- **Frontend Authentication**: Better Auth client for user registration, login, and session management
- **JWT Token Generation**: Better Auth will generate JWT tokens compatible with backend validation
- **Token Storage**: Secure storage of JWT tokens in browser with proper security measures
- **Token Interception**: Automatic attachment of JWT tokens to all backend API requests
- **Session Management**: Proper handling of token expiration and refresh mechanisms
- **Backend Compatibility**: JWT tokens will be validated against the same BETTER_AUTH_SECRET used by the backend

## Alternatives Considered
1. **Custom JWT Implementation**: Building authentication from scratch but would require significant development and security expertise
2. **NextAuth.js**: Alternative auth solution but Better Auth provides more streamlined JWT integration
3. **Firebase Authentication**: External provider but would add dependency and may not integrate as seamlessly with our backend
4. **OAuth Only**: Using third-party providers only but would limit user registration options
5. **Cookie-based Auth**: Alternative to JWT but would complicate API integration and stateless backend design

## Consequences
### Positive
- Better Auth provides complete authentication solution reducing development time
- JWT tokens work seamlessly with existing backend validation
- Built-in security best practices for token handling and storage
- Support for multiple authentication methods (email/password, social logins)
- Automatic session management and token refresh capabilities
- Strong security model with protection against common attack vectors

### Negative
- Additional dependency on Better Auth ecosystem
- Potential vendor lock-in to Better Auth patterns
- Learning curve for team members unfamiliar with Better Auth
- Need to coordinate secret management between frontend and backend
- Possible complexity in handling token expiration and refresh

## References
- specs/003-frontend-integration/plan.md
- specs/003-frontend-integration/spec.md
- backend/src/core/auth.py
- backend/src/core/security.py