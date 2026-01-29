# Quickstart: Authentication, Authorization & API Security

## Overview
Setup guide for JWT-based authentication and authorization in the multi-user todo application.

## Prerequisites
- Backend from Spec 1 (001-backend-todo-core) is running
- Better Auth configured on the frontend (will be configured in this spec)
- Environment variable `BETTER_AUTH_SECRET` set with shared secret

## Environment Setup
1. Set the shared secret in your environment:
   ```bash
   export BETTER_AUTH_SECRET="your-secure-secret-key-here"
   ```

2. Add to your `.env` file:
   ```
   BETTER_AUTH_SECRET=your-secure-secret-key-here
   ```

## Dependencies Installation
Add JWT-related dependencies to your project:
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

## Key Integration Points
1. **Token Validation**: All API endpoints will require a valid JWT in the Authorization header
2. **User Identity Injection**: Authenticated user data will be available in route handlers
3. **Authorization Enforcement**: User-specific endpoints will validate user_id matches token

## Testing the Security
1. Make a request without a token → Should return 401 Unauthorized
2. Make a request with an invalid token → Should return 401 Unauthorized
3. Make a request with a valid token to access your own data → Should succeed
4. Make a request with a valid token to access another user's data → Should return 403 Forbidden

## Common Endpoints
- All existing endpoints from Spec 1 will now require authentication
- Example protected endpoint: `GET /api/{user_id}/tasks` (requires valid token with matching user_id)
- Authentication is handled via Authorization: Bearer <token> header